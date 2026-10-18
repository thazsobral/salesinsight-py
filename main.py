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
    mv.inspecionar_dados(dados_brutos)

    # 3. Limpeza e Transformação
    dados_limpos = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # 4. Uso de Função de Ordem Superior (Lambda)
    dados_com_tag = mv.processar_transformacao(
        dados_transformados, 
        lambda x: {**x, "processado": True}
    )

    # 5. Métricas e Segmentação
    metricas = mv.calcular_metricas(dados_com_tag)
    segmentos = mv.segmentar_clientes(dados_com_tag)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    # 6. Exibição de Resultados no Terminal
    print("\n=== RESUMO EXECUTIVO ===")
    print(f"Receita Total da Empresa: R$ {metricas['total_geral']:,.2f}")
    
    print("\nReceita por Categoria:")
    for cat, rec in metricas["por_categoria"].items():
        print(f"  - {cat}: R$ {rec:,.2f}")

    print("\nReceita por Região:")
    for reg, rec in metricas["por_regiao"].items():
        print(f"  - {reg}: R$ {rec:,.2f}")

    print("\nTop 5 Clientes Ouro/Prata:")
    for cli, info in top_clientes:
        print(f"  - {cli}: R$ {info['total_gasto']:,.2f} ({info['segmento']})")

    # 7. Exportação dos Arquivos
    # mv.exportar_resultados(metricas, segmentos)

    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")

if __name__ == "__main__":
    main()