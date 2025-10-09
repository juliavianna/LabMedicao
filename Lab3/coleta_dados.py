import requests
import json
import csv
from datetime import datetime
from dateutil import parser
import time

# --- CONFIGURAÇÃO ---
# OBRIGATÓRIO: Crie e insira seu GitHub Personal Access Token (PAT) aqui.
GITHUB_TOKEN = "SEU_TOKEN_AQUI" 
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.com/v3+json"
}
BASE_URL = "https://api.github.com/repos"

# Lista de Repositórios Selecionados (Dono/Nome)
REPOSITORIOS = [
    "facebook/react",
    "kubernetes/kubernetes",
    "tensorflow/tensorflow",
    "dotnet/runtime",
    "home-assistant/core",
]

# --- FUNÇÕES DE COLETA E FILTRO ---

def fazer_requisicao(url, headers, timeout=15):
    """ Funcao auxiliar para tratar erros de conexao e timeout em requisicoes """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        return response
    except requests.exceptions.RequestException as e:
        # Erro de rede, DNS, ou Timeout. Retorna None.
        return None

def extrair_metrica_pr(repo_full_name, pr_number):
    """ Busca um PR específico e extrai as métricas, aplicando os filtros. """
    pr_url = f"{BASE_URL}/{repo_full_name}/pulls/{pr_number}"
    
    # 1. Requisição inicial do PR para dados básicos (Com tratamento de erro de rede)
    response = fazer_requisicao(pr_url, HEADERS)
    
    if response is None:
        return None
        
    # Imprime Status Code detalhado em caso de falha (problema de token/permissoes)
    if response.status_code != 200:
        return None
        
    pr_data = response.json()

    # Variáveis-chave de status e tempo
    pr_status = pr_data.get('state') 
    is_merged = pr_data.get('merged') 
    
    # CRITÉRIO DE FILTRO 1: MERGED ou CLOSED [cite: 33]
    if pr_status != 'closed':
        return None 
    
    created_at = parser.parse(pr_data.get('created_at'))
    closed_at = parser.parse(pr_data.get('closed_at')) if pr_data.get('closed_at') else None

    # CRITÉRIO DE FILTRO 3: Tempo de Análise > 1 hora [cite: 35]
    tempo_analise_seg = 0
    if closed_at:
        tempo_analise = closed_at - created_at
        tempo_analise_seg = tempo_analise.total_seconds()
        if tempo_analise_seg < 3600: # 3600 segundos = 1 hora
            return None
    else:
        return None 

    # CRITÉRIO DE FILTRO 2: Pelo menos uma revisão [cite: 34]
    reviews_url = f"{pr_url}/reviews"
    reviews_response = fazer_requisicao(reviews_url, HEADERS)
    
    if reviews_response is None or reviews_response.status_code != 200:
        return None 
        
    reviews_data = reviews_response.json()
    numero_revisoes = len(reviews_data)
    if numero_revisoes == 0:
        return None

    # EXTRAÇÃO DAS 8 MÉTRICAS (Definição de Métricas) [cite: 49, 50, 51, 53, 54]
    metricas = {
        'repo': repo_full_name,
        'pr_number': pr_number,
        'feedback_final': 'MERGED' if is_merged else 'CLOSED', # Variável dependente A [cite: 38]
        'numero_revisoes': numero_revisoes, # Variável dependente B [cite: 43]
        'tamanho_files': pr_data.get('changed_files'), # Métrica 1 [cite: 49]
        'tamanho_linhas_adicionadas': pr_data.get('additions'), # Métrica 2 [cite: 50]
        'tamanho_linhas_removidas': pr_data.get('deletions'), # Métrica 2 [cite: 50]
        'tempo_analise_horas': round(tempo_analise_seg / 3600, 2), # Métrica 3 [cite: 51]
        'descricao_caracteres': len(pr_data.get('body', '') or ''), # Métrica 4 [cite: 53]
        'interacoes_participantes': pr_data.get('user', {}).get('login'), # Métrica 5 [cite: 54]
        'interacoes_comentarios': pr_data.get('comments'), # Métrica 5 [cite: 54]
    }
    
    return metricas

def coletar_dados_repositorios(repositorios):
    """ Função principal que itera sobre os repositórios para coletar dados. """
    print(f"Iniciando coleta em {len(repositorios)} repositórios...")
    dados_coletados = []
    
    for repo in repositorios:
        print(f"\n[REPO] Coletando dados do repositório: {repo}")
        
        page = 1
        while True:
            # Busca PRs fechados (merged e closed)
            list_prs_url = f"{BASE_URL}/{repo}/pulls?state=closed&direction=desc&per_page=100&page={page}"
            response_list = fazer_requisicao(list_prs_url, HEADERS)
            
            if response_list is None:
                print(f"  > Erro de rede ao buscar lista de PRs na página {page}. Quebrando o loop.")
                break 

            if response_list.status_code != 200:
                print(f"  > Erro fatal ao buscar lista de PRs na página {page}: {response_list.status_code}. Quebrando o loop.")
                break 
            
            # Tratamento de erro de JSON (para evitar travamento silencioso)
            try:
                list_prs_data = response_list.json()
            except json.JSONDecodeError:
                print(f"  > ERRO FATAL DE JSON: Falha ao decodificar a lista de PRs. Quebrando o loop.")
                break

            if not list_prs_data:
                break 
            
            print(f"  > Processando {len(list_prs_data)} PRs na página {page}...")

            for pr_data in list_prs_data:
                pr_number = pr_data.get('number')
                metricas = extrair_metrica_pr(repo, pr_number)
                if metricas:
                    dados_coletados.append(metricas)
            
            # A correção de identação está aqui: page += 1 está fora do loop 'for'
            page += 1
            time.sleep(1.5)

    return dados_coletados

if __name__ == "__main__":
    dataset_final = coletar_dados_repositorios(REPOSITORIOS)
    
    if dataset_final:
        # Definir o nome do arquivo e os cabeçalhos
        csv_file = 'dataset_lab03.csv'
        fieldnames = list(dataset_final[0].keys())
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset_final)
            
        print(f"\nColeta finalizada. Total de {len(dataset_final)} entradas.")
        print(f"Dataset salvo em '{csv_file}'.")
    else:
        print("Coleta finalizada, mas nenhum PR passou nos filtros.")