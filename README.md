# LabMedicao

Laboratório da matéria Medição e Experimentação em Engenharia de Software

# Coletor e Analisador de Dados de Repositórios Populares do GitHub

Este projeto foi desenvolvido para coletar e analisar informações detalhadas de repositórios populares no GitHub, como parte de um estudo sobre as características de projetos open-source de sucesso. Ele utiliza a **API GraphQL do GitHub** para buscar dados de repositórios com mais de 1000 estrelas, com o objetivo de responder a uma série de **questões de pesquisa (RQs)** relacionadas a maturidade, contribuições externas, releases, atualizações e popularidade das linguagens.

---

## 📌 Roadmap do Projeto

* ✅ **Lab01S01** → Coleta inicial de dados para 100 repositórios, utilizando consulta GraphQL.
* ✅ **Lab01S02** → Implementação da paginação para coletar **1000 repositórios**, exportação em **.csv** e elaboração da **primeira versão do relatório com hipóteses informais**.
* ⏳ **Lab01S03** → Análise, visualização de dados e relatório final.

---

## Questões de Pesquisa (RQs)

O projeto visa responder às seguintes questões de pesquisa, usando as métricas extraídas pelo script:

* **RQ 01**: Sistemas populares são maduros/antigos?

  * *Métrica*: idade do repositório.
* **RQ 02**: Sistemas populares recebem muita contribuição externa?

  * *Métrica*: total de pull requests aceitas.
* **RQ 03**: Sistemas populares lançam releases com frequência?

  * *Métrica*: total de releases.
* **RQ 04**: Sistemas populares são atualizados com frequência?

  * *Métrica*: tempo até a última atualização.
* **RQ 05**: Sistemas populares são escritos nas linguagens mais populares?

  * *Métrica*: linguagem primária.
* **RQ 06**: Sistemas populares possuem um alto percentual de issues fechadas?

  * *Métrica*: razão entre issues fechadas e issues totais.
* **RQ 07 (Bônus)**: Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?

---

## 🔧 Como Usar

### Pré-requisitos

* **Python 3.x**
* **Bibliotecas Python**: `requests`, `csv` (padrão do Python), `pandas`
* **Variável de Ambiente**: `GITHUB_TOKEN` configurada

### 1. Instalar a biblioteca necessária

```bash
pip install requests
```

### 2. Obter um Token de Acesso Pessoal (PAT) do GitHub

1. Vá em **Settings** no seu perfil GitHub.
2. Acesse **Developer settings > Personal access tokens > Tokens (classic)**.
3. Clique em **Generate new token (classic)**.
4. Dê um nome ao token (ex: `GraphQL_Collector`).
5. Marque a permissão `repo` e `read:org`.
6. Gere o token e copie o valor.

### 3. Configurar a variável de ambiente

**Linux/macOS**:

```bash
export GITHUB_TOKEN="seu_token_aqui"
```

**Windows (CMD)**:

```bash
set GITHUB_TOKEN="seu_token_aqui"
```

### 4. Executar o script

Para rodar o script principal:

```bash
python lab01_coleta.py
```
### 3. Executar o código de análise para obter as respostas
1. Instalar a biblioteca pandas

```bash
pip install pandas
```
2. Navegar até a pasta Lab01S02 e rodar no terminal

```bash
python lab01_analise.py
```

---

Ao final da execução:

* No **Lab01S01**, é gerado o arquivo `lab01_data.json` com os dados de 100 repositórios.
* No **Lab01S02**, é gerado o arquivo `lab01_data.csv` com os dados de 1000 repositórios e o **relatório inicial** com hipóteses informais.
* No **Lab01S03** (em andamento), serão feitas análises estatísticas, visualizações gráficas e a elaboração do **relatório final**.

