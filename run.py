"""Script principal para executar todo o projeto"""

import os
import subprocess
import sys

def criar_diretorios():
    dirs = ['data', 'src', 'output', 'output/logs', 'output/relatorios']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("\n Diretórios criados.")

def instalar_dependencias():
    print("\n Instalando dependências.")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n Dependências instaladas")
    except:
        print("\n Erro na instalação. Verifique se requirements.txt existe")

def main():
    print("=" * 60)
    print("Projeto Teste Técnico Data Services - Pmweb")
    print("=" * 60)
    
    criar_diretorios()
    
    resposta = input("\n Deseja instalar dependências? (s/n): ")
    if resposta.lower() == 's':
        instalar_dependencias()
    
    # Executa ETL
    print("\n" + "=" * 60)
    print("Etapa 1: Executando ETL")
    print("=" * 60)
    from src.etl import executar_etl
    executar_etl()
    
    # Executa análises e cria o DER
    print("\n" + "=" * 60)
    print("Etapa 2: Gerando Análises")
    print("=" * 60)
    from src.analises import gerar_analises, criar_der
    gerar_analises()
    criar_der()

    # Cria DASHBOARD pygwalker
    print("\n" + "=" * 60)
    print("Etapa 3: Gerando Visualizações")
    print("=" * 60)
    from src.visualizacao import gerar_visualizacao
    gerar_visualizacao()
    
    print("\n" + "=" * 60)
    print("\n Estrutura Gerada:")
    print("     - projeto.db          - Banco de dados SQLite")
    print("     - output/relatorios/  - Arquivos CSV com análises")
    print("     - output/der.txt      - Diagrama DER")
    print("\n Próximos passos:")
    print("     1. Atualize seus CSVs na pasta 'data/'")
    print("     2. Execute: python3 run.py")
    print("=" * 60)
    print("\n DASHBOARD interativo disponível.")
    print("\n" + "=" * 60)
    print("\n Projeto executado com sucesso.")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()