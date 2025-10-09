import pandas as pd
from scipy.stats import spearmanr
import numpy as np
import json

# Nome do arquivo de dataset gerado
CSV_FILE = 'dataset_lab03.csv'

def carregar_e_limpar_dados(file):
    """Carrega o CSV e prepara os dados para análise."""
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print(f"Erro: Arquivo {file} não encontrado. Certifique-se de que a coleta de dados foi concluída.")
        return None
    
    # Limpeza e preparação dos dados
    df = df.dropna(subset=['feedback_final', 'numero_revisoes'])

    # Converter variáveis categóricas (MERGED/CLOSED) para numéricas (0/1)
    df['is_merged'] = df['feedback_final'].apply(lambda x: 1 if x == 'MERGED' else 0)
    
    # As métricas numéricas devem ser tratadas como float
    numeric_cols = [
        'tamanho_files', 'tamanho_linhas_adicionadas', 'tamanho_linhas_removidas', 
        'tempo_analise_horas', 'descricao_caracteres', 'interacoes_comentarios', 
        'numero_revisoes', 'is_merged'
    ]
    
    for col in numeric_cols:
        # Força a coluna a ser numérica, substituindo erros por NaN e depois descartando-os
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    df = df.dropna(subset=numeric_cols)
    
    print(f"Dataset carregado e limpo: {len(df)} entradas prontas para análise.")
    return df

def calcular_correlacao_spearman(df, var_independente, var_dependente, label_dependente):
    """Calcula a correlação de Spearman e o p-valor entre duas variáveis."""
    if len(df) < 2:
        return None, None

    # Correlação de Spearman é robusta para dados não normais e ordinais.
    coeficiente, p_valor = spearmanr(df[var_independente], df[var_dependente])
    
    # Verifica a significância estatística (p-valor < 0.05)
    significante = p_valor < 0.05
    
    return coeficiente, p_valor, significante

def gerar_analise(df):
    """Gera a sumarização por mediana e as correlações para as 8 RQs."""
    
    # Dicionário de resultados para o relatório
    resultados_analise = {
        'sumarizacao_mediana': {},
        'correlacoes': {}
    }
    
    # ----------------------------------------------------------------------
    # 1. SUMARIZAÇÃO DOS DADOS (MEDIANAS)
    # ----------------------------------------------------------------------
    print("\n--- 1. Sumarização por Mediana (Para o Relatório) ---")
    
    # Mediana geral para o dataset inteiro (requisito do Lab03S03)
    sumarizacao_geral = df[['tamanho_files', 'tamanho_linhas_adicionadas', 'tempo_analise_horas', 
                            'numero_revisoes', 'interacoes_comentarios']].median()
    
    for metrica, valor in sumarizacao_geral.items():
        resultados_analise['sumarizacao_mediana'][metrica] = round(valor, 2)
        print(f"Mediana de {metrica}: {round(valor, 2)}")
        
    # Mediana para variáveis comparadas por status (para discussão)
    medianas_por_status = df.groupby('feedback_final')[['tamanho_linhas_adicionadas', 'tempo_analise_horas', 
                                                          'numero_revisoes', 'interacoes_comentarios']].median()
    
    resultados_analise['sumarizacao_mediana']['por_status'] = medianas_por_status.to_dict()
    print("\nMedianas por Status (MERGED/CLOSED):")
    print(medianas_por_status)

    # ----------------------------------------------------------------------
    # 2. CORRELAÇÕES DE SPEARMAN (Para as 8 RQs)
    # ----------------------------------------------------------------------
    print("\n--- 2. Correlações de Spearman (Para as 8 RQs) ---")
    
    # Variáveis Independentes
    indep = {
        'Tamanho': 'tamanho_linhas_adicionadas', 
        'Tempo de Análise': 'tempo_analise_horas', 
        'Descrição': 'descricao_caracteres', 
        'Interações': 'interacoes_comentarios'
    }
    
    # Relações a serem testadas (RQ, Variável Independente, Variável Dependente)
    relacoes = [
        ('RQ01', 'Tamanho', 'is_merged'),
        ('RQ02', 'Tempo de Análise', 'is_merged'),
        ('RQ03', 'Descrição', 'is_merged'),
        ('RQ04', 'Interações', 'is_merged'),
        ('RQ05', 'Tamanho', 'numero_revisoes'),
        ('RQ06', 'Tempo de Análise', 'numero_revisoes'),
        ('RQ07', 'Descrição', 'numero_revisoes'),
        ('RQ08', 'Interações', 'numero_revisoes')
    ]
    
    for rq, label_indep, dep_var in relacoes:
        indep_var = indep[label_indep]
        
        coef, p_val, sig = calcular_correlacao_spearman(df, indep_var, dep_var, rq)
        
        resultado = {
            'RQ': rq,
            'Variáveis': f"{label_indep} vs. {dep_var}",
            'Correlação_Spearman': round(coef, 3) if coef is not None else 'N/A',
            'P_Valor': round(p_val, 4) if p_val is not None else 'N/A',
            'Significante': 'Sim' if sig else 'Não'
        }
        resultados_analise['correlacoes'][rq] = resultado
        print(f"{rq} - {resultado['Variáveis']}: Coeficiente = {resultado['Correlação_Spearman']}, P-valor = {resultado['P_Valor']} (Significativo: {resultado['Significante']})")

    return resultados_analise

if __name__ == "__main__":
    # Garante que o Pandas e SciPy estão instalados
    try:
        import pandas as pd
        from scipy.stats import spearmanr
    except ImportError:
        print("ERRO: Pandas e/ou SciPy não estão instalados. Por favor, rode 'python -m pip install pandas scipy'")
        exit()
        
    dados = carregar_e_limpar_dados(CSV_FILE)
    
    if dados is not None:
        resultados = gerar_analise(dados)
        
        # Opcional: Salvar resultados brutos da análise (para facilitar a escrita do relatório)
        with open('analise_resultados.json', 'w') as f:
            json.dump(resultados, f, indent=4)
        print("\nResultados da análise salvos em 'analise_resultados.json'.")