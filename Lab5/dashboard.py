import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv("dados_experimento.csv")

# Configuração visual
plt.style.use('ggplot')

# 1. Gráfico de TEMPO (Boxplot para ver a variação)
plt.figure(figsize=(10, 6))
df.boxplot(column='tempo_ms', by='tecnologia', grid=True, patch_artist=True)
plt.title('Comparação de Tempo de Resposta (RQ1)')
plt.suptitle('') # Remove título automático do pandas
plt.ylabel('Tempo (ms)')
plt.xlabel('Tecnologia')
plt.savefig('grafico_tempo.png') # Salva a imagem
print("Gerado: grafico_tempo.png")

# 2. Gráfico de TAMANHO (Barra simples, já que é constante)
plt.figure(figsize=(8, 6))
medias_tamanho = df.groupby('tecnologia')['tamanho_bytes'].mean()
ax = medias_tamanho.plot(kind='bar', color=['purple', 'orange'])
plt.title('Comparação de Tamanho do Payload (RQ2)')
plt.ylabel('Tamanho (Bytes)')
plt.xlabel('Tecnologia')
plt.xticks(rotation=0)

# Adicionar os valores em cima das barras
for i, v in enumerate(medias_tamanho):
    ax.text(i, v + 500, str(int(v)), ha='center', fontweight='bold')

plt.savefig('grafico_tamanho.png') # Salva a imagem
print("Gerado: grafico_tamanho.png")