#🏨 Visão Restaurante

import pandas as pd
from haversine import haversine, Unit
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
import numpy as np

from streamlit_folium import folium_static

from datetime import date

st.set_page_config(page_title="Visão Restaurante", layout="wide")
#-----------------------------------------------------------------------------------------------------------------
#                                             funções 
#-----------------------------------------------------------------------------------------------------------------  
def dest_city(df1):
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
    df_aux.columns = ['City', 'Road_traffic_density', 'avg_time', 'std_time']
    fig = px.sunburst(
        df_aux,
        path=['City', 'Road_traffic_density'],
        values='avg_time',
        color='std_time',
        color_continuous_scale='RdBu',
        color_continuous_midpoint=np.average(df_aux['std_time'])
    )
    return fig



def dist_city(df1):
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude', 'City']
    df1 = df1.loc[:, cols].copy()
    df1['distance'] = df1.apply(
        lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']),
            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
                ), axis=1
            )
    avg_distance = df1.groupby('City')['distance'].mean().reset_index()
    fig2 = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
    fig2.update_layout(width=400, height=400, margin=dict(l=0, r=0, t=0, b=0))  # aumenta o tamanho do gráfico
    return fig2



def alt_graph_size(df1):
        cols = ['City', 'Time_taken(min)']
        df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
        df_aux.columns = ['City', 'avg_time', 'std_time']
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Tempo Médio',
            x=df_aux['City'],
            y=df_aux['avg_time'],
            error_y=dict(type='data', array=df_aux['std_time'])
        ))
        fig.update_layout(barmode='group', width=700, height=400)
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
    min_value = date(2022, 2, 13),
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

tab1,tab2,tab3,tab4 = st.tabs(['Visão Gerencial','_','_','_'])

with tab1:
    st.header('Métricas Gerais')
    with st.container():   
        col1,col2,col3,col4,tab5,tab6 = st.columns(6)
        with col1:
            
            entrega_unico = df1_filtrado['Delivery_person_ID'].nunique()
            col1.metric(label='Entregadores únicos', value=entrega_unico)

        with col2:
           
            col = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df1_filtrado['distancia'] = df1_filtrado.loc[:, col].apply(
                lambda x: haversine(
                    (x['Restaurant_latitude'], x['Restaurant_longitude']),
                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            distancia_media = int(np.around(df1_filtrado['distancia'].mean(), 0))
            col2.metric(label='Distância Média', value=f'{distancia_media} Km')
            
        with col3:
            time_mid = ['Time_taken(min)', 'Festival']

            df_aux = df1_filtrado.loc[:, time_mid].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()

            df_aux.columns = ['Festival', 'avg_time', 'Time_std']

            linhas_select = df_aux['Festival'] == 'Yes'
            df_aux = df_aux.loc[linhas_select, :]

            df_aux = df_aux.reset_index(drop=True)

            tempo_medio_festival = int(np.round(df_aux['avg_time'].values[0], 0))
            col3.metric(label='Tempo Médio / Festival', value=f'{tempo_medio_festival} Min')

        with col4:
            time_mid = ['Time_taken(min)', 'Festival']

            df_aux = df1_filtrado.loc[:, time_mid].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()

            df_aux.columns = ['Festival', 'avg_time', 'std_time']

            linhas_select = df_aux['Festival'] == 'Yes'
            df_aux = df_aux.loc[linhas_select, :]

            desvio_padrao_festival = int(np.round(df_aux['std_time'].values[0], 0))
            col4.metric(label='Desvio Padrão / Festival', value=f'{desvio_padrao_festival} Min')
        
        with tab5:
            
            time_mid = ['Time_taken(min)', 'Festival']

            df_aux = df1_filtrado.loc[:, time_mid].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()

            df_aux.columns = ['Festival', 'avg_time', 'std_time']

            linhas_select = df_aux['Festival'] == 'No'
            df_aux = df_aux.loc[linhas_select, :]

            tempo_medio_sem_festival = int(np.round(df_aux['avg_time'].values[0], 0))
            tab5.metric(label='Tempo Médio / Sem Festival', value=f'{tempo_medio_sem_festival} Min')
            
        with tab6:
            
            time_mid = ['Time_taken(min)', 'Festival']

            df_aux = df1_filtrado.loc[:, time_mid].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()

            df_aux.columns = ['Festival', 'avg_time', 'std_time']

            linhas_select = df_aux['Festival'] == 'No'
            df_aux = df_aux.loc[linhas_select, :]

            desvio_padrao_sem_festival = int(np.round(df_aux['std_time'].values[0], 0))
            tab6.metric(label='Desvio Padrão / Sem Festival', value=f'{desvio_padrao_sem_festival} Min')
   
    with st.container():
        st.markdown("""___""")
        st.header('Avaliação dos Entregadores')
        

        # Define largura e altura fixas para o gráfico
        largura = 1200
        altura = 400
        fig = alt_graph_size(df1_filtrado)
        fig.update_layout(width=largura, height=altura)
        st.plotly_chart(fig, use_container_width=False)

       
    with st.container():
        st.markdown("""___""")
        st.header('Avaliação dos Entregadores')
        # Cria duas colunas de largura igual para alinhar gráficos e descrições
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("#### Distância Média por Cidade")
            fig2 = dist_city(df1_filtrado)
            fig2.update_layout(width=400, height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig2, use_container_width=False)
        with col2:
            st.markdown("#### Avaliação por Cidade e Trânsito")
            fig = dest_city(df1_filtrado)
            fig.update_layout(width=400, height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=False)
            
    with st.container():
        st.markdown("""___""")
        st.header('Tempo Médio de Entrega por Cidade')
        time_mid = ['City','Time_taken(min)','Type_of_order']

        df_aux = df1_filtrado.loc[:, time_mid].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()

        df_aux.columns = ['City', 'Type_of_order', 'Time_mean', 'Time_std']
        df_aux = df_aux.sort_values(['City', 'Time_mean'], ascending=True).reset_index(drop=True)
        
        # Adiciona uma borda à esquerda para centralizar
        col_space, col_table, col_space2 = st.columns([2, 3, 2])
        with col_table:

            st.dataframe(df_aux, width=500, height=473)
