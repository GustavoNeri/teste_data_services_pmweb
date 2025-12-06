import pandas as pd
import pygwalker as pyg
import sqlite3
import os
import webbrowser
import tempfile

def gerar_visualizacao():

    if not os.path.exists('projeto.db'):
        print("Execute primeiroo arquivo run.py")
        exit()

    conn = sqlite3.connect('projeto.db')

    print("Gerando DASHBOARD Interativo.")
    print("\n" + "=" * 60)
    print("Escolha o dataset, número:")
    print("1. Pedidos")
    print("2. Clientes")
    print("3. Análise de pedidos por semestre")
    print("4. Análise de ticket médio de clientes")
    print("5. Análise de intervalo médio entre pedidos")
    print("6. Análise de classificação de clientes em tiers")
    print("7. Análise de comparativos de segmentos em 2019 e 2020")
    print("8. Análise de faixa etária dos clientes")
    print("9. Análise de localização geográfica dos clientes")
    print("10. Análise de pedidos por dia da semana")
    print("11. Análise de clientes com pagamento não aprovado para Remarketing")

    opcao = input("\n Opção: ").strip()

    if opcao == '1':
        df = pd.read_sql_query("SELECT * FROM PEDIDOS", conn)
        nome_dataset = "Pedidos"
    elif opcao == '2':
        df = pd.read_sql_query("SELECT * FROM CLIENTES", conn)
        nome_dataset = "Clientes"
    elif opcao == '3':
        df = pd.read_csv('output/relatorios/01_pedidos_por_semestre.csv')
        nome_dataset = "Pedidos por Semestre"
    elif opcao == '4':
        df = pd.read_csv('output/relatorios/02_ticket_medio_cliente.csv')
        nome_dataset = "Ticket Médio"
    elif opcao == '5':
        df = pd.read_csv('output/relatorios/03_intervalo_medio_entre_compras.csv')
        nome_dataset = "Intervalo entre Compras"
    elif opcao == '6':
        df = pd.read_csv('output/relatorios/04_classificacao_clientes_tiers.csv')
        nome_dataset = "Classificação em Tiers"
    elif opcao == '7':
        df = pd.read_csv('output/relatorios/05_comparativos_segmentos_2019_2020.csv')
        nome_dataset = "Comparativo Segmentos"
    elif opcao == '8':
        df = pd.read_csv('output/relatorios/06_faixa_etaria_clientes.csv')
        nome_dataset = "Faixa Etária"
    elif opcao == '9':
        df = pd.read_csv('output/relatorios/07_localizacao_geografica_clientes.csv')
        nome_dataset = "Localização Geográfica"
    elif opcao == '10':
        df = pd.read_csv('output/relatorios/08_pedidos_por_dia_da_semana.csv')
        nome_dataset = "Pedidos por Dia da Semana"
    elif opcao == '11':
        df = pd.read_csv('output/relatorios/09_clientes_pagamento_pendente.csv')
        nome_dataset = "Pagamentos Não Confirmados - Remarketing"
    else:
        df = pd.read_sql_query("SELECT * FROM PEDIDOS", conn)
        nome_dataset = "Pedidos"

    conn.close()

    print(f"\n Dataset carregado: {len(df)} linhas x {len(df.columns)} colunas")
    print(f"Colunas: {list(df.columns)}")

    print(f"\n Gerando dashboard: {nome_dataset}")
    print("\n Abrindo Pygwalker no navegador.")
    print(" Arraste campos para criar visualizações.")

    abrir_pygwalker_no_navegador(df, nome_dataset)

def abrir_pygwalker_no_navegador(df, titulo="Dashboard"):

    try:
        from pygwalker.api.html import to_html
        
        html_content = to_html(df)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_file = f.name
        
        print(f"\n Dashboard salvo em: {temp_file}")
        
        import webbrowser
        webbrowser.open(f'file://{temp_file}')
        
        print("\n Dashboard aberto no navegador!")
        print("\n Modo de usar:")
        print("   • Arraste campos para criar gráficos.")
        print("   • Use diferentes tipos de visualização.")
        print("   • Filtre os dados com os controles.")
        
        '''input("\n Pressione Enter para continuar.")'''
        
    except Exception as e:
        print(f"Erro ao gerar HTML: {e}")

def criar_config_pygwalker():

    config_dir = 'config'
    config_file = os.path.join(config_dir, 'pygwalker_config.json')
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    if not os.path.exists(config_file):
        config_content = {
            "visSpec": {
                "width": 1200,
                "height": 800
            },
            "config": {
                "themeKey": "vega",
                "theme": "light",
                "layout": "horizontal"
            }
        }
        
        import json
        with open(config_file, 'w') as f:
            json.dump(config_content, f, indent=2)
        
        print(f"Configuração criada: {config_file}")
    
    return config_file
    
if __name__ == "__main__":
    criar_config_pygwalker()
    gerar_visualizacao()