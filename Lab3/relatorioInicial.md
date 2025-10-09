# Relatório Preliminar (Lab 03) - Rascunho Inicial com Hipóteses

## 1. Introdução

A prática de code review tornou-se uma constante nos processos de desenvolvimento ágeis. Em essência, consiste na interação entre desenvolvedores e revisores para inspecionar o código produzido antes de integrá-lo à base principal, visando garantir a qualidade e evitar a inclusão de defeitos.

No contexto do GitHub, essas atividades de code review ocorrem a partir da avaliação de Pull Requests (PRs). Ao final desse processo, a solicitação de merge pode ser aprovada ou rejeitada pelo revisor.

O objetivo deste laboratório é analisar a atividade de code review em repositórios populares do GitHub, identificando variáveis que influenciam o resultado final (merge) de um PR, sob a perspectiva de desenvolvedores.

## 2. Questões de Pesquisa e Hipóteses Informais

As hipóteses informais a seguir são elaboradas com base nas Questões de Pesquisa (RQs) e Métricas definidas na metodologia do laboratório.

### A. Dimensão: Feedback Final das Revisões (Status do PR)

(A variável dependente é o status final: MERGED ou CLOSED)

| RQ | Métrica (Variável Independente) | Hipótese Informal (Correlação Esperada) |
| :---: | :--- | :--- |
| *RQ 01* | Tamanho (Arquivos / Linhas Adicionadas/Removidas) | PRs menores têm *maior chance de serem MERGED*, pois representam um risco menor e exigem menos esforço de revisão. |
| *RQ 02* | Tempo de Análise (Intervalo Criação/Fechamento) | PRs que levam muito tempo para serem analisados têm *maior chance de serem CLOSED* (rejeitados ou abandonados), pois refletem dificuldade ou desinteresse do revisor. |
| *RQ 03* | Descrição (Número de caracteres do corpo) | PRs com descrições mais longas e claras têm *maior chance de serem MERGED*, pois fornecem o contexto necessário para a revisão. |
| *RQ 04* | Interações (Participantes / Comentários) | Um alto número de interações (participantes e/ou comentários) pode indicar controvérsia ou problemas no PR, correlacionando-se *positivamente com o status CLOSED*. |

### B. Dimensão: Número de Revisões

(A variável dependente é o número total de revisões realizadas)

| RQ | Métrica (Variável Independente) | Hipótese Informal (Correlação Esperada) |
| :---: | :--- | :--- |
| *RQ 05* | Tamanho (Arquivos / Linhas Adicionadas/Removidas) | PRs maiores (mais código) exigirão um *Número de Revisões maior* para garantir a qualidade e a cobertura da inspeção. |
| *RQ 06* | Tempo de Análise (Intervalo Criação/Fechamento) | Quanto mais tempo um PR leva para ser analisado, maior o *Número de Revisões, refletindo o tempo necessário para o ciclo de *feedback e correção. |
| *RQ 07* | Descrição (Número de caracteres do corpo) | Descrições claras reduzem as dúvidas e o ruído, correlacionando-se *negativamente* com o Número de Revisões (descrições melhores = menos idas e vindas). |
| *RQ 08* | Interações (Participantes / Comentários) | Mais interações (comentários) estão diretamente associadas a um *Número de Revisões maior, pois a métrica de interações é uma proxy para o volume de *feedback e discussão. |