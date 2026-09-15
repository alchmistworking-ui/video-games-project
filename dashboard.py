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

aba_global, aba_brasil = st.tabs([
    "🌎 Mercado Global",
    "🇧🇷 Mercado Brasileiro"
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

# ==========================================
# RODAPÉ
# ==========================================
# ==========================================
# SOBRE O PROJETO
# ==========================================

st.divider()

st.header("📚 Sobre o projeto")

st.write(
    """
    Este projeto apresenta uma análise de dados do mercado de
    videogames utilizando duas perspectivas complementares.

    O primeiro painel apresenta uma análise do mercado global,
    utilizando informações sobre jogos, consoles, gêneros,
    publishers, vendas e regiões.

    O segundo painel apresenta um panorama regional da indústria
    brasileira de desenvolvimento de games, permitindo observar
    a concentração das empresas desenvolvedoras entre as regiões
    do país.
    """
)

# ==========================================
# METODOLOGIA
# ==========================================

st.subheader("🔎 Metodologia")

st.write(
    """
    A análise foi realizada utilizando Python e bibliotecas de
    análise e visualização de dados. A base global passou por
    uma etapa de exploração, identificação de valores ausentes
    e organização das variáveis utilizadas no dashboard.

    Para as análises de vendas, foram considerados os registros
    que apresentam valores disponíveis nas respectivas variáveis.

    A análise temporal foi concentrada no período de 2005 a 2018,
    devido à maior consistência da cobertura de vendas nesse intervalo.
    """
)

# ==========================================
# FONTES
# ==========================================

st.subheader("📖 Fontes dos dados")

st.write(
    """
    • Base global: conjunto de dados de videogames utilizado
      no projeto, contendo informações sobre jogos, consoles,
      publishers, gêneros e vendas por região.

      A base reúne registros de diferentes anos. Para a análise
      temporal de vendas, foi adotado o período de 2005 a 2018,
      devido à maior consistência da cobertura de vendas nesse
      intervalo.

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
      independente: a Pesquisa da Indústria Brasileira de Games 2023,
      com dados referentes ao cenário da indústria em 2022.

    • Os indicadores dos dois painéis não devem ser comparados
      diretamente como se representassem a mesma variável ou o
      mesmo período.
    """
)
st.divider()

st.caption(
    "Projeto acadêmico — Análise de Dados do Mercado de Videogames"
)