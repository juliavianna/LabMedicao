import requests
import os
import subprocess
import pandas as pd
import shutil
import time
from datetime import datetime, timezone

# Bibliotecas para a análise
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# --- FUNÇÕES AUXILIARES (sem alterações) ---

def run_command(command):
    print(f"Executando comando shell: {' '.join(command)}")
    try:
        subprocess.run(
            command, check=True, capture_output=True, text=True, 
            encoding='utf-8', errors='ignore'
        )
        print("Comando executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {' '.join(command)}")
        print("STDERR:", e.stderr)
        raise

def find_best_java_source_directory(root_path):
    print(f"Identificando o melhor diretório de código-fonte em '{root_path}'...")
    standard_path_suffix = os.path.join("src", "main", "java")
    for dirpath, _, _ in os.walk(root_path):
        if dirpath.endswith(standard_path_suffix):
            print(f"Diretório padrão Java encontrado: '{dirpath}'")
            return dirpath, -1
    print("Diretório padrão não encontrado. Usando fallback para contar arquivos .java...")
    best_path = root_path
    max_java_files = 0
    for dirpath, _, filenames in os.walk(root_path):
        if os.path.sep + '.' in dirpath:
            continue
        java_files_count = sum(1 for f in filenames if f.endswith('.java'))
        if java_files_count > max_java_files:
            max_java_files = java_files_count
            best_path = dirpath
    print(f"Diretório com mais arquivos Java encontrado: '{best_path}' ({max_java_files} arquivos).")
    return best_path, max_java_files

def remove_directory_with_retries(path, max_retries=5, delay_seconds=3):
    for attempt in range(max_retries):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                print(f"Diretório '{path}' removido com sucesso.")
            return True
        except PermissionError:
            time.sleep(delay_seconds)
        except FileNotFoundError:
            return True
    print(f"AVISO: Não foi possível apagar o diretório '{path}' após {max_retries} tentativas.")
    return False

# --- FUNÇÃO DE ANÁLISE E VISUALIZAÇÃO (sem alterações) ---

def perform_analysis_and_visualization(final_df):
    print("\n--- INICIANDO ANÁLISE E GERAÇÃO DE GRÁFICOS ---")
    if not os.path.exists("graficos"):
        os.makedirs("graficos")
    rq_map = {
        "RQ01_Popularidade": {"metric": "stars", "label": "Popularidade (Estrelas)"},
        "RQ02_Maturidade": {"metric": "age_years", "label": "Maturidade (Anos)"},
        "RQ03_Atividade": {"metric": "releases_count", "label": "Atividade (Nº de Releases)"},
        "RQ04_Tamanho": {"metric": "size_kb", "label": "Tamanho (KB)"}
    }
    quality_metrics = ["median_cbo", "median_dit", "median_lcom"]
    for rq_name, rq_data in rq_map.items():
        for quality_metric in quality_metrics:
            print(f"\nAnalisando: {rq_name} vs. {quality_metric}")
            analysis_df = final_df[[rq_data["metric"], quality_metric]].dropna()
            if len(analysis_df) < 2:
                print("Dados insuficientes para análise.")
                continue
            corr, p_value = spearmanr(analysis_df[rq_data["metric"]], analysis_df[quality_metric])
            print(f"Correlação de Spearman: {corr:.3f} (p-valor: {p_value:.3f})")
            plt.figure(figsize=(10, 6))
            sns.regplot(data=analysis_df, x=rq_data["metric"], y=quality_metric, line_kws={"color": "red"})
            plt.title(f'{rq_name}: {rq_data["label"]} vs. {quality_metric.replace("_", " ").upper()}')
            plt.xlabel(rq_data["label"])
            plt.ylabel(quality_metric.replace("_", " ").upper())
            plt.grid(True)
            filename = f"graficos/{rq_name}_{quality_metric}.png"
            plt.savefig(filename)
            plt.close()
            print(f"Gráfico salvo em: {filename}")

# --- FUNÇÃO PRINCIPAL (COM AS CORREÇÕES) ---

def main():
    GITHUB_TOKEN = "seu_token_aqui"  # substituir pelo token do GitHub E DPS APAGAR!!!!!!!!!!!!!!11
    NUM_REPOS_TO_ANALYZE = 20
    REPOS_PER_PAGE = 100
    FINAL_CSV_PATH = "analise_final_repositorios.csv"

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    num_pages = (NUM_REPOS_TO_ANALYZE + REPOS_PER_PAGE - 1) // REPOS_PER_PAGE

    for page in range(1, num_pages + 1):
        api_url = f"https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc&per_page={REPOS_PER_PAGE}&page={page}"
        
        try:
            print(f"\nBuscando página {page}/{num_pages} de repositórios...")
            response = requests.get(api_url, timeout=60, headers=headers)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"Erro fatal ao acessar a API do GitHub: {e}"); return
        
        repos = response.json().get('items', [])
        
        for i, repo_data in enumerate(repos):
            current_repo_index = (page - 1) * REPOS_PER_PAGE + i + 1
            if current_repo_index > NUM_REPOS_TO_ANALYZE:
                break

            repo_name = repo_data['name']
            clone_url = repo_data['clone_url']
            print(f"\n--- Processando Repositório {current_repo_index}/{NUM_REPOS_TO_ANALYZE}: {repo_name} ---")

            stars = repo_data.get('stargazers_count', 0)
            created_at_str = repo_data.get('created_at', '')
            age_years = (datetime.now(timezone.utc) - datetime.fromisoformat(created_at_str)).days / 365.25 if created_at_str else 0
            size_kb = repo_data.get('size', 0)
            
            releases_url = repo_data.get('releases_url', '').replace('{/id}', '')
            releases_count = 0
            try:
                releases_response = requests.get(f"{releases_url}?per_page=100", headers=headers, timeout=30)
                if releases_response.status_code == 200:
                    releases_count = len(releases_response.json())
            except requests.exceptions.RequestException:
                print("Aviso: Falha ao buscar releases.")

            repo_metrics = {
                "repo_name": repo_name, "stars": stars, "age_years": age_years, 
                "releases_count": releases_count, "size_kb": size_kb,
                "median_cbo": None, "median_dit": None, "median_lcom": None
            }

            try:
                run_command(["git", "clone", "--depth", "1", clone_url])
                source_path, file_count = find_best_java_source_directory(repo_name)
                
                if file_count != 0:
                    run_command(["java", "-jar", "ck.jar", source_path, "false", "0", "false"])
                    if os.path.exists("class.csv"):
                        df = pd.read_csv("class.csv", encoding='latin-1')
                        if not df.empty:
                            repo_metrics["median_cbo"] = df['cbo'].median()
                            repo_metrics["median_dit"] = df['dit'].median()
                            repo_metrics["median_lcom"] = df['lcom'].median()
                else:
                    print("Nenhum arquivo .java encontrado, pulando análise do CK.")
                
            except Exception as e:
                print(f"ERRO: Falha no processamento do repositório {repo_name}. Erro: {e}")
            finally:
                # <<-- CORREÇÃO: Lógica de salvar e limpar a CADA iteração -->>
                # 1. Converte o dicionário atual para um DataFrame de uma linha
                df_to_append = pd.DataFrame([repo_metrics])
                
                # 2. Verifica se o arquivo final existe para decidir se escreve o cabeçalho
                file_exists = os.path.exists(FINAL_CSV_PATH)
                
                # 3. Adiciona os dados ao CSV final
                df_to_append.to_csv(FINAL_CSV_PATH, mode='a', header=not file_exists, index=False)
                print(f"Dados do repositório '{repo_name}' salvos em {FINAL_CSV_PATH}")

                # 4. Limpa os arquivos temporários e o repositório clonado
                print("Iniciando limpeza dos arquivos temporários...")
                if os.path.exists("class.csv"): os.remove("class.csv")
                if os.path.exists("method.csv"): os.remove("method.csv")
                remove_directory_with_retries(repo_name)
            
    print(f"\n--- COLETA DE DADOS CONCLUÍDA! ---")

    # --- ETAPA 2: ANÁLISE E VISUALIZAÇÃO (Lê o arquivo final que foi atualizado) ---
    if os.path.exists(FINAL_CSV_PATH):
        final_df = pd.read_csv(FINAL_CSV_PATH)
        if not final_df.empty:
            perform_analysis_and_visualization(final_df)
        else:
            print("O arquivo de análise está vazio. A análise não pode ser executada.")
    else:
        print("Arquivo de análise final não encontrado. A análise não pode ser executada.")

if _name_ == "_main_":
    main()
