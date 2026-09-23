import pandas as pd

arquivo = "data/Video_Game_Sales_as_of_Jan_2017.csv"
df = pd.read_csv(arquivo)

print("=" * 60)
print("DIMENSÕES DO DATASET")
print("=" * 60)
print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}")

print("\n" + "=" * 60)
print("COLUNAS")
print("=" * 60)
print(df.columns.tolist())

print("\n" + "=" * 60)
print("PRIMEIRAS LINHAS")
print("=" * 60)
print(df.head())

print("\n" + "=" * 60)
print("TIPOS DE DADOS")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("VALORES AUSENTES")
print("=" * 60)
print(df.isnull().sum())

print("\n" + "=" * 60)
print("INFORMAÇÕES GERAIS")
print("=" * 60)
df.info()
print("\n" + "=" * 60)
print("VALORES ÚNICOS")
print("=" * 60)

print("Plataformas:", df["Platform"].nunique())
print("Gêneros:", df["Genre"].nunique())
print("Publishers:", df["Publisher"].nunique())
print("Anos:", df["Year_of_Release"].nunique())
print("Classificações:", df["Rating"].nunique())


print("\n" + "=" * 60)
print("PLATAFORMAS")
print("=" * 60)

print(df["Platform"].value_counts().head(20))


print("\n" + "=" * 60)
print("GÊNEROS")
print("=" * 60)

print(df["Genre"].value_counts())


print("\n" + "=" * 60)
print("TOP 20 PUBLISHERS POR QUANTIDADE DE JOGOS")
print("=" * 60)

print(df["Publisher"].value_counts().head(20))


print("\n" + "=" * 60)
print("TOP 20 JOGOS POR VENDAS GLOBAIS")
print("=" * 60)

print(
    df[["Name", "Platform", "Year_of_Release", "Global_Sales"]]
    .sort_values("Global_Sales", ascending=False)
    .head(20)
)


print("\n" + "=" * 60)
print("VENDAS GLOBAIS POR GÊNERO")
print("=" * 60)

print(
    df.groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
)


print("\n" + "=" * 60)
print("VENDAS GLOBAIS POR PLATAFORMA")
print("=" * 60)

print(
    df.groupby("Platform")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
)


print("\n" + "=" * 60)
print("VENDAS POR REGIÃO")
print("=" * 60)

print("América do Norte:", df["NA_Sales"].sum())
print("Europa:", df["EU_Sales"].sum())
print("Japão:", df["JP_Sales"].sum())
print("Outros:", df["Other_Sales"].sum())
print("Global:", df["Global_Sales"].sum())
print("\n" + "=" * 60)
print("TOP 20 PUBLISHERS POR VENDAS GLOBAIS")
print("=" * 60)

print(
    df.groupby("Publisher")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
)


print("\n" + "=" * 60)
print("VENDAS GLOBAIS POR ANO")
print("=" * 60)

print(
    df.groupby("Year_of_Release")["Global_Sales"]
    .sum()
    .sort_index()
)


print("\n" + "=" * 60)
print("VENDAS GLOBAIS POR CLASSIFICAÇÃO")
print("=" * 60)

print(
    df.groupby("Rating")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
)


print("\n" + "=" * 60)
print("MÉDIA DE NOTA DOS CRÍTICOS")
print("=" * 60)

print(
    df["Critic_Score"]
    .describe()
)


print("\n" + "=" * 60)
print("RELAÇÃO ENTRE NOTA DOS CRÍTICOS E VENDAS")
print("=" * 60)

dados_notas = df[["Critic_Score", "Global_Sales"]].dropna()

print("Jogos com nota:", len(dados_notas))

print(
    dados_notas.corr()
)


print("\n" + "=" * 60)
print("CONFERÊNCIA DAS VENDAS REGIONAIS")
print("=" * 60)

soma_regioes = (
    df["NA_Sales"].sum()
    + df["EU_Sales"].sum()
    + df["JP_Sales"].sum()
    + df["Other_Sales"].sum()
)

print("Soma das regiões:", soma_regioes)
print("Global Sales:", df["Global_Sales"].sum())
print("Diferença:", df["Global_Sales"].sum() - soma_regioes)
print("\n" + "=" * 60)
print("VERIFICAÇÃO DE DUPLICIDADES")
print("=" * 60)

print("Linhas duplicadas completas:", df.duplicated().sum())

print("\nJogos com mesmo nome e plataforma:")
print(
    df.duplicated(
        subset=["Name", "Platform"],
        keep=False
    ).sum()
)