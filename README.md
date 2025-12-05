# Projeto Teste Técnico Data Services - Pmweb

## Projeto
Solução completa para integração e análise de dados contendo:
- Pipeline ETL automatizado
- Análises descritivas
- Diagrama DER
- Relatórios em CSV

## Como Executar
- python run.py

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)
- pandas 2.0.0+
- sqlite3

## Estrutura do Projeto

├── data/ # Arquivos CSV de entrada
├── src/ # Códigos fonte
│ ├── etl.py # Pipeline ETL principal
│ ├── database.py # Configuração do banco
│ ├── analises.py # Executa as queries e gera os relatórios
│ └── queries/ # Queries SQL
│   ├── pedidos_por_semestre.sql
│   ├── ticket_medio_cliente.sql
│   ├── intervalo_medio_compras.sql
│   ├── classificacao_clientes_tiers.sql
│   └── comparativos_segmentos_2019_2020.sql
├── output/ # Resultados
├── README.md # Documentação
└── run.py # Script de execução