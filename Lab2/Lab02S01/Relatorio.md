# Relatório Final do Laboratório 02: Um Estudo Sobre as Características de Qualidade de Sistemas Java

*Autores:* Julia Vidal e Leandra Ramos  
*Data:* 18 de setembro de 2025  

## 1. Introdução

A popularidade e a complexidade de projetos de software de código aberto têm crescido exponencialmente. Entender a relação entre as características externas de um projeto (como sua popularidade, idade e tamanho) e sua qualidade de código interna é fundamental para a engenharia de software. Este estudo visa investigar empiricamente essas relações, analisando os 1.000 repositórios Java mais populares da plataforma GitHub.

Para guiar esta investigação, foram definidas as seguintes Questões de Pesquisa (RQs):

- *RQ 01.* Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
- *RQ 02.* Qual a relação entre a maturidade do repositórios e as suas características de qualidade?
- *RQ 03.* Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- *RQ 04.* Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

### Hipóteses Iniciais

Antes da coleta e análise dos dados, foram formuladas as seguintes hipóteses para cada questão de pesquisa:

- *Hipótese para RQ01 (Popularidade):* Repositórios mais populares (medidos por estrelas) tendem a apresentar *melhor qualidade* de código (menores valores de CBO e LCOM), devido a uma maior revisão por pares e contribuição da comunidade.
- *Hipótese para RQ02 (Maturidade):* Repositórios mais maduros (mais antigos) tendem a ter *melhor qualidade*, pois tiveram mais tempo para processos de refatoração, correção de bugs e estabilização da arquitetura.
- *Hipótese para RQ03 (Atividade):* Repositórios mais ativos (medidos pelo número de releases) tendem a ter uma *qualidade ligeiramente inferior*, pois o foco na entrega contínua de novas funcionalidades pode levar a um aumento do débito técnico.
- *Hipótese para RQ04 (Tamanho):* Repositórios maiores (medidos por linhas de código ou tamanho em KB) tendem a apresentar *pior qualidade* (maiores valores de CBO e LCOM), devido ao aumento da complexidade inerente a sistemas de grande escala.

## 2. Metodologia

O processo metodológico foi dividido em duas etapas principais: coleta de dados e análise estatística.

### Coleta de Dados

1. **Seleção da Amostra:** Foram selecionados os 1.000 repositórios com o maior número de estrelas e linguagem primária Java, utilizando a API de busca do GitHub.  
2. **Extração de Métricas de Processo (Variáveis Independentes):** Para cada repositório, as seguintes métricas foram coletadas via API do GitHub:  
   - *Popularidade:* O número de estrelas (`stargazers_count`).  
   - *Maturidade:* A idade do repositório, calculada a partir da data de criação (`created_at`).  
   - *Atividade:* A contagem total de releases, obtida através do endpoint `/releases`.  
   - *Tamanho:* O tamanho do repositório em kilobytes (`size`), utilizado como uma aproximação para as linhas de código.  
3. **Extração de Métricas de Qualidade (Variáveis Dependentes):** A qualidade interna do código foi medida utilizando a ferramenta de análise estática CK (`ck.jar`). Para cada repositório, as seguintes métricas foram extraídas:  
   - *CBO (Coupling Between Objects):* Acoplamento entre objetos.  
   - *DIT (Depth of Inheritance Tree):* Profundidade da árvore de herança.  
   - *LCOM (Lack of Cohesion in Methods):* Falta de coesão nos métodos.  

### Processo de Análise

Um script em Python foi desenvolvido para automatizar o processo. Para cada repositório, o script:  

1. Clona o repositório (`git clone`).  
2. Identifica o diretório de código-fonte mais provável, buscando prioritariamente por pastas que terminam em `src/main/java` ou, como alternativa, a pasta com a maior concentração de arquivos `.java`.  
3. Executa a ferramenta CK sobre o diretório encontrado.  
4. Lê o arquivo de saída `class.csv` e, como as métricas são por classe, calcula a *mediana*, a *média* e o *desvio padrão* de CBO, DIT e LCOM para agregar os valores por repositório.  
5. Consolida todas as métricas em um único arquivo CSV para a análise final.  

Para responder às RQs, foram utilizados gráficos de dispersão para visualização e o coeficiente de correlação de Spearman para quantificar a força e a direção da relação entre as variáveis.

## 3. Resultados

Nesta seção, são apresentados os resultados da análise estatística para cada questão de pesquisa.

### Resultados para RQ01: Popularidade vs. Qualidade


### Resultados para RQ02: Maturidade vs. Qualidade


### Resultados para RQ03: Atividade vs. Qualidade


### Resultados para RQ04: Tamanho vs. Qualidade


## 4. Discussão

Esta seção interpreta os resultados apresentados, comparando-os com as hipóteses iniciais.

### Discussão sobre a RQ01 (Popularidade)


### Discussão sobre a RQ02 (Maturidade)


### Discussão sobre a RQ03 (Atividade)


### Discussão sobre a RQ04 (Tamanho)


## 5. Conclusão


### Limitações do Estudo

### Trabalhos Futuros
