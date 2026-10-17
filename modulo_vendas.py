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