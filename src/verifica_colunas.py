import sqlite3

def verificar_tabelas():
    conn = sqlite3.connect('projeto.db')
    cursor = conn.cursor()
    
    print("Verificando estrutura do banco.")
    print("=" * 60)
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    
    for tabela in tabelas:
        nome_tabela = tabela[0]
        print(f"\n Tabela: {nome_tabela}")
        print("-" * 40)
        
        cursor.execute(f"PRAGMA table_info({nome_tabela});")
        colunas = cursor.fetchall()
        
        for coluna in colunas:
            col_id, col_nome, col_tipo, not_null, default_val, pk = coluna
            print(f"  {col_id:2d}. {col_nome:25} ({col_tipo:10}) {'PK' if pk else ''}")
        
        try:
            cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 3;")
            linhas = cursor.fetchall()
            if linhas:
                print(f"\n Amostra de dados (3 primeiras linhas):")

                cursor.execute(f"PRAGMA table_info({nome_tabela});")
                nomes_colunas = [info[1] for info in cursor.fetchall()]
                print(f"Colunas: {nomes_colunas}")
                for linha in linhas:
                    print(f"{linha}")
        except:
            pass
    
    conn.close()

if __name__ == "__main__":
    verificar_tabelas()