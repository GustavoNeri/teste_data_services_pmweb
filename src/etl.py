import os
import pandas as pd
import sqlite3
from datetime import datetime
from src.database import get_connection, criar_banco

def log_rodada(tabela, qtd_incluido, qtd_alterado=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO LOG_DE_RODADAS (TABELA, QTD_ALTERADO, QTD_INCLUIDO)
        VALUES (?, ?, ?)
    ''', (tabela, qtd_incluido, qtd_alterado))
    conn.commit()
    conn.close()

def carregar_clientes():
    print("Carregando dados de clientes.")
    
    df = pd.read_csv('data/CADASTROS.csv', sep=';', encoding='latin1', engine='python', on_bad_lines='skip')
    
    mapeamento = {
        'ID': 'ID',
        'EMAIL': 'EMAIL', 
        'NOME': 'NOME',
        'DT_NASC': 'DATA_NASCIMENTO',
        'CIDADE': 'CIDADE',
        'ESTADO': 'UF',
        'RECEBE_EMAIL': 'PERMISSAO_RECEBE_EMAIL'
    }

    df_corrigido = pd.DataFrame()

    for col_orig, col_dest in mapeamento.items():
        if col_orig in df.columns:
            df_corrigido[col_dest] = df[col_orig]
            print(f"{col_orig} → {col_dest}")
        else:
            print(f"Coluna {col_orig} não encontrada no CSV")
            df_corrigido[col_dest] = None
    
    if 'PERMISSAO_RECEBE_EMAIL' in df_corrigido.columns:
        df_corrigido['PERMISSAO_RECEBE_EMAIL'] = df_corrigido['PERMISSAO_RECEBE_EMAIL'].fillna(0).astype(int)
    
    conn = get_connection()
    qtd_incluido = len(df_corrigido)

    df_corrigido.to_sql('CLIENTES', conn, if_exists='replace', index=False)

    conn.close()
    
    log_rodada('CLIENTES', qtd_incluido)
    print(f"{qtd_incluido} clientes carregados.")
    return qtd_incluido

def carregar_pedidos():
    print("Carregando dados de pedidos.")
    
    df = pd.read_csv('data/PEDIDOS.csv', sep=';', encoding='latin1', engine='python', on_bad_lines='skip')
    
    mapeamento = {
        'COD_CLIENTE': 'ID_CLIENTE',
        'COD_PEDIDO': 'ID_PEDIDO',
        'CODIGO_PRODUTO': 'ID_PRODUTO',
        'DEPTO': 'DEPARTAMENTO',
        'QUANTIDADE': 'QUANTIDADE',
        'VALOR_UNITARIO': 'VALOR_UNITARIO',
        'QTD_PARCELAS': 'PARCELAS',
        'DT_PEDIDO': 'DATA_PEDIDO',
        'MEIO_PAGTO': 'MEIO_PAGAMENTO',
        'STATUS_PAGAMENTO': 'STATUS_PAGAMENTO'
    }

    df_corrigido = pd.DataFrame()

    for col_orig, col_dest in mapeamento.items():
        if col_orig in df.columns:
            df_corrigido[col_dest] = df[col_orig]
            print(f"{col_orig} → {col_dest}")
        else:
            print(f"Coluna {col_orig} não encontrada no CSV")
            df_corrigido[col_dest] = None
    
    if 'QUANTIDADE' in df_corrigido.columns and 'VALOR_UNITARIO' in df_corrigido.columns:
        df_corrigido['VALOR_TOTAL'] = df_corrigido['QUANTIDADE'] * df_corrigido['VALOR_UNITARIO']
    
    if 'DATA_PEDIDO' in df_corrigido.columns:
        df_corrigido['DATA_PEDIDO'] = pd.to_datetime(df_corrigido['DATA_PEDIDO'])
    
    conn = get_connection()
    qtd_incluido = len(df_corrigido)

    df_corrigido.to_sql('PEDIDOS', conn, if_exists='replace', index=False)
    
    conn.close()
    
    log_rodada('PEDIDOS', qtd_incluido)
    print(f"{qtd_incluido} pedidos carregados.")
    return qtd_incluido

def executar_etl():
    print("Iniciando processo ETL.")
    print("-" * 50)
    
    criar_banco()
    
    qtd_clientes = carregar_clientes()
    qtd_pedidos = carregar_pedidos()
    
    print("-" * 50)
    print(f"ETL concluído com sucesso.")
    print(f"    - Clientes: {qtd_clientes}")
    print(f"    - Pedidos: {qtd_pedidos}")
    print(f"    - Banco: projeto.db")
    
    return True

if __name__ == "__main__":
    executar_etl()