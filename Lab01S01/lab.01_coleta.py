import requests
import json
import os
import time

# Lê o token do ambiente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Erro: Defina a variável de ambiente GITHUB_TOKEN antes de rodar o script.")

API_URL = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"}

# Qtd total de repos
TOTAL_REPOS = 100
# Qts buscar por requisição 
BATCH_SIZE = 20

all_repos = []
after_cursor = None

while len(all_repos) < TOTAL_REPOS:
    # Consulta GraphQL
    query = f"""
    query {{
      search(query: "stars:>1000", type: REPOSITORY, first: {BATCH_SIZE}{', after: "' + after_cursor + '"' if after_cursor else ''}) {{
        repositoryCount
        pageInfo {{
          endCursor
          hasNextPage
        }}
        edges {{
          node {{
            ... on Repository {{
              nameWithOwner
              createdAt
              pushedAt
              releases(first: 1) {{
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
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(API_URL, headers=headers, data=json.dumps({"query": query}))
    response.raise_for_status()
    result = response.json()

    edges = result["data"]["search"]["edges"]
    all_repos.extend(edges)

    page_info = result["data"]["search"]["pageInfo"]
    after_cursor = page_info["endCursor"]

    if not page_info["hasNextPage"]:
        break

    time.sleep(1)  # Pausa curta para não sobrecarregar a API

# Limita exatamente a 100 repositórios
all_repos = all_repos[:TOTAL_REPOS]

# Salva o resultado final
with open("lab01_data.json", "w", encoding="utf-8") as f:
    json.dump({"data": {"search": {"edges": all_repos}}}, f, indent=4, ensure_ascii=False)

print(f"✅ {len(all_repos)} repositórios coletados e salvos em 'lab01_data.json' com sucesso!")
