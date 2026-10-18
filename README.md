# SalesInsight PY - Pipeline de Análise de Dados de Vendas

Aplicação em Python nativo para coleta, limpeza, transformação, agregação e exportação de dados de vendas de uma empresa de varejo, acompanhado de versionamento estruturado via Git.

---

## 📁 Estrutura do Projeto

```text
salesinsight-py/
│
├── modulo_vendas.py     # Módulo com funções de tratamento, transformação e persistência
├── main.py              # Ponto de entrada e orquestração do pipeline de dados
├── vendas.csv           # Dataset de entrada contendo o histórico de vendas
├── README.md            # Documentação e instruções do projeto
├── .gitignore           # Configuração de exclusão de artefatos temporários
│
└── outputs/             # Diretório gerado contendo os relatórios finais
    ├── metricas_resumo.csv
    └── estatisticas.json
```

---

## 🛠️ Requisitos e Funcionalidades

* **Biblioteca Padrão:** Uso exclusivo dos módulos nativos `csv`, `json`, `os` e `random`.
* **Tratamento de Inconsistências:** Remoção de espaços extras (`.strip()`), filtragem de valores ausentes e conversão explícita de tipos numéricos (`int`, `float`).
* **Campos Derivados:** Cálculo de `receita_total` e classificação em `faixa_preco` (*Baixo*, *Médio*, *Alto*).
* **Métricas Agregadas:** Agregação de receita por Categoria, por Região e cálculo do Faturamento Global.
* **Segmentação de Clientes:** Enquadramento de clientes por nível de gasto acumulado (*Bronze*, *Prata*, *Ouro*).
* **Funções de Ordem Superior:** Aplicação de expressões `lambda` em iteradores de dados.
* **Persistência Multi-formato:** Exportação parametrizada dos relatórios finais em CSV e JSON.

---

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o **Python 3.8+** instalado em sua máquina.
2. Clone o repositório ou navegue até o diretório do projeto:
```bash
cd salesinsight-py
```

3. Execute o script principal via terminal:
```bash
python main.py
```

---

## 📌 Histórico de Versionamento (Git)

O projeto seguiu uma estratégia de versionamento baseada em *feature branches* e commits padronizados (*Conventional Commits*):

1. `chore: para alterações sem impacto direto nas regras de negócio`
2. `feat: para implementação de requisitos`
7. `refactor: para refatoração de código`
