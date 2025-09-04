import requests
import os
import subprocess
import pandas as pd
import shutil
import time

def run_command(command):
    print(f"Executando comando shell: {' '.join(command)}")
    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, 
            encoding='utf-8', errors='ignore'
        )
        print("Comando executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {' '.join(command)}")
        print("--- Erro Detalhado ---")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        print("----------------------")
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

def main():
    api_url = "https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc&per_page=2"
    
    # <<-- ADICIONE O TOKEN AQUI!!!!!!!!!!!! -->>
    # Substitua a string abaixo pelo token que você gerou no GitHub
    GITHUB_TOKEN = ""
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    for f in ["class.csv", "method.csv", "quality_metrics.csv"]:
        if os.path.exists(f): os.remove(f)

    try:
        print("Buscando os repositórios Java mais populares no GitHub...")
        # <<-- MODIFICADO: Adiciona os headers na requisição -->>
        response = requests.get(api_url, timeout=30, headers=headers)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do GitHub: {e}"); 
        if "401" in str(e):
            print("--> Verifique se o seu GITHUB_TOKEN está correto e não expirou.")
        return

    repo_data = response.json()['items'][1]
    repo_name = repo_data['name']
    clone_url = repo_data['clone_url']
    
    print(f"Analisando o 2º repo mais popular: {repo_name}")
    print(f"URL para clone: {clone_url}")

    if os.path.exists(repo_name):
        print(f"O repo '{repo_name}' já existe. Removendo...")
        time.sleep(2)
        shutil.rmtree(repo_name)
        
    try:
        print("\nClonando o repo...")
        run_command(["git", "clone", "--depth", "1", clone_url])
    except Exception as e:
        print(f"Falha ao clonar o repo. Erro: {e}"); return

    ck_jar_path = "ck.jar"
    if not os.path.exists(ck_jar_path):
        print(f"\nERRO: O arquivo '{ck_jar_path}' não foi encontrado."); return

    source_path_to_analyze, file_count = find_best_java_source_directory(repo_name)
    
    if file_count == 0:
        print(f"\nAVISO: Nenhum arquivo .java encontrado no repositório '{repo_name}'. Pulando análise do CK.")
    else:
        ck_command = ["java", "-jar", ck_jar_path, source_path_to_analyze, "false", "0", "false"]
        try:
            print("\nExecutando a ferramenta CK...")
            run_command(ck_command)
        except Exception:
            print(f"Falha ao executar a ferramenta CK."); return

        ck_output_file = "class.csv"
        if not os.path.exists(ck_output_file) or os.path.getsize(ck_output_file) <= 100:
            print(f"ERRO: O arquivo de saída '{ck_output_file}' não foi encontrado ou está vazio.")
        else:
            print(f"\nProcessando o arquivo de resultados: {ck_output_file}")
            df = pd.read_csv(ck_output_file, encoding='latin-1')
            metricas_interesse = ['cbo', 'dit', 'lcom']
            df_metricas = df[metricas_interesse]
            final_csv_path = "quality_metrics.csv"
            df_metricas.to_csv(final_csv_path, index=False)
            print(f"\nSUCESSO! O arquivo final com as métricas de qualidade foi salvo em:")
            print(f"-> {os.path.abspath(final_csv_path)}")

    print(f"\nLimpando os arquivos temporários...")
    try:
        time.sleep(2)
        shutil.rmtree(repo_name)
        print("Limpeza do repositório concluída.")
    except PermissionError:
        print(f"AVISO: Não foi possível apagar o diretório '{repo_name}' devido a um erro de permissão.")

if __name__ == "__main__":
    main()