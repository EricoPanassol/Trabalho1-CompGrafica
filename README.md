# Introdução

Este trabalho consiste em desenvolver, em OpenGL, um editor de curvas Bèzier.

O editor deve permitir a criação curvas através da informação de 3 pontos de controle das curvas.

Os comandos e modos do editor devem se ativados através de ícones exibidos na tela.

# MODOS DE CRIAÇÃO DE CURVAS

O editor deve suportar 3 modos de criação de curvas:

- **Modo sem continuidade:** a cada 3 pontos clicados, o programa deve gerar uma curva;

- **Modo com continuidade de posição:** a partir de uma curva já existente deve ser possível criar uma curva que mantenha continuidade de posição com o ponto final da última curva criada;

- **Modo com continuidade de derivada:** a partir de uma curva já existente deve ser possível criar uma curva que mantenha continuidade de derivada com o ponto final da última curva criada;

<!-- --- -->

Em todos os modos a criação a movimentação deve ser feita com a técnica de rubber-band aplicada às entidades visíveis (curvas e polígonos de controle). Um exemplo do uso desta técnica pode ser visto no vídeo a seguir.

![](/assets/ex.gif)

# A INTERFACE

A interface do programa deve ter, pelo as seguintes áreas:

- **área de desenho**, onde são exibidas as curvas;

- **área de ícones**, onde são exibidos os ícones;

- **área de status**, onde se informa qual o modo atual de operação da interface

# EDIÇÃO DE CURVAS

Durante a execução do programa deve ser possível realizar as seguintes operações:

- **Remoção de curvas:** Para remover uma curva o usuário deve clicar sobre uma das arestas do seu respectivo polígono de controle. Esta função só deve estar ativa se o polígono de controle estiver visível;

- **Movimentação de vértices:** deve ser possível mover um vértice de qualquer curva. Caso o vértice influencie a continuidade existente entre duas curvas, ambas devem ser alteradas conforme necessário. A movimentação deve ser feita com a técnica de rubber-band aplicada às entidades visíveis (curvas e polígonos de controle);

- **Conexão com uma curva já existente:** deve ser possível selecionar um vértice (inicial ou final de uma curva)_ e, a partir dele, iniciar uma nova curva. A forma de geração da nova curva dependerá do modo de continuidade que estiver ativo, no momento;

- **Atualização do modo de continuidade entre duas curvas:** clicando no vértice que conecta duas curvas, deve ser possível alterar o modo de continuidade entre duas curvas. Atente para as várias possibilidades de aumentar ou diminuir o grau de continuidade entre duas curvas. Uma posterior edição dos vértices destas curvas, deve respeitar o novo modo de continuidade entre as curvas.

# MODOS DE EXIBIÇÃO DAS CURVAS

Deve ser possível ligar e desligar a exibição das curvas e dos polígonos de controle.

Cada entidade exibida (polígonos, vértices e curvas) deve possuir uma cor diferente.

---

Entrega

Data de entrega no Moodle e apresentação: **18/04/2023**, até horário de início da aula.      

Para a entrega deverá ser criado um vídeo, de até 2 minutos, mostrando o funcionamento do programa e um relatório demonstrando que o trabalho atende aos requisitos da especificação e contendo o link para o vídeo.

Os trabalhos podem ser desenvolvidos em duplas. Os arquivos, contendo os programas-fontes do programa, devem ser compactados e submetidos pelo Moodle até a data e hora especificadas. **ENVIE APENAS ARQUIVOS .ZIP, ou seja, não envie 7z, rar, tar.gz, tgz, tar.bz2, etc.**

Poderá ser solicitada também a apresentação do trabalho de forma síncrona. Durante a apresentação será avaliado o domínio da resolução do problema, podendo inclusive ser possível invalidar o trabalho quando constatada a falta de conhecimento sobre o código implementado.

**A cópia parcial ou completa do trabalho terá como consequência a atribuição de nota ZERO ao trabalho dos alunos envolvidos.**

**FIM**