import pandas as pd
from haversine import haversine, Unit
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
from datetime import date

st.set_page_config(page_title="Visão Empresa", page_icon=":bar_chart:", layout="wide")
#-----------------------------------------------------------------------------------------------------------------
#                                             funções 
#-----------------------------------------------------------------------------------------------------------------  

def country_maps(df1):
    st.markdown('# Mapa de Entregas por Cidade')
    df_aux = df1_filtrado.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(
    ['City', 'Road_traffic_density'] ).median().reset_index()
    df_aux = df_aux.loc[df_aux ['City'] != 'NaN',:]
    df_aux = df_aux.loc[df_aux ['Road_traffic_density'] != 'NaN',:]

    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
    location_info['Delivery_location_longitude']],
    popup=location_info[['City', 'Road_traffic_density']] ).add_to(map)
    folium_static(map, width=1024, height=600)
    return map



def semana_dias(df1):
        # qunatidade de pedidos por semana / numero unicos de entregadores por semana
        pedidos_por_semana_entregadores01 = df1.loc[:, ['ID','week_of_year']].groupby('week_of_year').count().reset_index()
        pedidos_por_semana_entregadores02 = df1.loc[:, ['Delivery_person_ID','week_of_year']].groupby('week_of_year').nunique().reset_index()

        df_aux = pd.merge(
        pedidos_por_semana_entregadores01,
        pedidos_por_semana_entregadores02,
        on='week_of_year',
        how='inner'
        )


        df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

        fig5 = px.line(df_aux, x='week_of_year', y='order_by_deliver',
         title='Ordens por Entregador',
         labels={'week_of_year': 'Semana do Ano', 'order_by_deliver': 'Pedidos por Entregador'})
        return fig5


def pedidos_por_dia(df1):
    # 2 Quantidades de pedidos por semana
    df1['week_of_year'] = df1['Order_Date'].dt.isocalendar().week
    pedidos_por_semana = df1.groupby('week_of_year').size().reset_index(name='Quantidade de Pedidos')

    # Gráfico em linha da quantidade de pedidos por semana
    fig4 = px.line(pedidos_por_semana, x='week_of_year', y='Quantidade de Pedidos', title='Ordens por Semana')
    return fig4



def pedidos_por_cidade(df1):
    
    
    
            """3 Distribuição dos pedidos por cidade e tipo de tráfego (sem NaN)"""
            # Agrupar os dados por cidade e tipo de tráfego e contar a quantidade de pedidos
            st.markdown('#### Ordens por Cidade')
            pedidos_por_trafego = df1.loc[:, ['ID','City','Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
            pedidos_por_trafego = pedidos_por_trafego.loc[pedidos_por_trafego['City'] != 'NaN', :]
            pedidos_por_trafego = pedidos_por_trafego.loc[pedidos_por_trafego['Road_traffic_density'] != 'NaN', :]

            fig3 = px.scatter(pedidos_por_trafego, x='City', y='Road_traffic_density', size='ID',color='City',)
            return fig3



def traffic_order_share(df1):
            
                # 3 Distribuição dos pedidos por tipo de tráfego (sem NaN e em porcentagem)"""
                # 
                # Agrupar os dados por tipo de tráfego e contar a quantidade de pedidos


                st.markdown('#### Distribuição dos Pedidos por Tipo de Tráfego')
                pedidos_por_trafego = (
                df1_filtrado[df1_filtrado
                            ['Road_traffic_density'] != 'NaN']
                .groupby('Road_traffic_density')
                .size()
                .reset_index(name='Quantidade de Pedidos'))
                    

                # Calcular porcentagem
                total = pedidos_por_trafego['Quantidade de Pedidos'].sum()
                pedidos_por_trafego['Porcentagem'] = (pedidos_por_trafego['Quantidade de Pedidos'] / total * 100).round(2)

            

                fig2 = px.pie(pedidos_por_trafego, values='Porcentagem',names='Road_traffic_density',)
                return fig2





def numero_entregadores(df1):
            # 1 Quantidade de pedidos por dia

            st.markdown('# Ordens por Dia')

            pedidos_por_dia = df1.groupby('Order_Date').size().reset_index(name='ID')
            pedidos_por_dia.head(5)


            # 2 desenhar o grafico de linhas de pedidos por dia

            fig = px.bar(pedidos_por_dia, x='Order_Date', y='ID')
            return fig

#limpeza de dados
def clean_code(df1):
    
    """Este é um código de limpeza de dados que realiza as seguintes operações:
    1. Converte a coluna 'Delivery_person_Age' de texto para número inteiro (int).
    2. Converte a coluna 'Delivery_person_Ratings' de texto para número decimal (float).
    
    3. Converte a coluna 'Order_Date' de texto para data.
    4. Converte a coluna 'multiple_deliveries' de texto para número inteiro (int).
    5. Remove espaços em branco dentro de strings/texto/object.
    6. Limpa a coluna 'Time_taken(min)' extraindo apenas os números e
       convertendo para número inteiro (int).
    7. Remove linhas com valores 'NaN' em colunas específicas.
    8. Retorna o DataFrame limpo.
   """
# 1. Convertendo a coluna Age de texto para número

    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    linhas_selecionad = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionad, :].copy()


    linhas_seleciona = (df1['Weatherconditions'] != 'NaN ')
    df1 = df1.loc[linhas_seleciona, :].copy()


    linhas_selecion = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecion, :].copy()

    linhas_selecio = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecio, :].copy()

    # 2. Convertendo a coluna Ratings de texto para número decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 3. Convertendo a coluna Order_Date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 4. Convertendo multiple_deliveries de texto para número inteiro (int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 5. Removendo os espaços dentro de strings/texto/object
    df1['ID'] = df1['ID'].str.strip()
    df1['Road_traffic_density'] = df1['Road_traffic_density'].str.strip()
    df1['Type_of_order'] = df1['Type_of_order'].str.strip()
    df1['Type_of_vehicle'] = df1['Type_of_vehicle'].str.strip()
    df1['City'] = df1['City'].str.strip()
    df1['Festival'] = df1['Festival'].str.strip()



    #limpando a coluna de time taken 
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.extract(r'(\d+)', expand=False)
    df1['Time_taken(min)'] = pd.to_numeric(df1['Time_taken(min)'], errors='coerce').astype('Int64')

    return df1

#-----------------------------------------------------------------------------------------------------------------
#                                  Inicio da extrutura logica do codigo
#-----------------------------------------------------------------------------------------------------------------

#import data set
df = pd.read_csv('train.csv')
df1 = clean_code(df)







#=====================================================================================================
#                                        BARRA LATERAL
#=====================================================================================================

st.header('Marketplace - visão Cliente ')
image_path = 'logo2.gif'
image = Image.open(image_path)
st.sidebar.image(image, width=200)

st.sidebar.markdown('# Cury Company' )
st.sidebar.markdown('## Fastest Delivery in Town' )
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma data limite' )



start_time = st.sidebar.slider(
    "Até qual valor?",
    value = date(2022, 4, 13),
    min_value = date(2022, 2, 11),
    max_value = date(2022, 4, 6),
    format= 'YYYY,  MM, DD',
    key='start_time_slider'
)
   


st.sidebar.markdown("""___""")

trafic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low','Medium','High','Jam'],
    
)

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered By Decio Carrilho')

# Filtro de data 
start_time = pd.to_datetime(start_time)
linhas_data = df1['Order_Date'] < start_time
df1_filtrado = df1.loc[linhas_data, :]

# Filtro de trânsito
if trafic_options:
    linhas_trafego = df1_filtrado['Road_traffic_density'].isin(trafic_options)
    df1_filtrado = df1_filtrado.loc[linhas_trafego, :]
#st.dataframe(df1_filtrado)
#=====================================================================================================
#                                        LAYOUT STREAMLIT
#=====================================================================================================

tab1,tab2,tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

with tab1:
    with st.container():
        fig = numero_entregadores(df1_filtrado)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig2 = traffic_order_share(df1_filtrado)
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            fig3 = pedidos_por_cidade(df1_filtrado)
            st.plotly_chart(fig3, use_container_width=True)
            
            

with tab2:
    with st.container():
        fig4 = pedidos_por_dia(df1_filtrado)
        st.plotly_chart(fig4, use_container_width=True)

   
    with st.container():
        fig5 = semana_dias(df1_filtrado)
        st.plotly_chart(fig5, use_container_width=True)
        
        

with tab3:
    
    
    fig5 = country_maps(df1_filtrado)
