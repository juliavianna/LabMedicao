import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import os

# --- CONFIGURAÇÕES ---
FINAL_CSV_PATH = "analise_final_repositorios.csv"
OUTPUT_DIR = "graficos"
# --- FIM DAS CONFIGURAÇÕES ---

def perform_analysis_and_visualization(final_df):
    """
    Realiza a análise estatística e gera os gráficos de dispersão.
    (Esta função não precisa de alterações)
    """
    print(f"--- INICIANDO ANÁLISE E GERAÇÃO DE GRÁFICOS ---")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Diretório '{OUTPUT_DIR}' criado com sucesso.")

    rq_map = {
        "RQ01_Popularidade": {"metric": "stars", "label": "Popularidade (Estrelas)"},
        "RQ02_Maturidade": {"metric": "age_years", "label": "Maturidade (Anos)"},
        "RQ03_Atividade": {"metric": "releases_count", "label": "Atividade (Nº de Releases)"},
        "RQ04_Tamanho": {"metric": "size_kb", "label": "Tamanho (KB)"}
    }

    quality_metrics = {
        "median_cbo": "Mediana CBO",
        "median_dit": "Mediana DIT",
        "median_lcom": "Mediana LCOM"
    }

    for rq_name, rq_data in rq_map.items():
        print(f"\n--- Processando: {rq_name} ---")
        for quality_col, quality_label in quality_metrics.items():
            
            analysis_df = final_df[[rq_data["metric"], quality_col]].dropna()

            if len(analysis_df) < 2:
                print(f"AVISO: Dados insuficientes para analisar '{rq_data['label']}' vs. '{quality_label}'.")
                continue

            corr, p_value = spearmanr(analysis_df[rq_data["metric"]], analysis_df[quality_col])
            
            print(f"Análise: {rq_data['label']} vs. {quality_label}")
            print(f"  - Correlação de Spearman: {corr:.3f}")
            print(f"  - P-valor: {p_value:.3f}")

            plt.figure(figsize=(10, 6))
            sns.regplot(
                data=analysis_df,
                x=rq_data["metric"],
                y=quality_col,
                line_kws={"color": "red", "linestyle": "--"},
                scatter_kws={"alpha": 0.4}
            )

            plt.title(f'{rq_data["label"]} vs. {quality_label}')
            plt.xlabel(rq_data["label"])
            plt.ylabel(quality_label)
            plt.grid(True, linestyle='--', alpha=0.6)

            filename = f"{OUTPUT_DIR}/{rq_name}_{quality_col}.png"
            plt.savefig(filename)
            plt.close()
            print(f"  - Gráfico salvo em: {filename}")

def main():
    """
    Função principal que carrega os dados e inicia a análise.
    """
    if not os.path.exists(FINAL_CSV_PATH):
        print(f"ERRO: O arquivo '{FINAL_CSV_PATH}' não foi encontrado.")
        return

    # --- CORREÇÃO PRINCIPAL ---
    # Define os nomes corretos das colunas na ordem em que foram salvas
    column_names = [
        "repo_name",
        "stars",
        "age_years",
        "releases_count",
        "size_kb",
        "median_cbo",
        "median_dit",
        "median_lcom"
    ]

    try:
        # Carrega o CSV especificando que não há cabeçalho (header=None)
        # e fornecendo os nomes corretos para cada coluna.
        df = pd.read_csv(FINAL_CSV_PATH, header=None, names=column_names)
        print(f"Arquivo '{FINAL_CSV_PATH}' carregado com sucesso, contendo {len(df)} registros.")
        
    except Exception as e:
        print(f"ERRO: Falha ao ler o arquivo CSV. Detalhes: {e}")
        return

    # O resto do script funciona sem alterações agora que o DataFrame está correto
    if not df.empty:
        perform_analysis_and_visualization(df)
        print("\n--- ANÁLISE CONCLUÍDA! ---")
        print(f"Todos os gráficos foram salvos na pasta '{OUTPUT_DIR}'.")
    else:
        print("O arquivo CSV está vazio. Nenhuma análise será executada.")

if __name__ == "__main__":
    main()