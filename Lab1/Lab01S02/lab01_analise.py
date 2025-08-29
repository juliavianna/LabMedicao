import pandas as pd  #Rodar no terminal pip install pandas

import matplotlib.pyplot as plt

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
    'Contribuições médias (populares)': round(populares['pullRequests_totalCount'].mean(), 1),
    'Contribuições médias (outras)': round(outras['pullRequests_totalCount'].mean(), 1),
    'Releases médias (populares)': round(populares['releases_totalCount'].mean(), 1),
    'Releases médias (outras)': round(outras['releases_totalCount'].mean(), 1),
    'Atualização média (dias, populares)': round((now - populares['pushedAt']).dt.days.mean(), 1),
    'Atualização média (dias, outras)': round((now - outras['pushedAt']).dt.days.mean(), 1)
}

# Exibição dos resultados

print("\n===== MÉDIAS das RQs =====")
print(f"RQ01 - Idade média dos repositórios (dias): {idade_media_fmt}")
print(f"RQ02 - Média de pull requests aceitas: {pr_media_fmt}")
print(f"RQ03 - Média de releases: {releases_media_fmt}")
print(f"RQ04 - Tempo médio desde a última atualização (dias): {tempo_ultima_atualizacao_fmt}")
print("RQ05 - Linguagens mais comuns:\n" + linguagens_comuns_fmt)
print(f"RQ06 - Percentual médio de issues fechadas: {percent_issues_fechadas_media_fmt}")
print("RQ07 - Comparação entre linguagens populares e outras:")
for k, v in comparacao.items():
    print(f"  {k}: {v}")

# Exibição das medianas
print("\n===== MEDIANAS das RQs =====")
idade_mediana = (now - df['createdAt']).dt.days.median()
print(f"RQ01 - Idade mediana dos repositórios (dias): {round(idade_mediana, 1)}")

pr_mediana = df['pullRequests_totalCount'].median()
print(f"RQ02 - Mediana de pull requests aceitas: {round(pr_mediana, 1)}")

releases_mediana = df['releases_totalCount'].median()
print(f"RQ03 - Mediana de releases: {round(releases_mediana, 1)}")

tempo_ultima_atualizacao_mediana = (now - df['pushedAt']).dt.days.median()
print(f"RQ04 - Tempo mediano desde a última atualização (dias): {round(tempo_ultima_atualizacao_mediana, 1)}")

percent_issues_fechadas_mediana = df['percent_issues_fechadas'].median()
print(f"RQ06 - Percentual mediano de issues fechadas: {round(percent_issues_fechadas_mediana, 1)}")

# RQ07 - Medianas para linguagens populares e outras
populares_mediana = {
    'Contribuições medianas (populares)': round(populares['pullRequests_totalCount'].median(), 1),
    'Releases medianas (populares)': round(populares['releases_totalCount'].median(), 1),
    'Atualização mediana (dias, populares)': round((now - populares['pushedAt']).dt.days.median(), 1)
}
outras_mediana = {
    'Contribuições medianas (outras)': round(outras['pullRequests_totalCount'].median(), 1),
    'Releases medianas (outras)': round(outras['releases_totalCount'].median(), 1),
    'Atualização mediana (dias, outras)': round((now - outras['pushedAt']).dt.days.median(), 1)
}
print("RQ07 - Medianas entre linguagens populares e outras:")
for k, v in populares_mediana.items():
    print(f"  {k}: {v}")
for k, v in outras_mediana.items():
    print(f"  {k}: {v}")


# RQ01: Idade média dos repositórios
plt.figure()
plt.hist((now - df['createdAt']).dt.days, bins=30, color='skyblue')
plt.title('RQ01 - Distribuição da Idade dos Repositórios (dias)')
plt.xlabel('Idade (dias)')
plt.ylabel('Quantidade')
plt.grid(True)

# RQ02: Pull requests aceitas
plt.figure()
plt.hist(df['pullRequests_totalCount'], bins=30, color='orange')
plt.title('RQ02 - Distribuição de Pull Requests Aceitas')
plt.xlabel('Pull Requests Aceitas')
plt.ylabel('Quantidade')
plt.grid(True)

# RQ03: Releases
plt.figure()
plt.hist(df['releases_totalCount'], bins=30, color='green')
plt.title('RQ03 - Distribuição de Releases')
plt.xlabel('Releases')
plt.ylabel('Quantidade')
plt.grid(True)

# RQ04: Tempo desde a última atualização
plt.figure()
plt.hist((now - df['pushedAt']).dt.days, bins=30, color='purple')
plt.title('RQ04 - Tempo desde a Última Atualização (dias)')
plt.xlabel('Dias desde última atualização')
plt.ylabel('Quantidade')
plt.grid(True)

# RQ05: Linguagens mais comuns
plt.figure()
linguagens_comuns.plot(kind='bar', color='teal')
plt.title('RQ05 - Linguagens Mais Comuns')
plt.xlabel('Linguagem')
plt.ylabel('Quantidade')
plt.grid(True)

# RQ06: Percentual de issues fechadas
plt.figure()
plt.hist(df['percent_issues_fechadas'].dropna(), bins=30, color='red')
plt.title('RQ06 - Percentual de Issues Fechadas')
plt.xlabel('Percentual (%)')
plt.ylabel('Quantidade')
plt.grid(True)

# RQ07: Comparação entre linguagens populares e outras
labels = ['Contribuições', 'Releases', 'Atualização (dias)']
populares_vals = [
    comparacao['Contribuições médias (populares)'],
    comparacao['Releases médias (populares)'],
    comparacao['Atualização média (dias, populares)']
]
outras_vals = [
    comparacao['Contribuições médias (outras)'],
    comparacao['Releases médias (outras)'],
    comparacao['Atualização média (dias, outras)']
]

x = range(len(labels))
plt.figure()
plt.bar(x, populares_vals, width=0.4, label='Populares', align='center', color='blue')
plt.bar([i + 0.4 for i in x], outras_vals, width=0.4, label='Outras', align='center', color='gray')
plt.xticks([i + 0.2 for i in x], labels)
plt.title('RQ07 - Comparação Populares vs Outras Linguagens')
plt.ylabel('Média')
plt.legend()
plt.grid(True)

plt.show()
