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
        DT_NASC TEXT,
        SEXO TEXT,
        CADASTRO TEXT,
        CIDADE TEXT,
        ESTADO TEXT,
        RECEBE_EMAIL INTEGER
    )
    ''')
    
    # Tabela PEDIDOS
    conn.execute('''
    CREATE TABLE IF NOT EXISTS PEDIDOS (
        COD_PEDIDO INTEGER,
        COD_CLIENTE INTEGER,
        CODIGO_PRODUTO INTEGER,
        DEPTO TEXT,
        QUANTIDADE INTEGER,
        VALOR_UNITARIO REAL,
        QTD_PARCELAS INTEGER,
        DT_PEDIDO TEXT,
        MEIO_PAGTO TEXT,
        STATUS_PAGAMENTO TEXT,
        VALOR_TOTAL REAL,
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