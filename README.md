# LabMedicao
Laboratório da matéria Medição e Experimentação em Engenharia de Software

# Coletor de Dados de Repositórios Populares do GitHub

Este script Python foi desenvolvido para coletar informações detalhadas de repositórios populares no GitHub, como parte de um estudo sobre as características de projetos open-source de sucesso. Ele utiliza a API GraphQL do GitHub para buscar dados de repositórios com mais de 1000 estrelas, com o objetivo de responder a uma série de questões de pesquisa sobre maturidade, frequência de contribuição, releases e outras métricas.

Este é o **Laboratório 1** do projeto e foca na coleta inicial de dados para 100 repositórios.

### Questões de Pesquisa (RQs)

O projeto visa responder às seguintes questões de pesquisa, usando as métricas extraídas pelo script:

  * **RQ 01**: Sistemas populares são maduros/antigos? (Métrica: idade do repositório)
  * **RQ 02**: Sistemas populares recebem muita contribuição externa? (Métrica: total de pull requests aceitas)
  * **RQ 03**: Sistemas populares lançam releases com frequência? (Métrica: total de releases)
  * **RQ 04**: Sistemas populares são atualizados com frequência? (Métrica: tempo até a última atualização)
  * **RQ 05**: Sistemas populares são escritos nas linguagens mais populares? (Métrica: linguagem primária)
  * **RQ 06**: Sistemas populares possuem um alto percentual de issues fechadas? (Métrica: razão entre issues fechadas e issues totais)

-----

### Como Usar

Para executar este script, você precisa de um **token de acesso pessoal** do GitHub.

#### Pré-requisitos

  * **Python 3.x**
  * **Bibliotecas Python**: `requests`
  * **Variável de Ambiente**: `GITHUB_TOKEN` configurada

#### 1\. Instalar a biblioteca `requests`

```bash
pip install requests
```

#### 2\. Obter um Token de Acesso Pessoal (PAT) do GitHub

1.  Acesse as **Settings** do seu perfil no GitHub.
2.  Navegue até **Developer settings** \> **Personal access tokens** \> **Tokens (classic)**.
3.  Clique em **Generate new token (classic)**.
4.  Dê um nome ao token (ex: `GraphQL_Collector`).
5.  Marque a permissão `repo` e `read:org` para ter acesso aos repositórios.
6.  Clique em **Generate token** e copie o valor.

#### 3\. Configurar a variável de ambiente

Exporte o token para a variável de ambiente `GITHUB_TOKEN`.

No **Linux/macOS**:

```bash
export GITHUB_TOKEN="seu_token_aqui"
```

No **Windows (CMD)**:

```bash
set GITHUB_TOKEN="seu_token_aqui"
```

#### 4\. Executar o script

Com a variável de ambiente configurada, você pode executar o script Python.

```bash
python seu_script.py
```

Ao final da execução, o script criará um arquivo chamado `lab01_data.json` contendo os dados dos 100 repositórios coletados.
