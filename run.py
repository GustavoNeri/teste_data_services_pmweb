"""Script principal para executar todo o projeto"""

import os
import subprocess
import sys

def criar_diretorios():
    dirs = ['data', 'src', 'output', 'output/logs', 'output/relatorios']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("Diretórios criados.")

def instalar_dependencias():
    print("Instalando dependências.")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependências instaladas")
    except:
        print("Erro na instalação. Verifique se requirements.txt existe")

def main():
    print("=" * 60)
    print("Projeto Teste Técnico Data Services - Pmweb")
    print("=" * 60)
    
    criar_diretorios()
    
    resposta = input("\n Deseja instalar dependências? (s/n): ")
    if resposta.lower() == 's':
        instalar_dependencias()
    
    print("\n" + "=" * 60)
    print("Etapa 1: Executando ETL")
    print("=" * 60)
    from src.etl import executar_etl
    executar_etl()
    
    # Executar análises
    print("\n" + "=" * 60)
    print("Etapa 2: Gerando Análises")
    print("=" * 60)
    from src.analises import gerar_analises, criar_der
    gerar_analises()
    criar_der()
    
    print("\n" + "=" * 60)
    print("Projeto executado com sucesso.")
    print("=" * 60)
    print("\n Estrutura Gerada:")
    print("     - projeto.db          - Banco de dados SQLite")
    print("     - output/relatorios/  - Arquivos CSV com análises")
    print("     - output/der.txt      - Diagrama DER")
    print("\n Próximos passos:")
    print("     1. Coloque seus CSVs na pasta 'data/'")
    print("     2. Execute: python run.py")
    print("     3. Consulte os resultados na pasta 'output/'")

if __name__ == "__main__":
    main()