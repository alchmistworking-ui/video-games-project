import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Mercado de Videogames",
    page_icon="🎮",
    layout="wide"
)

# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================

df = pd.read_csv("data/video_games_tratado.csv")
brasil = pd.read_csv("data/brasil_regioes.csv")
df_sales = pd.read_csv(
    "data/Video_Game_Sales_as_of_Jan_2017.csv"
)

# ==========================================
# PREPARAÇÃO DOS DADOS
# ==========================================

df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)

df["ano"] = df["release_date"].dt.year

# ==========================================
# TÍTULO PRINCIPAL
# ==========================================

st.title("🎮 Mercado de Videogames")

st.subheader(
    "Análise de dados do mercado global e da indústria brasileira de games"
)

st.write(
    "Explore indicadores de vendas, consoles, gêneros, publishers "
    "e a distribuição regional das desenvolvedoras brasileiras."
)

st.divider()

# ==========================================
# ABAS
# ==========================================

aba_global, aba_sales, aba_comparativa, aba_brasil, aba_sobre = st.tabs([
    "🌎 Mercado Global",
    "📊 Sales & Performance",
    "🔎 Análise Comparativa",
    "🇧🇷 Mercado Brasileiro",
    "ℹ️ Sobre o Projeto"
])

# ==========================================================
# ==========================================================
#                  ABA MERCADO GLOBAL
# ==========================================================
# ==========================================================

with aba_global:

    st.header("🌎 Mercado Global de Videogames")
    st.caption(
        "Fonte: base global de videogames. A análise temporal "
        "utiliza 2005–2018, período com maior consistência "
        "na cobertura de vendas."
    )
    st.write(
        "Análise das vendas, consoles, gêneros, publishers "
        "e desempenho regional do mercado global."
    )

    # ==========================================
    # FILTROS
    # ==========================================

    st.sidebar.header("🎛️ Filtros — Mercado Global")

    consoles = sorted(
        df["console"]
        .dropna()
        .unique()
        .tolist()
    )

    generos = sorted(
        df["genre"]
        .dropna()
        .unique()
        .tolist()
    )

    console_selecionado = st.sidebar.multiselect(
        "🕹️ Console",
        consoles,
        placeholder="Todos os consoles"
    )

    genero_selecionado = st.sidebar.multiselect(
        "🎭 Gênero",
        generos,
        placeholder="Todos os gêneros"
    )

    # ==========================================
    # APLICAÇÃO DOS FILTROS
    # ==========================================

    df_filtrado = df.copy()

    if console_selecionado:
        df_filtrado = df_filtrado[
            df_filtrado["console"].isin(console_selecionado)
        ]

    if genero_selecionado:
        df_filtrado = df_filtrado[
            df_filtrado["genre"].isin(genero_selecionado)
        ]

         # ==========================================
    # KPIs
    # ==========================================

    total_jogos = df_filtrado["title"].count()

    dados_vendas = df_filtrado.dropna(
        subset=["total_sales"]
    )

    total_jogos_com_vendas = len(dados_vendas)

    total_vendas = df_filtrado["total_sales"].sum()

    if len(dados_vendas) > 0:

        jogo_mais_vendido = dados_vendas.loc[
            dados_vendas["total_sales"].idxmax(),
            "title"
        ]

        console_lider = (
            dados_vendas
            .groupby("console")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

    else:

        jogo_mais_vendido = "Sem dados"

        console_lider = "Sem dados"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🎮 Jogos na base",
            f"{total_jogos:,}"
        )

    with col2:
        st.metric(
            "💰 Vendas registradas",
            f"{total_vendas:,.2f} mi"
        )

    with col3:
        st.metric(
            "📊 Jogos com vendas",
            f"{total_jogos_com_vendas:,}"
        )

    with col4:
        st.metric(
            "🕹️ Console líder",
            console_lider
        )

        st.caption(
        "💡 Os valores de vendas representam milhões de unidades "
        "registradas na base. Como existem dados ausentes, os "
        "indicadores consideram apenas os registros disponíveis."
    )

    st.divider()

       # ==========================================
    # CONSOLES E GÊNEROS
    # ==========================================

    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:

        st.subheader("🕹️ Top 10 consoles por vendas")

        vendas_console = (
            df_filtrado
            .groupby("console")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(
            vendas_console,
            x_label="Console",
            y_label="Vendas (milhões)"
        )

    with col_grafico2:

        st.subheader("🎭 Top 10 gêneros por vendas")

        vendas_genero = (
            df_filtrado
            .groupby("genre")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(
            vendas_genero,
            x_label="Gênero",
            y_label="Vendas (milhões)"
        )
          # ==========================================
    # REGIÃO E EVOLUÇÃO TEMPORAL
    # ==========================================

    col_grafico3, col_grafico4 = st.columns(2)

    with col_grafico3:

        st.subheader("🌎 Vendas por região")

        vendas_regioes = pd.Series({
            "América do Norte": df_filtrado["na_sales"].sum(),
            "Europa/PAL": df_filtrado["pal_sales"].sum(),
            "Japão": df_filtrado["jp_sales"].sum(),
            "Outros": df_filtrado["other_sales"].sum()
        })

        st.bar_chart(
            vendas_regioes,
            x_label="Região",
            y_label="Vendas (milhões)"
        )

    with col_grafico4:

        st.subheader("📈 Evolução das vendas ao longo dos anos")

        vendas_por_ano = (
            df_filtrado[
                (df_filtrado["ano"] >= 2005) &
                (df_filtrado["ano"] <= 2018)
            ]
            .groupby("ano")["total_sales"]
            .sum()
        )

        st.line_chart(
            vendas_por_ano,
            x_label="Ano",
            y_label="Vendas (milhões)"
        )

        st.caption(
            "Período analisado: 2005–2018. "
            "Esse intervalo apresenta cobertura de vendas "
            "mais consistente na base."
        )
        # ==========================================
    # PUBLISHERS
    # ==========================================

    st.subheader("🏢 Top 10 publishers por vendas")

    vendas_publisher = (
        df_filtrado
        .groupby("publisher")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
    )

    st.bar_chart(
        vendas_publisher,
        x_label="Vendas (milhões)",
        y_label="Publisher"
    )
         # ==========================================
    # JOGOS MAIS VENDIDOS
    # ==========================================

    st.subheader("🏆 Top 10 jogos mais vendidos")

    top_jogos = (
        df_filtrado[
            [
                "title",
                "console",
                "genre",
                "publisher",
                "total_sales"
            ]
        ]
        .dropna(subset=["total_sales"])
        .sort_values(
            "total_sales",
            ascending=False
        )
        .head(10)
    )

    top_jogos = top_jogos.rename(
        columns={
            "title": "Jogo",
            "console": "Console",
            "genre": "Gênero",
            "publisher": "Publisher",
            "total_sales": "Vendas (milhões)"
        }
    )

    top_jogos["Vendas (milhões)"] = top_jogos[
        "Vendas (milhões)"
    ].round(2)

    st.dataframe(
        top_jogos,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Ranking baseado nos registros disponíveis de vendas "
        "na base global."
    )
    # ==========================================
    # PRINCIPAIS INSIGHTS
    # ==========================================

    st.divider()

    st.subheader("💡 Principais insights do mercado global")

    maior_genero = vendas_genero.index[0]
    vendas_maior_genero = vendas_genero.iloc[0]

    maior_console = vendas_console.index[0]
    vendas_maior_console = vendas_console.iloc[0]

    maior_regiao = vendas_regioes.idxmax()
    vendas_maior_regiao = vendas_regioes.max()

    col_insight1, col_insight2, col_insight3 = st.columns(3)

    with col_insight1:

        st.info(
            f"🎭 **Gênero líder**\n\n"
            f"{maior_genero} apresenta o maior volume de vendas "
            f"entre os gêneros analisados, com aproximadamente "
            f"{vendas_maior_genero:.2f} milhões de unidades."
        )

    with col_insight2:

        st.info(
            f"🕹️ **Console líder**\n\n"
            f"{maior_console} apresenta o maior volume acumulado "
            f"de vendas na base, com aproximadamente "
            f"{vendas_maior_console:.2f} milhões de unidades."
        )

    with col_insight3:

        st.info(
            f"🌎 **Principal região**\n\n"
            f"{maior_regiao} concentra o maior volume de vendas "
            f"registradas, com aproximadamente "
            f"{vendas_maior_regiao:.2f} milhões de unidades."
        )
    # ==========================================
    # LIMITAÇÕES DOS DADOS
    # ==========================================

    st.divider()

    st.subheader("⚠️ Limitações dos dados")

    st.write(
        "A base apresenta valores ausentes principalmente "
        "nas variáveis relacionadas às vendas e avaliações. "
        "As análises de vendas utilizam os registros que "
        "possuem valores disponíveis. A análise temporal foi "
        "limitada ao período de 2005 a 2018 devido à redução "
        "significativa da cobertura de vendas nos anos posteriores."
    )

# ==========================================================
# ==========================================================
#                  ABA SALES & PERFORMANCE
# ==========================================================
# ==========================================================

with aba_sales:

    st.header("📊 Sales & Performance")
    
    st.caption(
        "Fonte: Video Game Sales Dataset, com registros de "
        "vendas, plataformas, gêneros, publishers e avaliações."
    )

    st.write(
        "Análise complementar das vendas globais de videogames, "
        "desempenho das plataformas, gêneros, publishers e "
        "avaliações dos jogos."
    )
    # ==========================================
    # FILTROS
    # ==========================================

    st.subheader("🎛️ Filtros da análise")

    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

    plataformas_sales = sorted(
        df_sales["Platform"]
        .dropna()
        .unique()
        .tolist()
    )

    generos_sales = sorted(
        df_sales["Genre"]
        .dropna()
        .unique()
        .tolist()
    )

    anos_sales = sorted(
        df_sales["Year_of_Release"]
        .dropna()
        .unique()
        .tolist()
    )

    with col_filtro1:

        plataforma_selecionada = st.multiselect(
            "🕹️ Plataforma",
            plataformas_sales,
            placeholder="Todas as plataformas"
        )

    with col_filtro2:

        genero_sales_selecionado = st.multiselect(
            "🎭 Gênero",
            generos_sales,
            placeholder="Todos os gêneros"
        )

    with col_filtro3:

        intervalo_anos = st.slider(
            "📅 Período",
            int(min(anos_sales)),
            int(max(anos_sales)),
            (
                int(min(anos_sales)),
                int(max(anos_sales))
            )
        )

    # ==========================================
    # APLICAÇÃO DOS FILTROS
    # ==========================================

    df_sales_filtrado = df_sales.copy()

    if plataforma_selecionada:

        df_sales_filtrado = df_sales_filtrado[
            df_sales_filtrado["Platform"].isin(
                plataforma_selecionada
            )
        ]

    if genero_sales_selecionado:

        df_sales_filtrado = df_sales_filtrado[
            df_sales_filtrado["Genre"].isin(
                genero_sales_selecionado
            )
        ]

    df_sales_filtrado = df_sales_filtrado[
        df_sales_filtrado["Year_of_Release"].between(
            intervalo_anos[0],
            intervalo_anos[1]
        )
    ]

    st.caption(
        f"Registros após aplicação dos filtros: "
        f"{len(df_sales_filtrado):,}"
        .replace(",", ".")
    )

    st.divider()
    st.divider()

# ==========================================
# KPIs
# ==========================================

    total_registros_sales = len(df_sales_filtrado)

    vendas_globais_sales = (
        df_sales_filtrado["Global_Sales"].sum()
    )

    jogos_plataformas = (
        df_sales_filtrado["Platform"].nunique()
    )

    jogos_avaliados = (
        df_sales_filtrado["Critic_Score"].notna().sum()
    )

    

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🎮 Registros",
            f"{total_registros_sales:,}"
        )

    with col2:
        st.metric(
            "💰 Vendas globais",
            f"{vendas_globais_sales:,.2f} mi"
        )

    with col3:
        st.metric(
            "🕹️ Plataformas",
            jogos_plataformas
        )

    with col4:
        st.metric(
            "⭐ Jogos avaliados",
            f"{jogos_avaliados:,}"
        )

    st.divider()

        # ==========================================
    # VENDAS POR PLATAFORMA E GÊNERO
    # ==========================================

    col_sales1, col_sales2 = st.columns(2)

    with col_sales1:

        st.subheader("🕹️ Top 10 plataformas por vendas")

        vendas_plataforma = (
            df_sales_filtrado
            .groupby("Platform")["Global_Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(
            vendas_plataforma,
            x_label="Plataforma",
            y_label="Vendas globais (milhões)"
        )

    with col_sales2:

        st.subheader("🎭 Vendas por gênero")

        vendas_genero_sales = (
            df_sales_filtrado
            .groupby("Genre")["Global_Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            vendas_genero_sales,
            x_label="Gênero",
            y_label="Vendas globais (milhões)"
        )

    st.divider()

    # ==========================================
    # EVOLUÇÃO ANUAL
    # ==========================================

    st.subheader("📈 Evolução das vendas globais")

    vendas_ano_sales = (
        df_sales_filtrado
        .groupby("Year_of_Release")["Global_Sales"]
        .sum()
        .sort_index()
    )

    st.line_chart(
        vendas_ano_sales,
        x_label="Ano",
        y_label="Vendas globais (milhões)"
    )

    st.caption(
        "Os valores representam as vendas globais registradas "
        "na base por ano de lançamento, considerando os filtros selecionados."
    )

    st.divider()
    # ==========================================
    # PUBLISHERS
    # ==========================================

    st.subheader("🏢 Top 10 publishers por vendas")

    vendas_publishers_sales = (
    df_sales_filtrado
        .groupby("Publisher")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
    )

    st.bar_chart(
        vendas_publishers_sales,
        x_label="Vendas globais (milhões)",
        y_label="Publisher"
    )

    st.divider()

    # ==========================================
    # TOP 10 JOGOS
    # ==========================================

    st.subheader("🏆 Top 10 jogos por vendas globais")

    top_jogos_sales = (
        df_sales[
            [
                "Name",
                "Platform",
                "Genre",
                "Publisher",
                "Global_Sales"
            ]
        ]
        .sort_values(
            "Global_Sales",
            ascending=False
        )
        .head(10)
    )

    top_jogos_sales = top_jogos_sales.rename(
        columns={
            "Name": "Jogo",
            "Platform": "Plataforma",
            "Genre": "Gênero",
            "Publisher": "Publisher",
            "Global_Sales": "Vendas globais (mi)"
        }
    )

    top_jogos_sales["Vendas globais (mi)"] = (
        top_jogos_sales["Vendas globais (mi)"].round(2)
    )

    st.dataframe(
        top_jogos_sales,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # CLASSIFICAÇÃO ETÁRIA
    # ==========================================

    col_rating1, col_rating2 = st.columns(2)

    with col_rating1:

        st.subheader("🔞 Vendas por classificação")

        vendas_rating = (
            df_sales
            .dropna(subset=["Rating"])
            .groupby("Rating")["Global_Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            vendas_rating,
            x_label="Classificação",
            y_label="Vendas globais (milhões)"
        )

    with col_rating2:

        st.subheader("⭐ Distribuição das notas dos críticos")

        notas = (
            df_sales["Critic_Score"]
            .dropna()
        )

        st.write(
            f"**Jogos avaliados:** {len(notas):,}"
        )

        st.write(
            f"**Média:** {notas.mean():.2f}"
        )

        st.write(
            f"**Mediana:** {notas.median():.2f}"
        )

        st.write(
            f"**Maior nota:** {notas.max():.0f}"
        )

        st.write(
            f"**Menor nota:** {notas.min():.0f}"
        )

    st.divider()

    # ==========================================
    # NOTA X VENDAS
    # ==========================================

    st.subheader(
        "⭐ Relação entre avaliação dos críticos e vendas"
    )

    dados_correlacao = df_sales[
        ["Critic_Score", "Global_Sales"]
    ].dropna()

    correlacao = dados_correlacao[
        "Critic_Score"
    ].corr(
        dados_correlacao["Global_Sales"]
    )

    st.metric(
        "Correlação entre nota crítica e vendas",
        f"{correlacao:.3f}"
    )

    st.info(
        "A correlação observada é positiva, mas não representa "
        "uma relação de causalidade. Ela indica apenas a associação "
        "entre as duas variáveis nos registros que possuem "
        "avaliação crítica disponível."
    )

    st.divider()

    # ==========================================
    # LIMITAÇÕES
    # ==========================================

    st.subheader("⚠️ Limitações desta base")

    st.write(
        """
        • A base apresenta valores ausentes principalmente nas
          avaliações dos críticos, avaliações dos usuários e
          classificações etárias.

        • A análise de avaliações considera somente os jogos
          que possuem dados disponíveis.

        • Foram identificadas 10 ocorrências de jogos com o
          mesmo nome e plataforma, que foram mantidas na base
          original para preservar os registros.

        • Foi identificada uma diferença de 4,88 milhões entre
          a soma das vendas regionais e o campo Global_Sales.

        • Os valores representam os registros disponíveis na
          base e não necessariamente todo o mercado mundial.
        """
    )
    # ==========================================================
# ==========================================================
#                  ABA ANÁLISE COMPARATIVA
# ==========================================================
# ==========================================================

with aba_comparativa:

    st.header("🔎 Análise Comparativa dos Datasets")

    aba_visao, aba_generos, aba_plataformas, aba_publishers, aba_evolucao, aba_avaliacoes, aba_insights, aba_qualidade = st.tabs([
        "📋 Visão Geral",
        "🎮 Gêneros",
        "🕹️ Plataformas",
        "🏢 Publishers",
        "📈 Evolução",
        "⭐ Avaliações",
        "💡 Insights",
        "🔬 Qualidade"
    ])

    # ======================================================
    # VISÃO GERAL
    # ======================================================

    with aba_visao:

        st.subheader("📚 Comparação das bases de dados")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Dataset Mercado Global")

            st.metric(
                "Registros",
                f"{len(df):,}".replace(",", ".")
            )

            st.metric(
                "Vendas registradas",
                f"{df['total_sales'].sum():,.2f} mi"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            st.metric(
                "Consoles",
                df["console"].nunique()
            )

            st.metric(
                "Gêneros",
                df["genre"].nunique()
            )

            st.metric(
                "Período",
                "2005–2018*"
            )

        with col2:

            st.markdown("### 📊 Dataset Sales")

            st.metric(
                "Registros",
                f"{len(df_sales):,}".replace(",", ".")
            )

            st.metric(
                "Vendas globais",
                f"{df_sales['Global_Sales'].sum():,.2f} mi"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            st.metric(
                "Plataformas",
                df_sales["Platform"].nunique()
            )

            st.metric(
                "Gêneros",
                df_sales["Genre"].nunique()
            )

            st.metric(
                "Período",
                f"{int(df_sales['Year_of_Release'].min())}–"
                f"{int(df_sales['Year_of_Release'].max())}"
            )

        st.caption(
            "*Na base Mercado Global, o período 2005–2018 corresponde "
            "ao intervalo adotado para a análise temporal de vendas."
        )

        st.subheader("💡 Objetivo da comparação")

        st.info(
            """
            As duas bases possuem estruturas e períodos de cobertura
            diferentes. A comparação busca ampliar a análise do mercado
            de videogames a partir de diferentes fontes de dados.
            """
        )

    # ======================================================
    # GÊNEROS
    # ======================================================

    with aba_generos:

        st.subheader("🎮 Comparação de vendas por gênero")

        vendas_genero_global = (
            df.groupby("genre")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        vendas_genero_sales = (
            df_sales.groupby("Genre")["Global_Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Mercado Global")

            st.bar_chart(
                vendas_genero_global.sort_values(ascending=True),
                horizontal=True,
                x_label="Vendas (milhões)",
                y_label="Gênero"
            )

        with col2:

            st.markdown("### 📊 Sales Dataset")

            st.bar_chart(
                vendas_genero_sales.sort_values(ascending=True),
                horizontal=True,
                x_label="Vendas (milhões)",
                y_label="Gênero"
            )

        st.caption(
            "Os rankings apresentam os 10 gêneros com maior volume "
            "de vendas em cada base. Os valores não devem ser "
            "comparados diretamente como se as duas bases tivessem "
            "a mesma cobertura de registros e períodos."
        )

        # ======================================================
    # PLATAFORMAS
    # ======================================================

    with aba_plataformas:

        st.subheader("🕹️ Comparação de vendas por plataforma")

        vendas_console_global = (
            df.groupby("console")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        vendas_plataforma_sales = (
            df_sales.groupby("Platform")["Global_Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Mercado Global")

            st.bar_chart(
                vendas_console_global.sort_values(ascending=True),
                horizontal=True,
                x_label="Vendas (milhões)",
                y_label="Console"
            )

        with col2:

            st.markdown("### 📊 Sales Dataset")

            st.bar_chart(
                vendas_plataforma_sales.sort_values(ascending=True),
                horizontal=True,
                x_label="Vendas (milhões)",
                y_label="Plataforma"
            )

        st.caption(
            "Os rankings apresentam as 10 plataformas com maior volume "
            "de vendas em cada base. As plataformas e os valores podem "
            "variar devido às diferenças de cobertura entre os datasets."
        )
    # ======================================================
    # PUBLISHERS
    # ======================================================

    with aba_publishers:

        st.subheader("🏢 Comparação de vendas por publisher")

        vendas_publisher_global = (
            df.groupby("publisher")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        vendas_publisher_sales = (
            df_sales.groupby("Publisher")["Global_Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Mercado Global")

            st.bar_chart(
                vendas_publisher_global.sort_values(ascending=True),
                horizontal=True,
                x_label="Vendas (milhões)",
                y_label="Publisher"
            )

        with col2:

            st.markdown("### 📊 Sales Dataset")

            st.bar_chart(
                vendas_publisher_sales.sort_values(ascending=True),
                horizontal=True,
                x_label="Vendas (milhões)",
                y_label="Publisher"
            )

        st.caption(
            "Os rankings apresentam os 10 publishers com maior "
            "volume de vendas em cada base. Os valores não devem "
            "ser comparados diretamente como se as bases tivessem "
            "a mesma cobertura de registros e períodos."
        )
        # ======================================================
    # EVOLUÇÃO
    # ======================================================

    with aba_evolucao:

        st.subheader("📈 Evolução das vendas ao longo do tempo")

        st.markdown(
            "A comparação temporal considera o período de "
            "2005 a 2018 na base Mercado Global, intervalo "
            "adotado por apresentar maior consistência na "
            "cobertura de vendas."
        )

        # ------------------------------------------
        # MERCADO GLOBAL
        # ------------------------------------------

        vendas_ano_global = (
            df[
                (df["ano"] >= 2005) &
                (df["ano"] <= 2018)
            ]
            .groupby("ano")["total_sales"]
            .sum()
            .sort_index()
        )

        # ------------------------------------------
        # SALES DATASET
        # ------------------------------------------

        vendas_ano_sales = (
            df_sales[
                (df_sales["Year_of_Release"] >= 2005) &
                (df_sales["Year_of_Release"] <= 2018)
            ]
            .groupby("Year_of_Release")["Global_Sales"]
            .sum()
            .sort_index()
        )

        # ------------------------------------------
        # GRÁFICOS
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Mercado Global")

            st.line_chart(
                vendas_ano_global,
                x_label="Ano",
                y_label="Vendas (milhões)"
            )

        with col2:

            st.markdown("### 📊 Sales Dataset")

            st.line_chart(
                vendas_ano_sales,
                x_label="Ano",
                y_label="Vendas (milhões)"
            )

        st.caption(
            "Para tornar a comparação temporal mais consistente, "
            "ambas as bases foram analisadas no intervalo de 2005 "
            "a 2018. Os valores representam as vendas registradas "
            "em cada dataset."
        )
        # ======================================================
    # AVALIAÇÕES
    # ======================================================

    with aba_avaliacoes:

        st.subheader(
            "⭐ Avaliações dos jogos e relação com vendas"
        )

        st.markdown(
            "Esta análise utiliza o Sales Dataset, que possui "
            "informações de avaliação dos críticos. A base "
            "Mercado Global não apresenta uma variável equivalente "
            "disponível para comparação direta."
        )

        # ------------------------------------------
        # DADOS PARA ANÁLISE
        # ------------------------------------------

        dados_avaliacoes = df_sales[
            ["Critic_Score", "Global_Sales"]
        ].dropna()

        correlacao = (
            dados_avaliacoes["Critic_Score"]
            .corr(dados_avaliacoes["Global_Sales"])
        )

        nota_media = (
            dados_avaliacoes["Critic_Score"].mean()
        )

        jogos_analisados = len(dados_avaliacoes)

        # ------------------------------------------
        # KPIs
        # ------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎮 Jogos analisados",
                f"{jogos_analisados:,}".replace(",", ".")
            )

        with col2:

            st.metric(
                "⭐ Nota média",
                f"{nota_media:.1f}"
            )

        with col3:

            st.metric(
                "📊 Correlação nota × vendas",
                f"{correlacao:.3f}"
            )

        st.divider()

        # ------------------------------------------
        # GRÁFICO
        # ------------------------------------------

        st.subheader(
            "📊 Relação entre avaliação dos críticos e vendas"
        )

        st.scatter_chart(
            dados_avaliacoes,
            x="Critic_Score",
            y="Global_Sales"
        )

        st.caption(
            "Cada ponto representa um jogo que possui tanto "
            "avaliação dos críticos quanto informação de vendas "
            "globais disponível."
        )

        # ------------------------------------------
        # INTERPRETAÇÃO
        # ------------------------------------------

        st.subheader("💡 Interpretação")

        st.info(
            f"""
            A correlação observada entre a avaliação dos críticos
            e as vendas globais foi de **{correlacao:.3f}**.

            Esse resultado indica uma associação estatística entre
            as duas variáveis nos registros analisados. Entretanto,
            correlação não significa causalidade: o resultado não
            permite afirmar que uma avaliação maior necessariamente
            provoca maiores vendas.

            A análise considera apenas os jogos que possuem dados
            disponíveis para as duas variáveis.
            """
        )

        # ------------------------------------------
        # LIMITAÇÃO
        # ------------------------------------------

        st.warning(
            """
            ⚠️ A base Mercado Global não possui uma variável de
            avaliação crítica equivalente. Por isso, não é adequado
            calcular uma comparação direta entre as duas bases
            nesse indicador.
            """
        )

       # ======================================================
    # INSIGHTS
    # ======================================================

    with aba_insights:

        st.subheader("💡 Principais insights da comparação")

        # ------------------------------------------
        # LÍDERES — MERCADO GLOBAL
        # ------------------------------------------

        genero_lider_global = (
            df.groupby("genre")["total_sales"]
            .sum()
            .idxmax()
        )

        vendas_genero_lider_global = (
            df.groupby("genre")["total_sales"]
            .sum()
            .max()
        )

        console_lider_global = (
            df.groupby("console")["total_sales"]
            .sum()
            .idxmax()
        )

        vendas_console_lider_global = (
            df.groupby("console")["total_sales"]
            .sum()
            .max()
        )

        publisher_lider_global = (
            df.groupby("publisher")["total_sales"]
            .sum()
            .idxmax()
        )

        vendas_publisher_lider_global = (
            df.groupby("publisher")["total_sales"]
            .sum()
            .max()
        )

        # ------------------------------------------
        # LÍDERES — SALES DATASET
        # ------------------------------------------

        genero_lider_sales = (
            df_sales.groupby("Genre")["Global_Sales"]
            .sum()
            .idxmax()
        )

        vendas_genero_lider_sales = (
            df_sales.groupby("Genre")["Global_Sales"]
            .sum()
            .max()
        )

        plataforma_lider_sales = (
            df_sales.groupby("Platform")["Global_Sales"]
            .sum()
            .idxmax()
        )

        vendas_plataforma_lider_sales = (
            df_sales.groupby("Platform")["Global_Sales"]
            .sum()
            .max()
        )

        publisher_lider_sales = (
            df_sales.groupby("Publisher")["Global_Sales"]
            .sum()
            .idxmax()
        )

        vendas_publisher_lider_sales = (
            df_sales.groupby("Publisher")["Global_Sales"]
            .sum()
            .max()
        )

        # ------------------------------------------
        # CARDS
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Mercado Global")

            st.info(
                f"""
                **🎭 Gênero líder**

                {genero_lider_global} — 
                {vendas_genero_lider_global:.2f} milhões de unidades.

                **🕹️ Console líder**

                {console_lider_global} — 
                {vendas_console_lider_global:.2f} milhões de unidades.

                **🏢 Publisher líder**

                {publisher_lider_global} — 
                {vendas_publisher_lider_global:.2f} milhões de unidades.
                """
            )

        with col2:

            st.markdown("### 📊 Sales Dataset")

            st.info(
                f"""
                **🎭 Gênero líder**

                {genero_lider_sales} — 
                {vendas_genero_lider_sales:.2f} milhões de unidades.

                **🕹️ Plataforma líder**

                {plataforma_lider_sales} — 
                {vendas_plataforma_lider_sales:.2f} milhões de unidades.

                **🏢 Publisher líder**

                {publisher_lider_sales} — 
                {vendas_publisher_lider_sales:.2f} milhões de unidades.
                """
            )

        st.divider()

        # ------------------------------------------
        # SÍNTESE
        # ------------------------------------------

        st.subheader("📌 Síntese da comparação")

        st.write(
            """
            As duas bases apresentam informações sobre o mercado
            de videogames, mas possuem diferenças importantes em
            relação à composição, período e variáveis disponíveis.

            A comparação mostra que os rankings de gêneros,
            plataformas, consoles e publishers podem variar entre
            os datasets. Essas diferenças estão relacionadas ao
            conjunto de registros e à cobertura de cada fonte.

            Portanto, os resultados devem ser interpretados como
            perspectivas complementares do mercado, e não como
            duas medições idênticas do mesmo universo.
            """
        )

        st.warning(
            """
            ⚠️ Os valores absolutos de vendas não devem ser usados
            isoladamente para determinar qual dataset representa
            melhor o mercado. Cada base possui características,
            períodos e registros próprios.
            """
        )
        # ======================================================
    # QUALIDADE DOS DADOS
    # ======================================================

    with aba_qualidade:

        st.subheader("🔬 Qualidade e completude dos dados")

        st.markdown(
            """
            Esta seção avalia a disponibilidade de informações
            nas duas bases utilizadas no projeto. A análise de
            dados ausentes é importante para identificar possíveis
            limitações antes da interpretação dos resultados.
            """
        )

        # ------------------------------------------
        # MERCADO GLOBAL
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Mercado Global")

            total_registros_global = len(df)

            dados_vendas_global = df["total_sales"].notna().sum()

            dados_genero_global = df["genre"].notna().sum()

            dados_console_global = df["console"].notna().sum()

            dados_publisher_global = df["publisher"].notna().sum()

            st.metric(
                "📋 Registros",
                f"{total_registros_global:,}".replace(",", ".")
            )

            st.metric(
                "💰 Registros com vendas",
                f"{dados_vendas_global:,}".replace(",", ".")
            )

            st.metric(
                "🎭 Registros com gênero",
                f"{dados_genero_global:,}".replace(",", ".")
            )

            st.metric(
                "🕹️ Registros com console",
                f"{dados_console_global:,}".replace(",", ".")
            )

            st.metric(
                "🏢 Registros com publisher",
                f"{dados_publisher_global:,}".replace(",", ".")
            )

        # ------------------------------------------
        # SALES DATASET
        # ------------------------------------------

        with col2:

            st.markdown("### 📊 Sales Dataset")

            total_registros_sales = len(df_sales)

            dados_vendas_sales = df_sales["Global_Sales"].notna().sum()

            dados_genero_sales = df_sales["Genre"].notna().sum()

            dados_plataforma_sales = df_sales["Platform"].notna().sum()

            dados_publisher_sales = df_sales["Publisher"].notna().sum()

            st.metric(
                "📋 Registros",
                f"{total_registros_sales:,}".replace(",", ".")
            )

            st.metric(
                "💰 Registros com vendas",
                f"{dados_vendas_sales:,}".replace(",", ".")
            )

            st.metric(
                "🎭 Registros com gênero",
                f"{dados_genero_sales:,}".replace(",", ".")
            )

            st.metric(
                "🕹️ Registros com plataforma",
                f"{dados_plataforma_sales:,}".replace(",", ".")
            )

            st.metric(
                "🏢 Registros com publisher",
                f"{dados_publisher_sales:,}".replace(",", ".")
            )

        st.divider()

        # ------------------------------------------
        # DADOS AUSENTES
        # ------------------------------------------

        st.subheader("⚠️ Dados ausentes")

        faltantes_global = (
            df[
                [
                    "genre",
                    "console",
                    "publisher",
                    "total_sales",
                    "critic_score"
                ]
            ]
            .isna()
            .sum()
            .sort_values(ascending=False)
        )

        faltantes_sales = (
            df_sales[
                [
                    "Genre",
                    "Platform",
                    "Publisher",
                    "Global_Sales",
                    "Critic_Score"
                ]
            ]
            .isna()
            .sum()
            .sort_values(ascending=False)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌎 Mercado Global")

            st.bar_chart(
                faltantes_global,
                x_label="Variável",
                y_label="Quantidade de valores ausentes"
            )

        with col2:

            st.markdown("### 📊 Sales Dataset")

            st.bar_chart(
                faltantes_sales,
                x_label="Variável",
                y_label="Quantidade de valores ausentes"
            )

        st.caption(
            "A quantidade de valores ausentes varia entre as bases "
            "e entre as diferentes variáveis. Essas diferenças devem "
            "ser consideradas na interpretação das análises."
        )

        st.divider()

        st.subheader("💡 Interpretação")

        st.info(
            """
            A qualidade dos dados influencia diretamente as análises
            realizadas no dashboard.

            Variáveis com muitos valores ausentes podem reduzir o
            número de registros disponíveis para determinados
            indicadores. Por isso, as análises foram realizadas
            utilizando apenas as variáveis e registros necessários
            para cada comparação.

            Dessa forma, os resultados apresentados devem ser
            interpretados considerando as características e limitações
            de cada dataset.
            """
        )
# ==========================================================
# ==========================================================
#                  ABA MERCADO BRASILEIRO
# ==========================================================
# ==========================================================

with aba_brasil:

    st.header(
        "🇧🇷 Panorama Regional da Indústria Brasileira de Games"
    )
    st.caption(
        "Fonte: Pesquisa da Indústria Brasileira de Games 2023 "
        "(Abragames/Brazil Games), com dados referentes ao cenário "
        "da indústria em 2022."
    )
    st.write(
        "Distribuição regional das desenvolvedoras de games "
        "identificadas pela Pesquisa da Indústria Brasileira de Games."
    )

    st.divider()

    # ==========================================
    # KPIs BRASIL
    # ==========================================

    total_desenvolvedoras = (
        brasil["desenvolvedoras"].sum()
    )

    regiao_lider = brasil.loc[
        brasil["desenvolvedoras"].idxmax(),
        "regiao"
    ]

    quantidade_regiao_lider = (
        brasil["desenvolvedoras"].max()
    )

    participacao_lider = brasil.loc[
        brasil["desenvolvedoras"].idxmax(),
        "participacao"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🇧🇷 Desenvolvedoras localizadas",
            f"{total_desenvolvedoras:,}"
        )

    with col2:
        st.metric(
            "🏆 Região líder",
            regiao_lider
        )

    with col3:
        st.metric(
            "📊 Participação da região líder",
            f"{participacao_lider}%"
        )

    st.divider()

        # ==========================================
    # ANÁLISE REGIONAL
    # ==========================================

    col_brasil1, col_brasil2 = st.columns(2)

    with col_brasil1:

        st.subheader(
            "📍 Desenvolvedoras de games por região"
        )

        brasil_regioes = (
            brasil
            .set_index("regiao")["desenvolvedoras"]
            .sort_values(ascending=False)
        )

        st.bar_chart(brasil_regioes)

    with col_brasil2:

        st.subheader(
            "📊 Participação regional"
        )

        participacao = (
            brasil
            .set_index("regiao")["participacao"]
            .sort_values(ascending=False)
        )

        st.bar_chart(participacao)

    st.caption(
        "Os percentuais representam a participação de cada "
        "região entre as empresas com localização identificada "
        "no levantamento."
    )

    # ==========================================
    # TABELA
    # ==========================================

    st.subheader(
        "📋 Distribuição regional"
    )

    tabela_brasil = brasil.copy()

    tabela_brasil = tabela_brasil.rename(
        columns={
            "regiao": "Região",
            "desenvolvedoras": "Desenvolvedoras",
            "participacao": "Participação (%)"
        }
    )

    st.dataframe(
        tabela_brasil,
        use_container_width=True,
        hide_index=True
    )

    # ==========================================
    # INTERPRETAÇÃO
    # ==========================================

    st.divider()

    st.subheader(
        "💡 Principais observações"
    )

    st.write(
        f"A região Sudeste apresenta a maior concentração "
        f"de desenvolvedoras identificadas, com {quantidade_regiao_lider} "
        f"empresas e participação de {participacao_lider}%."
    )
    st.write(
        f"Em conjunto, Sudeste e Sul concentram "
        f"{brasil.loc[brasil['regiao'].isin(['Sudeste', 'Sul']), 'participacao'].sum()}% "
        f"das desenvolvedoras com localização identificada, "
        f"indicando uma forte concentração regional da indústria brasileira."
    )
    st.write(
        "Os dados brasileiros representam a distribuição regional "
        "da indústria de desenvolvimento de games e não devem ser "
        "interpretados como vendas de jogos por região."
    )

# ==========================================================
# ==========================================================
#                  ABA SOBRE O PROJETO
# ==========================================================
# ==========================================================

with aba_sobre:

    st.header("📚 Sobre o projeto")

    st.write(
        """
        Este projeto apresenta uma análise de dados do mercado de
        videogames utilizando diferentes perspectivas.

        O painel reúne informações sobre jogos, consoles, gêneros,
        publishers, vendas, avaliações e a distribuição regional
        das desenvolvedoras brasileiras.
        """
    )

    st.divider()

    # ==========================================
    # METODOLOGIA
    # ==========================================

    st.subheader("🔎 Metodologia")

    st.write(
        """
        A análise foi realizada utilizando Python e bibliotecas de
        análise e visualização de dados.

        As bases passaram por etapas de exploração, identificação
        de valores ausentes, organização das variáveis e análise
        estatística.

        Para as análises de vendas, foram considerados os registros
        que apresentam valores disponíveis nas respectivas variáveis.

        A análise temporal da base global foi concentrada no período
        de 2005 a 2018 devido à maior consistência da cobertura
        de vendas nesse intervalo.
        """
    )

    st.divider()

    # ==========================================
    # FONTES
    # ==========================================

    st.subheader("📖 Fontes dos dados")

    st.write(
        """
        • Base global: conjunto de dados de videogames utilizado
          no projeto, contendo informações sobre jogos, consoles,
          publishers, gêneros e vendas por região.

        • Base Sales: conjunto de dados contendo informações sobre
          jogos, plataformas, gêneros, publishers, vendas globais,
          avaliações e classificação etária.

        • Base brasileira: Pesquisa da Indústria Brasileira de Games
          2023, realizada pela Abragames em parceria com o Brazil Games.

        Os dados utilizados no painel regional representam o cenário
        da indústria brasileira de desenvolvimento de games em 2022,
        conforme o levantamento publicado em 2023.
        """
    )

    st.markdown(
        "🔗 **Fonte oficial — Pesquisa da Indústria Brasileira de Games:** "
        "[Abragames / Brazil Games](https://brazilgames.org/pesquisa-da-industria-brasileira-de-games/)"
    )

    st.markdown(
        "📄 **Relatório completo da pesquisa:** "
        "[Relatório da Indústria Brasileira de Games 2023]"
        "(https://www.abragames.org/uploads/5/6/8/0/56805537/2023_relat%C3%B3rio_final_v4.3.3_ptbr.pdf)"
    )

    st.divider()

    # ==========================================
    # LIMITAÇÕES
    # ==========================================

    st.subheader("⚠️ Limitações")

    st.write(
        """
        • A base global apresenta valores ausentes em diversas variáveis,
          especialmente nas informações de vendas, avaliações e datas.

        • As vendas registradas não representam necessariamente a
          totalidade do mercado mundial, pois dependem da disponibilidade
          de dados na base utilizada.

        • A análise temporal foi concentrada entre 2005 e 2018 devido à
          maior consistência da cobertura de vendas nesse período.

        • A base global não apresenta informações específicas sobre a
          distribuição regional da indústria brasileira.

        • Por esse motivo, o painel brasileiro utiliza uma fonte
          independente: a Pesquisa da Indústria Brasileira de Games 2023.

        • Os indicadores dos diferentes painéis não devem ser comparados
          diretamente como se representassem a mesma variável ou o
          mesmo período.
        """
    )

    st.divider()

    st.caption(
        "Projeto acadêmico — Análise de Dados do Mercado de Videogames"
    )




