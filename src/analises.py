import os
import pandas as pd
import sqlite3
from src.database import get_connection


def carregar_query(nome_arquivo):
    caminho = os.path.join('src', 'queries', nome_arquivo)
    try:
        with open(caminho, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return None


def executar_query_salvar_csv(nome_query, nome_arquivo_saida, conn):
    print(f"\n Executando: {nome_query}")
    
    query = carregar_query(nome_query)
    if query is None:
        return False
    
    df = pd.read_sql_query(query, conn)
    
    caminho_saida = os.path.join('output', 'relatorios', nome_arquivo_saida)
    df.to_csv(caminho_saida, index=False, encoding='utf-8')
    
    # Pré visualização
    print(f"Resultados: {len(df)} linhas")
    print(f"Salvo em: {caminho_saida}")
    
    if not df.empty:
        print(f"Pré visualização (5 primeiras linhas):")
        print(df.head().to_string(index=False))
    
    print("-" * 50)
    return True


def gerar_analises():
    print("\n Gerando anàlises pelas queries SQL")
    print("=" * 60)
    
    conn = get_connection()
    
    # nome_arquivo_query.sql -> nome_arquivo_saida.csv
    queries = {
        '01_pedidos_por_semestre.sql': '01_pedidos_por_semestre.csv',
        '02_ticket_medio_cliente.sql': '02_ticket_medio_cliente.csv',
        '03_intervalo_medio_compras.sql': '03_intervalo_medio_entre_compras.csv',
        '04_classificacao_clientes_tiers.sql': '04_classificacao_clientes_tiers.csv',
        '05_comparativos_segmentos_2019_2020.sql': '05_comparativos_segmentos_2019_2020.csv',
        '06_faixa_etaria_clientes.sql': '06_faixa_etaria_clientes.csv',
        '07_localizacao_geografica_clientes.sql': '07_localizacao_geografica_clientes.csv',
        '08_pedidos_por_dia_da_semana.sql': '08_pedidos_por_dia_da_semana.csv',
        '09_clientes_pagamento_pendente.sql': '09_clientes_pagamento_pendente.csv'
    }
    
    resultados = []
    for query_arquivo, saida_arquivo in queries.items():
        sucesso = executar_query_salvar_csv(query_arquivo, saida_arquivo, conn)
        resultados.append((query_arquivo, sucesso))
    
    conn.close()
    
    print("\n Resumo das análises geradas:")
    print("=" * 60)
    for query, sucesso in resultados:
        status = "Sucesso" if sucesso else "Falha"
        print(f"   {query}: {status}")
    
    return all([r[1] for r in resultados])

def criar_der():
    print("\n Diagrama DER (Entidade-Relacionamento):")
    print("=" * 60)
    
    der = """
    ┌────────────────────────┐       ┌──────────────────┐
    │    CLIENTES            │       │     PEDIDOS      │
    ├────────────────────────┤       ├──────────────────┤
    │ ID (PK)                │1    N │ ID_PEDIDO        │
    │ EMAIL                  │◄─────►│ ID_CLIENTE (FK)  │
    │ NOME                   │       │ ID_PRODUTO       │
    │ DATA_NASCIMENTO        │       │ DEPARTAMENTO     │
    | CIDADE                 │       │ QUANTIDADE       │
    │ UF                     │       │ VALOR_UNITARIO   │
    │ PERMISSAO_RECEBE_EMAIL │       │ PARCELAS         │
    └────────────────────────┘       │ DATA_PEDIDO      │
                                     │ MEIO_PAGAMENTO   │
                                     │ STATUS_PAGAMENTO │
                                     │ VALOR_TOTAL      │
    ┌─────────────────┐              └──────────────────┘
    │ LOG_DE_RODADAS  │       
    ├─────────────────┤       
    │ ID_RODADA (PK)  │
    │ DATA_RODADA     │
    │ TABELA          │
    │ QTD_ALTERADO    │
    │ QTD_INCLUIDO    │
    └─────────────────┘
    
    RELACIONAMENTOS:
    • Um CLIENTE pode ter vários PEDIDOS (1:N)
    • Cada PEDIDO pertence a um único CLIENTE
    • LOG_DE_RODADAS registra todas as operações ETL
    """
    
    print(der)
    
    # Salvar DER em arquivo
    caminho_der = os.path.join('output', 'der.txt')
    with open(caminho_der, 'w', encoding='utf-8') as f:
        f.write(der)
    
    print(f"\n DER salvo em: {caminho_der}")
    return True

def criar_relatorio_consolidado():
    print("\n Criando relatório consolidado...")
    
    relatorio = f"""# Relatório de análises - Teste Técnico Data Services - Pmweb

Data de geração: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}

## Arquivos Gerados

1. **Pedidos por Semestre** (`01_pedidos_por_semestre.csv`)
   - Quantidade de pedidos parcelados por cliente, agrupados por semestre

2. **Ticket Médio** (`02_ticket_medio_cliente.csv`)
   - Valor médio gasto por cliente, agrupado por mês e ano

3. **Intervalo entre Compras** (`03_intervalo_medio_entre_compras.csv`)
   - Tempo médio (em dias) entre compras de cada cliente

4. **Classificação em Tiers** (`04_classificacao_clientes_tiers.csv`)
   - Categorização mensal dos clientes (Básico, Prata, Ouro, Super)

5. **Comparativo por Segmento** (`05_comparativos_segmentos_2019_2020.csv`)
   - Variação percentual de vendas entre 2019 e 2020 (Som e Papelaria)

6. **Classificação em Faixa Etária** (`06_faixa_etaria_clientes.csv`)
   - Comportamento de compra por faixa etária dos clientes

7. **Localização Geográfica** (`07_localizacao_geografica_clientes.csv`)
   - Analisar as vendas por localização geográfica dos clientes

8. **Sazonalidade por dia da semana** (`08_pedidos_por_dia_da_semana.csv`)
   - Identificar a sazonalidade de vendas por dia da semana

9. **Clientes com pagamento não confirmado** (`09_clientes_pagamento_pendente.csv`)
   - Insight para campanhas de remarketing para clientes

## Tecnologias Utilizadas

- **Linguagem**: Python 3.8+
- **Banco de Dados**: SQLite
- **Bibliotecas**: pandas, sqlite3, pygwalker
- **Estrutura**: Arquitetura modular com queries SQL separadas

## Métricas do Projeto

- Queries SQL: 9
- Tabelas criadas: 3 (CLIENTES, PEDIDOS, LOG_DE_RODADAS)
- Relatórios gerados: 9 arquivos CSV
- Visualização das análises: DASHBOARD interativo com biblioteca pygwalker
- Logs: Sistema completo de logs

## Insights

1. **Comportamento de Compra**: Identificar clientes frequentes vs. ocasionais
2. **Sazonalidade por período do ano**: Padrões de compra por período do ano
3. **Segmentação**: Clientes por valor gasto (tiers)
4. **Performance**: Evolução das vendas por segmento
5. **Pagamento**: Análise de preferência por parcelamento
6. **Faixa Etária**: Comportamento de compra por faixa etária 
7. **Localização**: Identifica localização geográfica do clientes
8. **Sazonalidade por dia da semana**: Padrões de compra por dias da semana
9. **Campanhas de Remarketing**: Classifica clientes com pagamento não confirmado que podem receber e-mails
"""
    
    caminho_relatorio = os.path.join('output', 'relatorios', 'RELATORIO.md')
    with open(caminho_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"Relatório consolidado salvo em: {caminho_relatorio}")
    return True

if __name__ == "__main__":
    gerar_analises()
    criar_der()
    criar_relatorio_consolidado()