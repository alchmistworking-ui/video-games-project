import pandas as pd

# Carregar a base de dados
df = pd.read_csv("data/Video Games Data.csv")

# Mostrar as primeiras 5 linhas
print(df.head())

# Informações gerais da base
print("\nInformações da base:")
df.info()
# Verificar valores ausentes
print("\nValores ausentes por coluna:")
print(df.isnull().sum())
print("\nQuantidade de jogos por gênero:")
print(df["genre"].value_counts())

print("\nQuantidade de jogos por console:")
print(df["console"].value_counts().head(20))

print("\nQuantidade de jogos por publisher:")
print(df["publisher"].value_counts().head(20))
print("\nEstatísticas das vendas totais:")
print(df["total_sales"].describe())

print("\n10 jogos com maiores vendas:")
print(df[["title", "console", "total_sales"]]
      .sort_values("total_sales", ascending=False)
      .head(10))
print("\nVendas por região:")

print("\nAmérica do Norte:")
print(df["na_sales"].describe())

print("\nJapão:")
print(df["jp_sales"].describe())

print("\nEuropa:")
print(df["pal_sales"].describe())

print("\nOutras regiões:")
print(df["other_sales"].describe())
# ==========================================
# PREPARAÇÃO DOS DADOS
# ==========================================

# Criando uma cópia da base
df_analise = df.copy()

# Transformando a data de lançamento em formato de data
df_analise["release_date"] = pd.to_datetime(
    df_analise["release_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Criando uma coluna com o ano de lançamento
df_analise["release_year"] = df_analise["release_date"].dt.year

print("\nInformações da base preparada:")
print(df_analise[[
    "title",
    "console",
    "genre",
    "total_sales",
    "release_date",
    "release_year"
]].head())

print("\nQuantidade de jogos por ano:")
print(df_analise["release_year"].value_counts().sort_index())
print("\nQuantidade de datas válidas:")
print(df_analise["release_date"].notna().sum())

print("\nQuantidade de datas ausentes:")
print(df_analise["release_date"].isna().sum())

print("\nAno mais antigo:")
print(df_analise["release_year"].min())

print("\nAno mais recente:")
print(df_analise["release_year"].max())

print("\nQuantidade de jogos após 2020:")
print(
    df_analise[df_analise["release_year"] > 2020]
    .shape[0]
)
print("\nVendas por gênero:")

vendas_genero = (
    df_analise
    .groupby("genre")
    .agg(
        quantidade_jogos=("title", "count"),
        vendas_totais=("total_sales", "sum"),
        media_vendas=("total_sales", "mean")
    )
    .sort_values("vendas_totais", ascending=False)
)

print(vendas_genero)
print("\nTop 10 gêneros por vendas totais:")

top_generos = (
    df_analise.groupby("genre")["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_generos)
import matplotlib.pyplot as plt

top_generos = (
    df_analise.groupby("genre")["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

top_generos.sort_values().plot(kind="barh")

plt.title("Top 10 gêneros de jogos por vendas totais")
plt.xlabel("Vendas totais (milhões)")
plt.ylabel("Gênero")

plt.tight_layout()
plt.show()
vendas_por_ano = (
    df_analise.dropna(subset=["total_sales", "release_year"])
    .groupby("release_year")["total_sales"]
    .sum()
)

print("\nVendas totais por ano:")
print(vendas_por_ano)
plt.figure(figsize=(12, 6))

vendas_por_ano.plot(kind="line", marker="o")

plt.title("Evolução das vendas de jogos ao longo dos anos")
plt.xlabel("Ano de lançamento")
plt.ylabel("Vendas totais (milhões)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
print("\nVendas por console:")

vendas_console = (
    df_analise
    .groupby("console")
    .agg(
        quantidade_jogos=("title", "count"),
        vendas_totais=("total_sales", "sum"),
        media_vendas=("total_sales", "mean")
    )
    .sort_values("vendas_totais", ascending=False)
)

print(vendas_console.head(15))
print("\nTop 10 consoles por vendas totais:")

top_consoles = (
    df_analise.groupby("console")["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_consoles)

plt.figure(figsize=(10, 6))

top_consoles.sort_values().plot(kind="barh")

plt.title("Top 10 consoles por vendas totais")
plt.xlabel("Vendas totais (milhões)")
plt.ylabel("Console")

plt.tight_layout()
plt.show()
print("\nVendas por publisher:")

vendas_publisher = (
    df_analise
    .groupby("publisher")
    .agg(
        quantidade_jogos=("title", "count"),
        vendas_totais=("total_sales", "sum"),
        media_vendas=("total_sales", "mean")
    )
    .sort_values("vendas_totais", ascending=False)
)

print(vendas_publisher.head(15))
print("\nTop 10 jogos por vendas:")

top_jogos = (
    df_analise[["title", "console", "genre", "total_sales"]]
    .dropna(subset=["total_sales"])
    .sort_values("total_sales", ascending=False)
    .head(10)
)

print(top_jogos)
print("\nVendas totais por região:")

vendas_regiao = pd.Series({
    "América do Norte": df_analise["na_sales"].sum(),
    "Japão": df_analise["jp_sales"].sum(),
    "Europa/PAL": df_analise["pal_sales"].sum(),
    "Outras regiões": df_analise["other_sales"].sum()
})

print(vendas_regiao.sort_values(ascending=False))
# Gráfico de vendas por região

plt.figure(figsize=(8, 5))

vendas_regiao.sort_values(ascending=True).plot(
    kind="barh"
)

plt.title("Vendas totais por região")
plt.xlabel("Vendas (milhões)")
plt.ylabel("Região")
plt.tight_layout()
plt.show()
# ==========================================
# 6. VENDAS AO LONGO DOS ANOS
# ==========================================

# Converter a coluna release_date para formato de data
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

# Criar uma coluna contendo apenas o ano
df["ano"] = df["release_date"].dt.year

# Somar as vendas por ano
vendas_por_ano = df.groupby("ano")["total_sales"].sum()

print("\nVendas totais por ano:")
print(vendas_por_ano.tail(20))

# Gráfico
plt.figure(figsize=(12, 6))

plt.plot(vendas_por_ano.index, vendas_por_ano.values)

plt.title("Vendas de Videogames ao Longo dos Anos")
plt.xlabel("Ano")
plt.ylabel("Vendas Totais (milhões)")

plt.grid(True)
plt.show()
# ==========================================
# 7. QUANTIDADE DE JOGOS E VENDAS POR ANO
# ==========================================

analise_anos = df.groupby("ano").agg(
    quantidade_jogos=("title", "count"),
    jogos_com_vendas=("total_sales", "count"),
    vendas_totais=("total_sales", "sum")
)

print("\nAnálise de jogos e vendas por ano:")
print(analise_anos.tail(20))
# ==========================================
# 8. VENDAS POR CONSOLE
# ==========================================

vendas_console = df.groupby("console")["total_sales"].sum().sort_values(ascending=False)

print("\nTop 15 consoles por vendas:")
print(vendas_console.head(15))
# ==========================================
# 9. VENDAS POR PUBLISHER
# ==========================================

vendas_publisher = (
    df.groupby("publisher")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 15 publishers por vendas:")
print(vendas_publisher.head(15))
# ==========================================
# 10. VENDAS POR GÊNERO E REGIÃO
# ==========================================

vendas_genero_regiao = df.groupby("genre")[
    ["na_sales", "pal_sales", "jp_sales", "other_sales"]
].sum().sort_values("na_sales", ascending=False)

print("\nVendas por gênero e região:")
print(vendas_genero_regiao)
# ==========================================
# 11. KPIs DO MERCADO GLOBAL
# ==========================================

total_jogos = df["title"].count()
total_vendas = df["total_sales"].sum()

jogo_mais_vendido = df.loc[df["total_sales"].idxmax(), "title"]
vendas_jogo_mais_vendido = df["total_sales"].max()

console_lider = vendas_console.idxmax()
vendas_console_lider = vendas_console.max()

publisher_lider = vendas_publisher.idxmax()
vendas_publisher_lider = vendas_publisher.max()

vendas_regioes = df[
    ["na_sales", "pal_sales", "jp_sales", "other_sales"]
].sum()

regiao_lider = vendas_regioes.idxmax()
vendas_regiao_lider = vendas_regioes.max()

print("\n==========================================")
print("          KPIs DO MERCADO GLOBAL")
print("==========================================")

print(f"Total de jogos: {total_jogos:,}")
print(f"Vendas totais: {total_vendas:.2f} milhões")
print(f"Jogo mais vendido: {jogo_mais_vendido}")
print(f"Vendas do jogo mais vendido: {vendas_jogo_mais_vendido:.2f} milhões")
print(f"Console líder: {console_lider}")
print(f"Vendas do console líder: {vendas_console_lider:.2f} milhões")
print(f"Publisher líder: {publisher_lider}")
print(f"Vendas do publisher líder: {vendas_publisher_lider:.2f} milhões")
print(f"Região líder: {regiao_lider}")
print(f"Vendas da região líder: {vendas_regiao_lider:.2f} milhões")
# ==========================================
# 12. PREPARAÇÃO DA BASE PARA O DASHBOARD
# ==========================================

# Criar uma cópia da base
df_tratado = df.copy()

# Remover espaços extras dos nomes das colunas
df_tratado.columns = df_tratado.columns.str.strip()

# Remover linhas sem título
df_tratado = df_tratado.dropna(subset=["title"])

# Salvar a base tratada
df_tratado.to_csv(
    "data/video_games_tratado.csv",
    index=False
)

print("\n==========================================")
print("       BASE TRATADA CRIADA")
print("==========================================")

print(f"Linhas: {len(df_tratado):,}")
print("Arquivo: data/video_games_tratado.csv")