import pandas as pd  #Rodar no terminal pip install pandas

# Carrega os dados
df = pd.read_csv('lab01_data.csv')

# Converte datas para timezone-naive (sem fuso horário)
df['createdAt'] = pd.to_datetime(df['createdAt']).dt.tz_localize(None)
df['pushedAt'] = pd.to_datetime(df['pushedAt']).dt.tz_localize(None)
now = pd.Timestamp.now().tz_localize(None)

# RQ 01: Idade média dos repositórios

# RQ 01: Idade média dos repositórios
idade_media = (now - df['createdAt']).dt.days.mean()
idade_media_fmt = round(idade_media, 1)

# RQ 02: Média de pull requests aceitas
pr_media = df['pullRequests_totalCount'].mean()
pr_media_fmt = round(pr_media, 1)

# RQ 03: Média de releases
releases_media = df['releases_totalCount'].mean()
releases_media_fmt = round(releases_media, 1)

# RQ 04: Tempo médio desde a última atualização
tempo_ultima_atualizacao = (now - df['pushedAt']).dt.days.mean()
tempo_ultima_atualizacao_fmt = round(tempo_ultima_atualizacao, 1)

# RQ 05: Linguagens mais comuns
linguagens_comuns = df['primaryLanguage_name'].value_counts().head(5)
linguagens_comuns_fmt = '\n'.join([f"{lang}: {count}" for lang, count in linguagens_comuns.items()])

# RQ 06: Percentual médio de issues fechadas
df['issues_total'] = df['closedIssues_totalCount'] + df['openIssues_totalCount']
df['percent_issues_fechadas'] = df['closedIssues_totalCount'] / df['issues_total'] * 100
percent_issues_fechadas_media = df['percent_issues_fechadas'].mean()
percent_issues_fechadas_media_fmt = round(percent_issues_fechadas_media, 1)

# RQ 07: Comparação entre linguagens populares e outras
linguagens_populares = ['JavaScript', 'Python', 'TypeScript']
populares = df[df['primaryLanguage_name'].isin(linguagens_populares)]
outras = df[~df['primaryLanguage_name'].isin(linguagens_populares)]

comparacao = {
    'Contribuições médias (populares = JavaScript, Python ou TypeScript)': round(populares['pullRequests_totalCount'].mean(), 1),
    'Contribuições médias (outras)': round(outras['pullRequests_totalCount'].mean(), 1),
    'Releases médias (populares)': round(populares['releases_totalCount'].mean(), 1),
    'Releases médias (outras)': round(outras['releases_totalCount'].mean(), 1),
    'Atualização média (dias, populares)': round((now - populares['pushedAt']).dt.days.mean(), 1),
    'Atualização média (dias, outras)': round((now - outras['pushedAt']).dt.days.mean(), 1)
}

# Exibição dos resultados
print(f"RQ01 - Idade média dos repositórios (dias): {idade_media_fmt}")
print(f"RQ02 - Média de pull requests aceitas: {pr_media_fmt}")
print(f"RQ03 - Média de releases: {releases_media_fmt}")
print(f"RQ04 - Tempo médio desde a última atualização (dias): {tempo_ultima_atualizacao_fmt}")
print("RQ05 - Linguagens mais comuns:\n" + linguagens_comuns_fmt)
print(f"RQ06 - Percentual médio de issues fechadas: {percent_issues_fechadas_media_fmt}")
print("RQ07 - Comparação entre linguagens populares e outras:")
for k, v in comparacao.items():
    print(f"  {k}: {v}")