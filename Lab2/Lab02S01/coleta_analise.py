import requests
import os
import subprocess
import pandas as pd
import shutil

def run_command(command):
    """Executa um comando no shell e lida com a saída."""
    print(f"Executando comando: {' '.join(command)}")
    try:
        # Usamos text=True para decodificar a saída como texto
        # Adicionamos um encoding para evitar erros em diferentes sistemas
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore'
        )
        print("Comando executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {' '.join(command)}")
        print("--- Erro Detalhado ---")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        print("----------------------")
        raise

def main():
    # --- Passo 1: Encontrar o repositório mais popular via API do GitHub ---
    print("Buscando o repo Java mais popular no GitHub...")
    api_url = "https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc&per_page=1"
    
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do GitHub: {e}")
        return

    repo_data = response.json()['items'][0]
    repo_name = repo_data['name']
    clone_url = repo_data['clone_url']
    
    print(f"repo encontrado: {repo_name}")
    print(f"URL para clone: {clone_url}")

    # --- Passo 2: Clonar o repositório ---
    clone_command = ["git", "clone", "--depth", "1", clone_url]
    
    if os.path.exists(repo_name):
        print(f"O repo '{repo_name}' já existe. Removendo para uma nova clonagem...")
        shutil.rmtree(repo_name)
        
    try:
        print("\nClonando o repo...")
        run_command(clone_command)
    except Exception as e:
        print(f"Falha ao clonar o repo. Erro: {e}")
        return

    # --- Passo 3: Rodar a ferramenta CK ---
    ck_jar_path = "ck.jar"
    
    if not os.path.exists(ck_jar_path):
        print(f"\nERRO: O arquivo '{ck_jar_path}' não foi encontrado.")
        print("Por favor, baixe a ferramenta CK e coloque o arquivo .jar na mesma pasta deste script.")
        print(f"\nRemovendo o diretório do repositório clonado: {repo_name}")
        shutil.rmtree(repo_name)
        return

    repo_path = repo_name
    output_dir = "output_ck" 
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    ck_command = [
        "java", "-jar", ck_jar_path,
        repo_path,  
        "false",  
        "0", 
        "false"  
    ]

    try:
        print("\nExecutando a ferramenta CK (isso pode levar alguns minutos)...")
        run_command(ck_command)
    except Exception as e:
        print(f"Falha ao executar a ferramenta CK. Verifique se o Java está instalado e configurado corretamente.")
        shutil.rmtree(repo_name)
        return

    # --- Passo 4, 5 e 6: Processar o CSV e gerar o arquivo final ---
    ck_output_file = os.path.join(output_dir, "class.csv")

    if not os.path.exists(ck_output_file):
        print(f"ERRO: O arquivo de saída do CK '{ck_output_file}' não foi encontrado após a execução.")
    else:
        print(f"\nProcessando o arquivo de resultados: {ck_output_file}")
        df = pd.read_csv(ck_output_file)
        
        metricas_interesse = ['cbo', 'dit', 'lcom']
        colunas_existentes = [col for col in metricas_interesse if col in df.columns]
        
        if colunas_existentes:
            print(f"Extraindo as métricas: {', '.join(colunas_existentes)}")
            df_metricas = df[colunas_existentes]
            
            final_csv_path = "quality_metrics.csv"
            df_metricas.to_csv(final_csv_path, index=False)
            
            print(f"\nSUCESSO! O arquivo final com as métricas de qualidade foi salvo em:")
            print(f"-> {os.path.abspath(final_csv_path)}")
        else:
            print("AVISO: Nenhuma das métricas de interesse (cbo, dit, lcom) foi encontrada no arquivo CSV gerado.")

    # --- Passo 7: Limpeza final ---
    print(f"\nLimpando os arquivos temporários...")
    print(f"Removendo o diretório do repo clonado: {repo_name}")
    shutil.rmtree(repo_name)
    if os.path.exists(output_dir):
        print(f"Removendo o diretório de saída do CK: {output_dir}")
        shutil.rmtree(output_dir)
    print("Limpeza concluída.")

if _name_ == "_main_":
    main()
