import csv
import json
import os
import random

def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=100, seed=42):
    """
    Gera um arquivo CSV sintético com dados de vendas contendo propositalmente
    alguns valores nulos e espaços extras para posterior etapa de limpeza.
    """
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    categorias = {
        "Notebook": "Eletrônicos",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Eletrônicos",
        "Teclado": "Acessórios",
        "Mouse": "Acessórios"
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    
    cabecalho = ["id_venda", "data_venda", "cliente", "produto", "categoria", "regiao", "quantidade", "preco_unitario"]
    dados = []

    for i in range(1, n_registros + 1):
        prod = random.choice(produtos)
        # Inserindo nulos ocasionalmente (5% de chance)
        qtd = str(random.randint(1, 8)) if random.random() > 0.05 else ""
        preco = str(round(random.uniform(100, 3500), 2)) if random.random() > 0.05 else ""
        # Adicionando espaços em branco extras em 10% dos produtos
        prod_nome = f"  {prod} " if random.random() < 0.1 else prod

        dados.append([
            i,
            f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            f"Cliente_{random.randint(1, 30):03d}",
            prod_nome,
            categorias.get(prod, "Outros"),
            random.choice(regioes),
            qtd,
            preco
        ])

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)
        writer.writerows(dados)
        
    print(f"[OK] Dataset gerado em: {caminho_arquivo}")


def carregar_csv(caminho_arquivo):
    """
    Lê o arquivo CSV de entrada utilizando csv.DictReader e retorna uma lista de dicionários.
    """
    dados = []
    with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados.append(linha)
    return dados


def inspecionar_dados(dados):
    """
    Exibe um diagnóstico inicial dos dados brutos carregados na memória.
    """
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")
    if dados:
        print(f"Campos disponíveis: {list(dados[0].keys())}")
        print(f"Exemplo do primeiro registro: {dados[0]}")

def limpar_dados(dados_brutos):
    """
    Remove espacos extras, descarta registros incompletos ou invalidos 
    e realiza a conversao explicita dos tipos de dados.
    """
    dados_limpos = []
    removidos = 0

    for lin in dados_brutos:
        # Tratamento de espacos extras em strings
        prod = lin["produto"].strip()
        cat = lin["categoria"].strip()
        reg = lin["regiao"].strip()
        cli = lin["cliente"].strip()

        # Validacao de registros com valores vazios ou ausentes
        if not lin["quantidade"] or not lin["preco_unitario"]:
            removidos += 1
            continue

        # Conversao explicita dos tipos numericos
        try:
            qtd = int(lin["quantidade"])
            preco = float(lin["preco_unitario"])
            
            dados_limpos.append({
                "id_venda": int(lin["id_venda"]),
                "data_venda": lin["data_venda"].strip(),
                "cliente": cli,
                "produto": prod,
                "categoria": cat,
                "regiao": reg,
                "quantidade": qtd,
                "preco_unitario": preco
            })
        except ValueError:
            removidos += 1

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros Válidos: {len(dados_limpos)} | Registros Removidos: {removidos}")
    return dados_limpos

def processar_transformacao(dados, funcao_transformacao):
    """
    Aplica uma funcao de ordem superior em cada registro do dataset.
    """
    return [funcao_transformacao(item) for item in dados]


def criar_campos_derivados(dados):
    """
    Calcula a receita total de cada item e classifica o registro por faixa de preco.
    """
    for item in dados:
        receita = round(item["quantidade"] * item["preco_unitario"], 2)
        item["receita_total"] = receita
        
        if receita < 500:
            item["faixa_preco"] = "Baixo"
        elif receita <= 2000:
            item["faixa_preco"] = "Médio"
        else:
            item["faixa_preco"] = "Alto"
            
    return dados

def calcular_metricas(dados):
    """
    Processa o conjunto de dados calculando a receita total por categoria,
    por regiao e o faturamento global da empresa.
    """
    receita_categoria = {}
    receita_regiao = {}
    total_geral = 0.0

    for item in dados:
        cat = item["categoria"]
        reg = item["regiao"]
        rec = item["receita_total"]

        # Agregação via dicionários usando .get() para valor padrão 0.0
        receita_categoria[cat] = round(receita_categoria.get(cat, 0.0) + rec, 2)
        receita_regiao[reg] = round(receita_regiao.get(reg, 0.0) + rec, 2)
        total_geral += rec

    return {
        "total_geral": round(total_geral, 2),
        "por_categoria": receita_categoria,
        "por_regiao": receita_regiao
    }


def segmentar_clientes(dados):
    """
    Calcula o total acumulado por cliente e classifica em faixas (Bronze, Prata, Ouro).
    """
    gastos_cliente = {}
    for item in dados:
        cli = item["cliente"]
        gastos_cliente[cli] = gastos_cliente.get(cli, 0.0) + item["receita_total"]

    segmentos = {}
    for cli, total in gastos_cliente.items():
        if total > 8000:
            cat = "Ouro"
        elif total >= 3000:
            cat = "Prata"
        else:
            cat = "Bronze"
        segmentos[cli] = {"total_gasto": round(total, 2), "segmento": cat}

    return segmentos


def obter_top_clientes(segmentos, top_n=5):
    """
    Retorna os top N clientes ordenados pelo maior valor acumulado em compras.
    """
    clientes_ordenados = sorted(
        segmentos.items(),
        key=lambda item: item[1]["total_gasto"],
        reverse=True
    )
    return clientes_ordenados[:top_n]

def exportar_resultados(metricas, clientes, pasta_saida="outputs"):
    """
    Exporta as metricas agregadas e a segmentacao de clientes em arquivos JSON e CSV.
    """
    os.makedirs(pasta_saida, exist_ok=True)
    
    # 1. Exportar JSON com relatorio estatistico consolidado
    caminho_json = os.path.join(pasta_saida, "estatisticas.json")
    dados_json = {
        "metricas_gerais": metricas,
        "clientes": clientes
    }
    
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados_json, f, indent=4, ensure_ascii=False)
    print(f"[OK] Arquivo JSON exportado em: {caminho_json}")

    # 2. Exportar CSV com resumo por categoria
    caminho_csv = os.path.join(pasta_saida, "metricas_resumo.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Categoria", "Receita Total"])
        for cat, rec in metricas["por_categoria"].items():
            escritor.writerow([cat, rec])
    print(f"[OK] Arquivo CSV exportado em: {caminho_csv}")