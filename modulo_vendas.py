import csv
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
