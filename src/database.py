import os
import sqlite3
import pandas as pd

def criar_banco():
    conn = sqlite3.connect('projeto.db')
    
    # Tabela CLIENTES
    conn.execute('''
    CREATE TABLE IF NOT EXISTS CLIENTES (
        ID INTEGER PRIMARY KEY,
        EMAIL TEXT,
        NOME TEXT,
        DATA_NASCIMENTO TEXT,
        CIDADE TEXT,
        UF TEXT,
        PERMISSAO_RECEBE_EMAIL INTEGER
    )
    ''')
    
    # Tabela PEDIDOS
    conn.execute('''
    CREATE TABLE IF NOT EXISTS PEDIDOS (
        ID_PEDIDO INTEGER,
        ID_CLIENTE INTEGER,
        ID_PRODUTO INTEGER,
        DEPARTAMENTO TEXT,
        QUANTIDADE INTEGER,
        VALOR_UNITARIO REAL,
        PARCELAS INTEGER,
        DATA_PEDIDO TEXT,
        MEIO_PAGAMENTO TEXT,
        STATUS_PAGAMENTO TEXT,
        FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID)
    )
    ''')
    
    # Tabela LOG_DE_RODADAS
    conn.execute('''
    CREATE TABLE IF NOT EXISTS LOG_DE_RODADAS (
        ID_RODADA INTEGER PRIMARY KEY AUTOINCREMENT,
        DATA_RODADA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        TABELA TEXT,
        QTD_INCLUIDO INTEGER,
        QTD_ALTERADO INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados criado.")

def get_connection():
    return sqlite3.connect('projeto.db')