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

    # 4. Limpeza dos dados
    dados_limpos = mv.limpar_dados(dados_brutos)

    # 5. Transformação dos dados
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # Exibir os dados transformados
    if dados_transformados:
        print("\nDados transformados (exemplo):")
        for registro in dados_transformados[:5]:  # Exibir apenas os primeiros 5 registros
            print(registro)

    # 6. Cálculo de métricas e segmentação
    metricas = mv.calcular_metricas(dados_transformados)

    # 7. Segmentação de clientes e obtenção dos top clientes
    segmentos = mv.segmentar_clientes(dados_transformados)

    # 8. Obter os top clientes
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    print("\n=== RESUMO EXECUTIVO (PRÉVIA) ===")
    print(f"Receita Total da Empresa: R$ {metricas['total_geral']:,.2f}")
    print("\nReceita por Categoria:")
    for cat, rec in metricas["por_categoria"].items():
        print(f"  - {cat}: R$ {rec:,.2f}")

    print("\nTop 5 Clientes:")
    for cli, info in top_clientes:
        print(f"  - {cli}: R$ {info['total_gasto']:,.2f} ({info['segmento']})")

if __name__ == "__main__":
    main()