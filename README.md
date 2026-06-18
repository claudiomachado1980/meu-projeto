# Sistema de Gestão de Imobilizado Escolar

Este projeto foi desenvolvido em Python e tem como objetivo criar um sistema simples de gestão de imobilizado escolar.

O sistema permite registar, consultar, alterar, remover e importar bens de uma escola, mantendo os dados guardados num ficheiro de texto.

Cada bem é tratado de forma individual.
Ou seja, cada computador, cadeira, mesa, projetor ou outro equipamento tem o seu próprio ID.

---

## Objetivo do projeto

O objetivo principal é permitir o registo e controlo de bens existentes numa escola, de forma simples e organizada.

O sistema permite:

* Registar novos bens
* Pesquisar bens por ID ou nome
* Listar todo o inventário
* Listar bens por localização
* Alterar o estado de um bem
* Alterar a localização de um bem
* Remover bens do inventário
* Guardar os dados num ficheiro de texto
* Gerar relatórios simples
* Exportar relatório para ficheiro TXT
* Importar bens a partir de ficheiros externos
* Importar ficheiros com colunas diferentes através de mapeamento flexível
* Validar o formato dos IDs dos bens

---

## Versão atual

A versão atual do projeto é a **V3 - Importação flexível com validação de ID**.

O sistema funciona através do terminal, usando um menu simples.

Os dados são guardados no ficheiro `inventario.txt`, permitindo que a informação continue disponível mesmo depois de fechar o programa.

---

## Evolução do projeto

O projeto foi desenvolvido por fases.

### V1 - Gestão base do inventário

Na primeira versão foi criada a base do sistema.

Funcionalidades principais:

* Registar bens
* Pesquisar bens
* Listar inventário
* Listar bens por localização
* Alterar estado
* Alterar localização
* Remover bens
* Guardar e carregar dados através de ficheiro TXT

### V2 - Relatórios simples

Na segunda versão foram adicionados relatórios ao sistema.

Funcionalidades adicionadas:

* Relatório geral do inventário
* Relatório por categoria
* Relatório por estado
* Relatório por localização
* Exportação de relatório para ficheiro TXT

Os relatórios exportados são guardados na pasta:

```text
relatorios_exportados/
```

### V3 - Importação flexível

Na terceira versão foi adicionada a importação de bens a partir de ficheiros externos.

Existem duas formas de importação:

#### Importação simples

Nesta opção, o ficheiro externo deve seguir exatamente a estrutura usada pelo sistema:

```text
id;nome;categoria;estado;localizacao
```

Exemplo:

```text
COM0001;Computador;Equipamento Informático;Bom;Sala 1
```

#### Importação flexível

Nesta opção, o ficheiro pode ter nomes de colunas diferentes.

Exemplo:

```text
codigo;descricao;sala;situacao
PC001;Computador HP;Sala TIC;Bom
```

O sistema mostra as colunas encontradas e pede ao utilizador para indicar quais correspondem aos campos principais do inventário:

* ID
* Nome
* Categoria
* Estado
* Localização

Se algum campo não existir no ficheiro, o sistema tenta resolver da seguinte forma:

* Se não existir ID, gera automaticamente um novo ID
* Se o ID existir mas estiver fora do formato correto, gera automaticamente um novo ID válido
* Se não existir categoria, tenta descobrir através do nome ou usa `Outro`
* Se não existir estado, pede um estado padrão ao utilizador
* Se não existir localização, pede uma localização padrão ao utilizador

As colunas que não forem necessárias são ignoradas nesta versão.

---

## Estrutura do projeto

O projeto foi construído de forma gradual, seguindo uma ordem lógica.

### 1. produtos.py

Este foi o primeiro ficheiro criado.

Neste ficheiro foram definidos os elementos base do sistema:

* Categorias iniciais dos bens
* Estados possíveis dos bens
* Localizações da escola
* Tipos de bens iniciais
* Radicais usados nos IDs
* Funções base para criar, mostrar, guardar e ler bens

Este ficheiro serve como base estrutural do projeto.

### 2. gestao.py

Este ficheiro contém a lógica principal de gestão do inventário.

Inclui funções para:

* Carregar dados do ficheiro
* Guardar dados no ficheiro
* Gerar IDs automaticamente
* Registar bens
* Pesquisar bens
* Listar inventário
* Listar bens por localização
* Alterar estado de um bem
* Alterar localização de um bem
* Remover bens
* Disponibilizar a lista de bens para os relatórios e importações

### 3. relatorios.py

Este ficheiro foi criado na V2.

Contém as funções responsáveis pelos relatórios do sistema.

Inclui:

* Relatório geral
* Relatório por categoria
* Relatório por estado
* Relatório por localização
* Exportação de relatório para TXT

### 4. importacao.py

Este ficheiro foi criado para tratar da importação de bens a partir de ficheiros externos.

Inclui:

* Importação simples
* Importação flexível
* Leitura de ficheiros externos
* Deteção de separador
* Mapeamento de colunas
* Geração automática de ID quando necessário
* Tratamento de campos em falta
* Resumo da importação

### 5. validacoes.py

Este ficheiro contém validações gerais usadas pelo sistema.

Nesta fase, inclui a validação do formato do ID.

O formato obrigatório do ID é:

```text
3 letras + 4 números
```

Exemplos válidos:

```text
COM0001
MSA0001
PRJ0001
```

Exemplos inválidos:

```text
PCF001
CADF001
123ABC1
COM01
```

### 6. main.py

Este é o ficheiro principal do programa.

É neste ficheiro que está o menu apresentado ao utilizador.

O utilizador deve executar este ficheiro para usar o sistema.

---

## Pastas do projeto

O projeto também contém algumas pastas auxiliares.

### exemplos/

Esta pasta contém ficheiros de exemplo usados para testar as importações.

Exemplos:

```text
exemplos/importar_teste.txt
exemplos/teste_flexivel.txt
exemplos/teste_ids_invalidos.txt
```

Estes ficheiros ajudam a demonstrar como funciona a importação simples e a importação flexível.

### relatorios_exportados/

Esta pasta é usada para guardar os relatórios exportados pelo sistema.

Exemplo:

```text
relatorios_exportados/relatorio_inventario.txt
```

---

## Campos usados pelo sistema

Cada bem tem os seguintes campos:

* ID
* Nome
* Categoria
* Estado
* Localização

Nesta versão ainda não são usados:

* Quantidade
* Valor monetário

Esta decisão foi tomada porque, nesta fase, cada bem é tratado de forma individual.

---

## ID automático

O ID é gerado automaticamente com base no tipo de bem.

Exemplos:

* Computador -> COM0001
* Mesa Aluno -> MSA0001
* Projetor -> PRJ0001
* Impressora -> IMP0001

O formato obrigatório do ID é:

```text
3 letras + 4 números
```

Exemplo:

```text
COM0001
```

O ID é importante porque permite identificar cada bem de forma única, mesmo quando existem vários bens com o mesmo nome.

Por exemplo:

```text
COM0001 - Computador - Sala 1
COM0002 - Computador - Sala 2
COM0003 - Computador - Biblioteca
```

Durante a importação flexível, se o ficheiro externo trouxer um ID fora deste formato, o sistema gera automaticamente um novo ID válido.

---

## Persistência dos dados

Os dados são guardados no ficheiro:

```text
inventario.txt
```

Quando o programa começa, os dados são carregados desse ficheiro.

Sempre que o inventário é alterado, os dados são guardados novamente.

Isto permite que os dados continuem disponíveis mesmo depois de fechar e voltar a abrir o programa.

---

## Como executar o programa

No terminal, dentro da pasta do projeto, executar:

```bash
python main.py
```

---

## Menu principal

O programa apresenta o seguinte menu:

```text
1. Registar novo bem
2. Pesquisar bem
3. Listar inventário completo
4. Listar bens por localização
5. Alterar estado de um bem
6. Alterar localização de um bem
7. Remover bem
8. Relatório geral
9. Relatório por categoria
10. Relatório por estado
11. Relatório por localização
12. Exportar relatório para TXT
13. Importar bens de ficheiro externo
14. Importar bens com mapeamento flexível
0. Guardar e sair
```

---

## Explicação geral da lógica

O projeto foi construído por etapas.

Primeiro foi criado o ficheiro `produtos.py`, onde se definiu a estrutura de um bem e os dados base do sistema.

Depois foi criado o ficheiro `gestao.py`, onde se implementou a lógica de gestão dos bens, incluindo o registo, pesquisa, listagem, alteração e remoção.

Na V2 foi criado o ficheiro `relatorios.py`, responsável pelos relatórios simples do inventário.

Na V3 foi criado o ficheiro `importacao.py`, responsável pela importação de dados externos, e o ficheiro `validacoes.py`, responsável por regras de validação do sistema.

Por fim, o ficheiro `main.py` centraliza o menu principal e chama as funções necessárias.

Esta organização permite separar melhor o projeto:

* `produtos.py` define a estrutura dos bens
* `gestao.py` trata da lógica de gestão
* `relatorios.py` trata dos relatórios
* `importacao.py` trata das importações
* `validacoes.py` trata das validações
* `main.py` trata da interação com o utilizador

---

## Onde estão as principais funcionalidades no código

Esta secção serve para identificar rapidamente onde se encontra cada parte importante do sistema.

- Estrutura base dos bens, categorias, estados, localizações e tipos:
  - `produtos.py`

- Registo, pesquisa, listagem, alteração e remoção de bens:
  - `gestao.py`

- Menu principal apresentado ao utilizador:
  - `main.py`

- Relatórios simples:
  - `relatorios.py`

- Importação simples de ficheiros externos:
  - `importacao.py`
  - função `importar_bens_de_ficheiro()`

- Importação flexível com mapeamento de colunas:
  - `importacao.py`
  - função `importar_bens_flexivel()`

- Escolha/mapeamento das colunas do ficheiro externo:
  - `importacao.py`
  - função `_escolher_coluna()`

- Geração automática de ID:
  - `importacao.py`
  - funções `_obter_radical_pelo_nome()` e `_gerar_id_automatico()`

- Validação do formato do ID:
  - `validacoes.py`
  - função `validar_formato_id()`

---

## Possíveis melhorias futuras

O projeto poderá evoluir com novas funcionalidades, como:

* Interface gráfica
* Exportação para CSV ou Excel
* Exportação para PDF
* Melhor apresentação dos dados
* Filtros mais avançados
* Validação completa do inventário atual
* Alteração de mais campos dos bens
* Impressão de etiquetas
* Associação de código de barras ou QR Code a cada bem
* Sistema mais configurável para diferentes espaços físicos
* Possibilidade de guardar campos adicionais vindos dos ficheiros externos

---

## Código de barras ou QR Code

Numa versão futura, poderá ser adicionada a possibilidade de associar uma etiqueta a cada bem.

Essa etiqueta poderia conter o ID do bem.

Exemplo:

```text
COM0001
```

Para bens maiores, como computadores, projetores, mesas ou impressoras, poderá fazer sentido usar uma etiqueta com código de barras ou QR Code.

Para bens muito pequenos, como canetas ou lápis, poderá ser mais difícil colocar uma etiqueta individual, devido ao espaço reduzido.

Nesse caso, poderá ser necessário avaliar se esses bens devem ser tratados individualmente ou agrupados de outra forma numa versão futura.

O código de barras poderá ser útil quando se pretende guardar apenas o ID do bem.

O QR Code poderá ser útil se, no futuro, o sistema tiver uma ficha digital com mais informação sobre cada bem.

---

## Observações finais

O objetivo inicial foi criar uma base simples, funcional e bem organizada.

Com a evolução até à V3, o sistema já permite não só gerir bens individuais, mas também gerar relatórios e importar dados externos de forma mais flexível.

A estrutura criada permite que o projeto seja melhorado no futuro, sem alterar a lógica base já implementada.
