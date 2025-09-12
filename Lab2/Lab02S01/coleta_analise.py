import requests
import os
import subprocess
import pandas as pd
import shutil

def run_command(command):
    try:
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
    print(f"URL: {clone_url}")

    # --- Passo 2: Clonar o repositório ---
    clone_command = ["git", "clone", "--depth", "1", clone_url]
    
    if os.path.exists(repo_name):
        print(f"O repo '{repo_name}' já existe")
        shutil.rmtree(repo_name)
        
    try:
        print("\nClonando o repo...")
        run_command(clone_command)
    except Exception as e:
        print(f"Falha ao clonar o repo. Erro: {e}")
        return

   
    # --- Passo 7: Limpeza final ---
    print(f"\nLimpando os arquivos temporários...")
    print(f"Removendo o diretório do repo clonado: {repo_name}")
    shutil.rmtree(repo_name)
   
    print("Limpeza concluída.")

if __name__ == "__main__":
    main()