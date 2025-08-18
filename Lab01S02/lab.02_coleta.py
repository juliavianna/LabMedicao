import requests
import json
import os
import time
import csv
from datetime import datetime

# Lê o token do ambiente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Erro: Defina a variável de ambiente GITHUB_TOKEN antes de rodar o script.")

API_URL = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"}

TOTAL_REPOS = 1000
BATCH_SIZE_LIST = 100  # Usaremos um lote maior para a lista de repositórios, que é mais leve.
BATCH_SIZE_DETAILS = 5 # Um lote pequeno para os detalhes, para evitar erros.

def get_repo_list():
    """Coleta a lista de 1000 repositórios (apenas nome e data de criação)."""
    repo_list = []
    after_cursor = None
    
    while len(repo_list) < TOTAL_REPOS:
        print(f"Coletando lista de repositórios... Total coletado: {len(repo_list)}")
        query = f"""
        query {{
          search(query: "stars:>1000", type: REPOSITORY, first: {BATCH_SIZE_LIST}{', after: "' + after_cursor + '"' if after_cursor else ''}) {{
            pageInfo {{
              endCursor
              hasNextPage
            }}
            edges {{
              node {{
                ... on Repository {{
                  nameWithOwner
                  createdAt
                }}
              }}
            }}
          }}
        }}
        """
        try:
            response = requests.post(API_URL, headers=headers, data=json.dumps({"query": query}))
            response.raise_for_status()
            result = response.json()
            
            edges = result["data"]["search"]["edges"]
            repo_list.extend(edges)

            page_info = result["data"]["search"]["pageInfo"]
            after_cursor = page_info["endCursor"]

            if not page_info["hasNextPage"] or len(repo_list) >= TOTAL_REPOS:
                break
                
            time.sleep(1)
            
        except requests.exceptions.HTTPError as err:
            print(f"Erro HTTP ao coletar a lista: {err}")
            return None
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
            
    return repo_list[:TOTAL_REPOS]

def get_repo_details(repo_list):
    """Para cada repositório da lista, coleta os detalhes."""
    detailed_data = []
    for i, repo_edge in enumerate(repo_list):
        repo_name = repo_edge.get("node", {}).get("nameWithOwner")
        print(f"Coletando detalhes do repositório {i+1}/{TOTAL_REPOS}: {repo_name}")
        
        query = f"""
        query {{
          repository(owner: "{repo_name.split('/')[0]}", name: "{repo_name.split('/')[1]}") {{
            pushedAt
            releases {{
              totalCount
            }}
            primaryLanguage {{
              name
            }}
            pullRequests(states: MERGED) {{
              totalCount
            }}
            closedIssues: issues(states: CLOSED) {{
              totalCount
            }}
            openIssues: issues(states: OPEN) {{
              totalCount
            }}
            stargazers {{
              totalCount
            }}
          }}
        }}
        """
        
        try:
            response = requests.post(API_URL, headers=headers, data=json.dumps({"query": query}))
            response.raise_for_status()
            result = response.json()
            
            repo_details = result["data"]["repository"]
            
            # Combina os dados de identificação com os detalhes
            combined_data = {
                "nameWithOwner": repo_name,
                "createdAt": repo_edge.get("node", {}).get("createdAt"),
                "pushedAt": repo_details.get("pushedAt"),
                "releases_totalCount": repo_details.get("releases", {}).get("totalCount", 0),
                "primaryLanguage_name": repo_details.get("primaryLanguage", {}).get("name", "N/A"),
                "pullRequests_totalCount": repo_details.get("pullRequests", {}).get("totalCount", 0),
                "closedIssues_totalCount": repo_details.get("closedIssues", {}).get("totalCount", 0),
                "openIssues_totalCount": repo_details.get("openIssues", {}).get("totalCount", 0),
                "stargazers_totalCount": repo_details.get("stargazers", {}).get("totalCount", 0)
            }
            detailed_data.append(combined_data)

            time.sleep(1) # Pausa para evitar sobrecarga

        except requests.exceptions.HTTPError as err:
            print(f"Erro HTTP ao coletar detalhes para {repo_name}: {err}")
            # Pula para o próximo repositório
            continue
        except Exception as e:
            print(f"Ocorreu um erro ao coletar detalhes para {repo_name}: {e}")
            continue

    return detailed_data

def save_to_csv(data, filename="lab01_data.csv"):
    """Salva os dados coletados em um arquivo CSV."""
    if not data:
        print("Nenhum dado para salvar.")
        return
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Dados salvos em '{filename}' com sucesso!")

# Execução do processo principal
if __name__ == "__main__":
    initial_list = get_repo_list()
    if initial_list:
        final_data = get_repo_details(initial_list)
        if final_data:
            save_to_csv(final_data)