import os
import pandas as pd
import sqlite3
from datetime import datetime
from src.database import get_connection, criar_banco

def log_rodada(tabela, qtd_incluido, qtd_alterado=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO LOG_DE_RODADAS (TABELA, QTD_INCLUIDO, QTD_ALTERADO)
        VALUES (?, ?, ?)
    ''', (tabela, qtd_incluido, qtd_alterado))
    conn.commit()
    conn.close()

def carregar_clientes():
    print("Carregando dados de clientes.")
    
    df = pd.read_csv('data/CADASTROS.csv', sep=';', encoding='latin1', engine='python', on_bad_lines='skip')
    
    df.columns = [col.upper() for col in df.columns]
    
    if 'PERMISSAO_RECEBE_EMAIL' in df.columns:
        df['PERMISSAO_RECEBE_EMAIL'] = df['PERMISSAO_RECEBE_EMAIL'].astype(int)
    
    conn = get_connection()
    qtd_incluido = len(df)
    df.to_sql('CLIENTES', conn, if_exists='replace', index=False)
    conn.close()
    
    log_rodada('CLIENTES', qtd_incluido)
    print(f"{qtd_incluido} clientes carregados.")
    return qtd_incluido

def carregar_pedidos():
    print("Carregando dados de pedidos.")
    
    df = pd.read_csv('data/PEDIDOS.csv', sep=';', encoding='latin1', engine='python', on_bad_lines='skip')
    
    df.columns = [col.upper() for col in df.columns]
    
    df['VALOR_TOTAL'] = df['QUANTIDADE'] * df['VALOR_UNITARIO']
    
    if 'DATA_PEDIDO' in df.columns:
        df['DATA_PEDIDO'] = pd.to_datetime(df['DATA_PEDIDO'])
    
    conn = get_connection()
    qtd_incluido = len(df)
    df.to_sql('PEDIDOS', conn, if_exists='replace', index=False)
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