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