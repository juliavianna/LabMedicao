# Relatório de Análise de Repositórios Populares (Versão 1.0)

## 1. Introdução

Este relatório apresenta a primeira etapa de um estudo sobre as características de sistemas open-source populares. O estudo baseia-se nos 1.000 repositórios com mais estrelas no GitHub e tem como objetivo investigar padrões de desenvolvimento, maturidade, frequência de atualizações e releases, e a linguagem de programação utilizada nesses projetos. Foram definidas pelos professores sete questões de pesquisa (RQs), e a seguir apresentamos as hipóteses informais sobre as possíveis respostas para elas.

## 2. Hipóteses Informais

**RQ 01. Sistemas populares são maduros/antigos?**
* **Métrica:** Idade do repositório (calculado a partir da data de sua criação) 
* **Hipótese:** Acreditamos que a maioria dos sistemas populares será relativamente antiga e madura, com pelo menos alguns anos de existência (2-5). A popularidade geralmente é construída ao longo do tempo, e projetos mais antigos tiveram mais oportunidade de crescer, acumular estrelas e atrair colaboradores.

**RQ 02. Sistemas populares recebem muita contribuição externa?**
* **Métrica:** Total de pull requests aceitas
* **Hipótese:** Esperamos que repositórios populares tenham um número muito alto de pull requests aceitas, pois a alta popularidade deve atrair muitas contribuições externas de comunidades de desenvolvimento.

**RQ 03. Sistemas populares lançam releases com frequência?**
* **Métrica:** Total de releases
* **Hipótese:** Nossa hipótese é que sistemas populares lançam releases com frequência, embora o total possa variar bastante. Projetos bem-sucedidos costumam ter um ciclo de desenvolvimento para entregar novas funcionalidades e correções de bugs aos usuários, o que é refletido no número de releases.

**RQ 04. Sistemas populares são atualizados com frequência?**
* **Métrica:** Tempo até a última atualização (calculado a partir da data de última atualização)
* **Hipótese:** Acreditamos que a grande maioria dos repositórios populares terá sido atualizada muito recentemente (dias ou poucas semanas atrás). A falta de atualização pode sinalizar que um projeto está abandonado, o que normalmente faria com que perdesse popularidade.

**RQ 05. Sistemas populares são escritos nas linguagens mais populares?**
* **Métrica:** Linguagem primária de cada um desses repositórios
* **Hipótese:** Acreditamos que linguagens como JavaScript, Python e TypeScript dominem a lista de linguagens primárias. A popularidade de um projeto está ligada à popularidade da linguagem, pois linguagens mais comuns têm comunidades maiores de desenvolvedores.

**RQ 06. Sistemas populares possuem um alto percentual de issues fechadas?**
* **Métrica:** Razão entre número de issues fechadas pelo total de issues 
* **Hipótese:** Nossa hipótese é que a razão de issues fechadas será alta, provavelmente acima de 80%. Projetos bem mantidos e com alta popularidade precisam gerenciar eficientemente seus problemas reportados para manter a qualidade e a confiança da comunidade.

**RQ 07. Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizadas com mais frequência?**
* **Métrica:** Razão entre resultados para os sistemas com as linguagens da reportagem com os resultados de sistemas em outras linguagens 
* **Hipótese:** Nossa hipótese é que os sistemas escritos em linguagens mais populares terão mais contribuições, releases e atualizações do que os desenvolvidos em linguagens menos populares

## 3. Metodologia

Para responder a estas questões, foi desenvolvido um script em Python que utiliza a API GraphQL do GitHub. O script consulta os 1.000 repositórios com o maior número de estrelas, coletando dados como data de criação, número de pull requests aceitas, total de releases, data da última atualização, linguagem primária e número de issues abertas e fechadas. A coleta foi realizada com paginação para garantir que todos os 1.000 repositórios fossem obtidos. Os dados foram salvos em um arquivo CSV para posterior análise.