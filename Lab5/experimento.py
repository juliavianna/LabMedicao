import requests
import time
import pandas as pd

# --- CONFIGURAÇÕES ---
RODADAS = 50  # Faremos 30 chamadas para ter média estatística
URL_REST = "https://rickandmortyapi.com/api/character"
URL_GRAPHQL = "https://rickandmortyapi.com/graphql"

# Query GraphQL equivalente (trazendo APENAS nome e status)
QUERY_GQL = """
query {
  characters(page: 1) {
    results {
      name
      status
    }
  }
}
"""

resultados = []

print(f"--- INICIANDO O EXPERIMENTO ({RODADAS} RODADAS) ---")

for i in range(RODADAS):
    print(f"Rodada {i+1}/{RODADAS}...", end="\r") # O end="\r" faz ficar na mesma linha
    
    # 1. TESTE REST (Traz dados demais = Overfetching)
    inicio = time.time()
    resp_rest = requests.get(URL_REST)
    fim = time.time()
    
    tempo_rest = (fim - inicio) * 1000 # Converte para milissegundos
    tamanho_rest = len(resp_rest.content) # Tamanho em bytes
    
    resultados.append({
        "rodada": i + 1,
        "tecnologia": "REST",
        "tempo_ms": tempo_rest,
        "tamanho_bytes": tamanho_rest
    })
    
    # 2. TESTE GRAPHQL (Traz apenas o pedido)
    inicio = time.time()
    resp_gql = requests.post(URL_GRAPHQL, json={'query': QUERY_GQL})
    fim = time.time()
    
    tempo_gql = (fim - inicio) * 1000
    tamanho_gql = len(resp_gql.content)
    
    resultados.append({
        "rodada": i + 1,
        "tecnologia": "GraphQL",
        "tempo_ms": tempo_gql,
        "tamanho_bytes": tamanho_gql
    })

print("\n\n--- FINALIZADO! ---")

# Salvar em CSV para usar na próxima entrega (Dashboard)
df = pd.DataFrame(resultados)
df.to_csv("dados_experimento.csv", index=False)

print("Arquivo 'dados_experimento.csv' gerado com sucesso.")
print("\n--- MÉDIAS PRELIMINARES ---")
print(df.groupby("tecnologia")[["tempo_ms", "tamanho_bytes"]].mean())