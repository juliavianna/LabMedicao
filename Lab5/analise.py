import pandas as pd

# Carregar os dados
df = pd.read_csv("dados_experimento.csv")

print("--- ANÁLISE ESTATÍSTICA (Lab05S02) ---")

# Agrupar por tecnologia
grupo = df.groupby("tecnologia")

# 1. Análise de TEMPO (ms)
print("\n>>> RQ1: TEMPO DE RESPOSTA (ms)")
desc_tempo = grupo["tempo_ms"].describe()[['count', 'mean', 'std', '50%', 'min', 'max']]
desc_tempo.columns = ['Qtd', 'Média', 'Desvio Padrão', 'Mediana', 'Mín', 'Máx']
print(desc_tempo)

# Diferença percentual
media_rest_tempo = df[df["tecnologia"]=="REST"]["tempo_ms"].mean()
media_gql_tempo = df[df["tecnologia"]=="GraphQL"]["tempo_ms"].mean()
diff_tempo = ((media_gql_tempo - media_rest_tempo) / media_rest_tempo) * 100

print(f"\nDiferença: O GraphQL foi {abs(diff_tempo):.2f}% {'mais lento' if diff_tempo > 0 else 'mais rápido'} que o REST.")

# 2. Análise de TAMANHO (bytes)
print("\n>>> RQ2: TAMANHO DA RESPOSTA (bytes)")
desc_tamanho = grupo["tamanho_bytes"].describe()[['mean', 'std']]
desc_tamanho.columns = ['Média', 'Desvio Padrão']
print(desc_tamanho)

media_rest_tam = df[df["tecnologia"]=="REST"]["tamanho_bytes"].mean()
media_gql_tam = df[df["tecnologia"]=="GraphQL"]["tamanho_bytes"].mean()
razao = media_rest_tam / media_gql_tam

print(f"\nDiferença: A resposta REST é {razao:.1f} vezes maior que a do GraphQL.")