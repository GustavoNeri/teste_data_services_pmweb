import os
import sqlite3
import pandas as pd

def criar_banco():
    conn = sqlite3.connect('projeto.db')
    
    # Tabela CLIENTES
    conn.execute('DROP TABLE IF EXISTS CLIENTES')
    conn.execute('''
    CREATE TABLE CLIENTES (
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
    conn.execute('DROP TABLE IF EXISTS PEDIDOS')
    conn.execute('''
    CREATE TABLE PEDIDOS (
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
        VALOR_TOTAL REAL,
        FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID)
    )
    ''')
    
    # Tabela LOG_DE_RODADAS
    conn.execute('DROP TABLE IF EXISTS LOG_DE_RODADAS')
    conn.execute('''
    CREATE TABLE LOG_DE_RODADAS (
        ID_RODADA INTEGER PRIMARY KEY AUTOINCREMENT,
        DATA_RODADA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        TABELA TEXT,
        QTD_ALTERADO INTEGER DEFAULT 0,
        QTD_INCLUIDO INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados criado.")

def get_connection():
    return sqlite3.connect('projeto.db')

def resetar_banco():
    print("=" * 60)
    print("Reset do banco de dados")
    print("=" * 60)

    if os.path.exists('projeto.db'):
        os.remove('projeto.db')
        print("Arquivo projeto.db removido")
    
    criar_banco()
    
    verificar_estrutura()

if __name__ == "__main__":
    resetar_banco()