import os
import modulo_vendas as mv

def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Pipeline de Processamento com Python Nativo")
    print("=" * 60)

    arquivo_dados = "vendas.csv"

    # 1. Gerar dataset sintético se não existir
    if not os.path.exists(arquivo_dados):
        mv.gerar_dataset_sintetico(arquivo_dados, n_registros=150)

    # 2. Leitura dos dados
    dados_brutos = mv.carregar_csv(arquivo_dados)
    
    # 3. Inspeção inicial
    mv.inspecionar_dados(dados_brutos)

if __name__ == "__main__":
    main()