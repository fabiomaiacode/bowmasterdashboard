import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import altair as alt
import streamlit.components.v1 as components
import base64
from PIL import Image

# Visual

# Textos

# Exibição de dados

# lê o arquivo CSV e cria um DataFrame
df = pd.read_csv('dflimpo.csv')

# Criando as páginas

def home():
    # Adicione aqui o conteúdo da página inicial
    st.title("Bem Vindo ao BOWMASTER")
    image = Image.open('logocomplete.png')
    st.image(image, width=600)
    st.write('O BOWMASTER - ROI Dashboard foi desenvolvido por Fábio Maia, estudante do curso de Ciência da Computação da UNIFAVIP.'
             '\n\nO BOWMASTER lhe trará diversos gráficos e análises para fundamentar sua tomada de decisão.'
             '\n\nA ferramenta traz uma calculadora de ROI, a evolução das vendas, as relações TVxVendas, RádioxVendas, Social MediaxVendas e InfluencerxVendas.'
             '\n\nAlém de tudo isso, a ferramenta permite que você tenha acesso a dois filtros como o de Canais de Marketing e o de Datas.'
             '\n\nAcesse o Menu lateral e tenha acesso a diversos gráficos para tomar as melhores decisões.'
             '\n\nOs dados desse Dashboard foram baseados no dataset criado e tratado por Fábio Maia no Google Colab e posteriormente importado para o VSCode.')

# Calculadora de ROI    

import streamlit as st

def calculadora_roi():
    st.title("Calculadora de ROI")
    def calcular_roi(influencer, social_media, tv, radio):
        influencer_coef = 1.10813 # 0.554065 índice da coeficientes de correlação de Pearson
        social_media_coef = 1.04118 # 0.520590 índice da coeficientes de correlação de Pearson
        tv_coef = 0.069694 # 0.034847 índice da coeficientes de correlação de Pearson
        radio_coef = -1.233282 # -0.616641 índice da coeficientes de correlação de Pearson
        
        roi_influencer = influencer*influencer_coef
        roi_social_media = social_media*social_media_coef
        roi_tv = tv*tv_coef
        roi_radio = radio*radio_coef
        
        roi_total = roi_influencer + roi_social_media + roi_tv + roi_radio
        
        return roi_influencer, roi_social_media, roi_tv, roi_radio, roi_total

    def roi_calculator():
        st.write('Informe abaixo os valores de investimentos em marketing por canal:')
        with st.form(key='calculadora_form'):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                influencer = st.number_input('Influencer', min_value=0, max_value=1000000, value=0, step=100, format='%d', key='influencer')
            with col2:
                social_media = st.number_input('Social Media', min_value=0, max_value=1000000, value=0, step=100, format='%d', key='social_media')
            with col3:
                tv = st.number_input('TV', min_value=0, max_value=1000000, value=0, step=100, format='%d', key='tv')
            with col4:
                radio = st.number_input('Radio', min_value=0, max_value=1000000, value=0, step=100, format='%d', key='radio')
            submitted = st.form_submit_button(label='Calcular')
            if submitted:
                roi_influencer, roi_social_media, roi_tv, roi_radio, roi_total = calcular_roi(influencer, social_media, tv, radio)
                if roi_total == 0:
                    st.warning('Não é possível calcular o ROI quando o valor total do investimento é zero.')
                else:
                    st.write('ROI por canal:')
                    st.write(f'- Influencer: R$ {roi_influencer:.2f}')
                    st.write(f'- Social Media: R$ {roi_social_media:.2f}')
                    st.write(f'- TV: R$ {roi_tv:.2f}')
                    st.write(f'- Radio: R$ {roi_radio:.2f}')
                    st.write(f'Total de ROI: R$ {roi_total:.2f}')
                    fig, ax = plt.subplots()
                    ax.bar(['Influencer', 'Social Media', 'TV', 'Radio'], [roi_influencer, roi_social_media, roi_tv, roi_radio])
                    ax.set_xlabel('Canais')
                    ax.set_ylabel('ROI')
                    ax.set_title('Gráfico de ROI')
                    st.pyplot(fig)

    roi_calculator()

    st.write('ROI (Return on Investment) é um indicador financeiro utilizado para avaliar o retorno obtido em um investimento em relação ao seu custo.'
             'O ROI é calculado pela divisão do lucro obtido pelo investimento feito. Em outras palavras, é uma medida de eficiência que indica o quanto '
             'de dinheiro um investimento está gerando em relação ao valor investido.'
            'O ROI é uma métrica importante para ajudar a tomar decisões sobre investimentos, já que permite comparar a rentabilidade de diferentes oportunidades de negócio.'
             ' Quanto maior o ROI, maior será o retorno sobre o investimento e, consequentemente, mais atraente será a oportunidade.'
             '\n\nLembrando que esse cálculo considera apenas a relação linear entre as variáveis e pode não refletir a realidade em outras circunstâncias.'
             ' Além disso, é importante lembrar que o ROI não deve ser o único fator a ser considerado em uma estratégia de marketing, pois outros fatores, '
            'como o público-alvo, a mensagem da campanha, entre outros, também são importantes para o sucesso da estratégia.')

    st.write('OBS: A calculadora foi baseada nos Coeficientes de Correlação de Pearson. Sendo convertidos (x2) por conta da lógica de cálculo do ROI. '
             'Caso não tivessem sido convertidos, os ROIs sempre seriam negativos.')

# converter os valores no eixo x para formato de data/hora
df["Mes/Ano"] = pd.to_datetime(df["Mes/Ano"], format="%m/%Y")

# ---------------------------------------------------------------

def vendas():
    st.title("Evolução das vendas")
    # Adicione aqui o conteúdo da página de evolução das vendas
    # cria um gráfico de linha para mostrar a evolução das vendas ao longo do tempo
    df["Ano"] = df["Mes/Ano"].dt.year
    ax = sns.lineplot(x="Ano", y="Vendas", data=df, color='blue')
    
    # adiciona a linha de correlação
    sns.regplot(x="Ano", y="Vendas", data=df, color='red', ax=ax, scatter=False)
    
    plt.xticks(rotation=45)
    plt.title("Evolução das Vendas")
    plt.tight_layout()
    st.pyplot(ax.figure)
    st.write('Podemos observar a evolução ao longo dos anos da receita. Existem diversos fatores que devem ser observados para entender essa evolução.'
             ' Como estamos analisando o ROI, verificamos uma correlação positiva com dois canais, '
             'um canal obteve uma correlação negativa e outro canal não teve nenhuma correlação. Conheça os outros campos do BOWMASTER para verificar e tomar sua melhor decisão.')


def tv_x_vendas():
    st.title("TV x Vendas")
    # Adicione aqui o conteúdo da página de TV x vendas
    fig, ax = plt.subplots()
    x = df['TV']
    y = df['Vendas']
    ax.scatter(x, y)
    ax.set_xlabel('TV')
    ax.set_ylabel('Vendas')
    # Adiciona a linha de correlação
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), color='red')
    st.pyplot(fig)
    st.write('As grandes redes de televisão tem entrado no mundo do stream. Porém, com a concorrência internacional forte (Netflix, Disney, Starplus...) fica cada vez'
             ' mais difícil conquistar a atenção das pessoas. O gráfico mostra que não há uma correlação.'
             ' Diante dos números, nós da BOWMASTER não recomendamos investir mais que 20% do orçamento de marketing no canal TV.')


def radio_x_vendas():
    st.title("Rádio x Vendas")
    # Adicione aqui o conteúdo da página de Rádio x vendas
    fig, ax = plt.subplots()
    ax.scatter(df['Radio'], df['Vendas'])
    ax.set_xlabel('Radio')
    ax.set_ylabel('Vendas')
    
    # Adicionar linha de regressão linear
    x = df['Radio']
    y = df['Vendas']
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b, color='red')
    
    st.pyplot(fig)
    st.write('O gráfico acima mostra uma correlação negativa. Com o passar do tempo, as rádios são acessadas por um público cada vez mais velho.'
             ' Com o advento de tantos atrativos como Spotify, Deezer, Netflix entre outros, o público ouvinte das rádios, cada dia diminui.'
             ' A nova geração cada vez mais antenada com as novas tecnologias, tem deixado esse canal de lado, mesmo as rádios tendo se adaptado ao mundo digital.')

def social_media_x_vendas():
    st.title("Social Media x Vendas")
    # Adicione aqui o conteúdo da página de Social Media x vendas
    fig, ax = plt.subplots()
    ax.scatter(df['Social_Media'], df['Vendas'])
    ax.set_xlabel('Social_Media')
    ax.set_ylabel('Vendas')
    
    # calcular a linha de regressão linear
    x = df['Social_Media']
    y = df['Vendas']
    coeffs = np.polyfit(x, y, 1)
    intercept = coeffs[-1]
    slope = coeffs[-2]
    line = slope*x + intercept
    
    # traçar a linha de regressão linear
    ax.plot(x, line, color='red')
    
    st.pyplot(fig)
    st.write('O gráfico acima mostra uma correlação positiva. As redes sociais aqui no Brasil principalmente representadas por:'
             ' Instagram, TikTok e Facebook aumentaram e muito a quantidade de usuários, potenciais consumidores.'
             ' Devido a esse aumento de usuários e também a facilidade de se atingir o público alvo, as redes sociais se tornaram mais acertivas quanto a publicidade.')


def influencer_x_vendas():
    st.title("Influencer x Vendas")
    # Adicione aqui o conteúdo da página de Influencer x vendas
    fig, ax = plt.subplots()
    ax.scatter(df['Influencer'], df['Vendas'])
    ax.set_xlabel('Influencer')
    ax.set_ylabel('Vendas')

    # Calcular os coeficientes da reta de regressão linear
    a, b = np.polyfit(df['Influencer'], df['Vendas'], deg=1)

    # Criar uma função que descreve a reta de regressão linear
    f = np.poly1d([a, b])

    # Plotar a linha de correlação sobre o scatter plot
    ax.plot(df['Influencer'], f(df['Influencer']), color='red')

    st.pyplot(fig)
    st.write('O gráfico acima mostra uma correlação positiva. Ao longo do tempo muito por conta da entrada de novos usuários nas redes sociais'
             ' os influenciadores ganharam mais destaque, representando um poder de influência nas decisões de compra')


def filtro_canais():
    st.title("Filtro de canais de marketing")
    # Adicione aqui o conteúdo da página de filtro de canais de marketing
    # Botão para Filtro Canais de Marketing

    def show_filtered_graph():
        # Define a variável de estado para controlar se o botão foi clicado
        if "show_graph" not in st.session_state:
            st.session_state.show_graph = False

        # Define a variável para armazenar as opções selecionadas nos filtros
        selected_options = []

        # Cria um botão na barra lateral
        if st.sidebar.button("Filtro Canais de Marketing", key="filtroscanaismarketing"):
            # Muda o valor da variável de estado para True quando o botão for clicado
            st.session_state.show_graph = True

        # Se o botão foi clicado, mostra o gráfico
        if st.session_state.show_graph:
            # Cria um botão multiselect na barra lateral com as opções de canais de marketing
            options = ["TV", "Radio", "Social_Media", "Influencer"]
            selected_options = st.sidebar.multiselect("Selecione os canais de marketing", options, default=options)

            if selected_options:
                # Filtra o dataframe de acordo com as opções selecionadas
                df_grafico02 = df[selected_options + ["Mes/Ano"]]

                # Cria um gráfico de linhas com os canais de marketing selecionados
                fig, ax = plt.subplots(figsize=(10, 6))
                colors = ["blue", "green", "red", "black"]

                for i, col in enumerate(selected_options):
                    ax.plot(df_grafico02["Mes/Ano"], df_grafico02[col], color=colors[i], label=col)

                # Configurações do gráfico
                ax.set_xlabel("Mes/Ano")
                ax.set_ylabel("Vendas")
                ax.set_title("Relação entre Vendas, Tempo e Canais de Marketing")
                ax.legend()

                # Mostra o gráfico no Streamlit
                st.pyplot(fig)
            else:
                st.warning("Selecione pelo menos um canal de marketing")

        # Atualiza a variável de estado quando as opções de filtros são modificadas
        st.session_state.show_graph = bool(selected_options)

    # Chama a função quando o botão é clicado
    show_filtered_graph()


# ------------------------------------------------------------------------------------


def filtro_datas():
    st.title("Filtro de datas")
    # Adicione aqui o conteúdo da página de filtro de datas
    # Criando um filtro do tipo Slider com escolha de períodos de tempo:

    import plotly.express as px
    import datetime as dt

    inicio_padrao = dt.datetime(2010, 1, 1)
    fim_padrao = dt.datetime(2022, 12, 31)

    # Definir valor padrão para datas selecionadas
    inicio_selecionado = inicio_padrao
    fim_selecionado = fim_padrao

    # Criar a barra lateral
    with st.sidebar.expander('Filtro de Datas'):
        inicio_selecionado = st.slider('Selecione a data de início', min_value=inicio_padrao, max_value=fim_padrao, value=inicio_padrao, key='inicio')
        fim_selecionado = st.slider('Selecione a data de fim', min_value=inicio_padrao, max_value=fim_padrao, value=fim_padrao, key='fim')
        
    # Exibir o gráfico
    df_grafico02 = df[(df['Mes/Ano'] >= inicio_selecionado) & (df['Mes/Ano'] <= fim_selecionado)]
    fig = px.line(df_grafico02, x='Mes/Ano', y=['TV', 'Radio', 'Social_Media', 'Influencer'], title='Desempenho de Vendas por Canal de Marketing')
    fig.update_xaxes(title='Mês/Ano')
    fig.update_yaxes(title='Vendas')
    st.plotly_chart(fig, use_container_width=True)


    # Calcular a correlação entre cada canal e as vendas
    correlacoes = df[['TV', 'Radio', 'Social_Media', 'Influencer', 'Vendas']].corr()['Vendas']

    # Mostrar as correlações em ordem decrescente
    print(correlacoes.sort_values(ascending=False))


    # ------------------------------------------------------------------



# Defina as páginas da sua aplicação
pages = {
    "Início": home,
    "Calculadora de ROI": calculadora_roi,
    "Evolução das Vendas": vendas,
    "TV x Vendas": tv_x_vendas,
    "Rádio x Vendas": radio_x_vendas,
    "Social Media x Vendas": social_media_x_vendas,
    "Influencer x Vendas": influencer_x_vendas,
    "Filtro de Canais de Marketing": filtro_canais,
    "Filtro de Datas": filtro_datas
}

# Crie o layout da aplicação com a função streamlit.MultiPage()
def app():
    st.set_page_config(page_title="Trade-Off - ROI Dashboard")
    image = Image.open('logocomplete.png')
    st.sidebar.image(image, width=280)
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Selecione uma página", list(pages.keys()))
    page = pages[selection]
    page()

if __name__ == "__main__":
    app()


def main():
    # Titulo
    st.title("Dashboard para análise e tomada de decisão de ROI")




