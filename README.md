# Conversão de CSV para JSON e Inserção de Dados no PostgreSQL com Monitoramento

Este repositório contém dois scripts Python que automatizam o processo de conversão de um arquivo CSV para um arquivo JSON e, em seguida, a atualização de um banco de dados PostgreSQL com os dados do arquivo JSON. Os scripts utilizam a biblioteca `watchdog` para monitorar mudanças no arquivo CSV e atualizar o banco de dados em tempo real quando o arquivo JSON é alterado.

## Scripts

### 1. Conversão de CSV para JSON com Monitoramento de Arquivo
O script "csv_to_json.py" monitora o arquivo `dados_ficticios.csv` para quaisquer modificações. Se o arquivo for modificado, o script converte os dados do CSV para JSON e os salva como `dados_ficticios.json`.

#### Funcionalidades:
- **Monitoramento de Arquivo:** Utiliza a biblioteca `watchdog` para observar alterações no arquivo CSV.
- **Conversão de CSV para JSON:** Converte os dados do CSV para JSON com o manejo adequado de codificação.
- **Tratamento de Erros:** Inclui tratamento de erros para problemas comuns, como erros de formato de arquivo, dados vazios ou problemas de permissão.

#### Como Funciona:
- O script monitora o diretório atual em busca de mudanças no arquivo `dados_ficticios.csv`.
- Quando o arquivo é modificado, ele lê o arquivo CSV, detecta a codificação e converte os dados para o formato JSON.
- O arquivo JSON é salvo com a formatação adequada (com espaçamento).

### 2. Atualização do Banco de Dados PostgreSQL a partir do JSON
O script "main.py" verifica mudanças no arquivo `dados_ficticios.json` e atualiza um banco de dados PostgreSQL com os novos dados. Ele insere os dados em uma tabela chamada `clients`.

#### Funcionalidades:
- **Integração com PostgreSQL:** Insere dados no banco de dados PostgreSQL.
- **Criação da Tabela no Banco:** Cria automaticamente a tabela `clients` caso ela não exista.
- **Monitoramento de Arquivo:** Verifica alterações no arquivo JSON a cada 10 segundos e atualiza o banco de dados conforme necessário.
- **Tratamento de Erros:** Trata erros comuns durante a inserção de dados.

#### Como Funciona:
- O script monitora o arquivo `dados_ficticios.json` em busca de alterações.
- Quando uma alteração é detectada, ele lê o arquivo JSON e insere os dados na tabela `clients` no banco de dados PostgreSQL.
- Se a tabela não existir, ela será criada automaticamente.

## Requisitos

- Python 3.12.1
- PostgreSQL
- Bibliotecas necessárias: 

 - psycopg2 
 - pandas
 - chardet 
 - watchdog

Para instalar as bibliotecas necessárias, execute:
```bash
pip install psycopg2 pandas chardet watchdog
