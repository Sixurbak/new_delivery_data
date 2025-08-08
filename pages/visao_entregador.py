import pandas as pd
from haversine import haversine, Unit
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium

from streamlit_folium import folium_static

from datetime import date

st.set_page_config(page_title="Visão Entregador", page_icon=":bar_chart:", layout="wide")
#-----------------------------------------------------------------------------------------------------------------
#                                             funções 
#-----------------------------------------------------------------------------------------------------------------  



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

tab1,tab2,tab3 = st.tabs(['Visão Gerencial','_','_'])

with tab1:
    st.header('Métricas Gerais')
    with st.container():   
        col1,col2,col3,col4 = st.columns(4, gap='large')
        with col1:
            
            maior_idade =('{} Anos'.format(df1_filtrado.loc[:,['Delivery_person_Age']].max().values[0]))
            col1.metric(label='Maior Idade', value=maior_idade)
        with col2:
           
            menor_idade =('{} Anos'.format(df1_filtrado.loc[:,['Delivery_person_Age']].min().values[0]))
            col2.metric(label='Menor Idade', value=menor_idade)
        with col3:
            melhor_condition =('{}'.format(df1_filtrado.loc[:,['Vehicle_condition']].max().values[0]))
            col3.metric(label='Melhor Condição', value=melhor_condition)
        with col4:
            pior_condition =('{}'.format(df1_filtrado.loc[:,['Vehicle_condition']].min().values[0]))
            col4.metric(label='Pior Condição', value=pior_condition)

    with st.container():
        st.markdown("""___""")

        st.header('Avaliações')
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('avaliações médias por entregador')
            range_median_entregador = df1_filtrado.loc[:,['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(range_median_entregador.head(15), width=500, height=473)

        with col2:
            st.subheader('avaliações médias por clima')
            avali_media_clima = (
                df1_filtrado.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                .groupby('Weatherconditions')
                .agg({'Delivery_person_Ratings': ['mean', 'std']})
            )
            avali_media_clima.columns = ['deliveri_mean', 'avaliacao_media']
            avali_media_clima.reset_index(inplace=True)
            st.dataframe(avali_media_clima.head(4))

            st.subheader('avaliações médias por transito')
            range_median_trafego = df1_filtrado.loc[:,['Road_traffic_density','Delivery_person_Ratings']].groupby('Road_traffic_density').mean().reset_index()
            st.dataframe(range_median_trafego)

    with st.container():
        st.markdown("""___""")

        st.header('Velocidade de Entrega')
        col1,col2 = st.columns(2)
        with col1:
            
        
                
            st.subheader('Top entregas rapidas')
            df2 = df1_filtrado.loc [:, ['Delivery_person_ID', 'City', 'Time_taken(min)' ]].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'],ascending=True                                                                                                                              ).reset_index()
            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] =='Semi-Urban', :].head(10)
            df3 = pd.concat([df_aux01, df_aux02, df_aux03] ).reset_index(drop=True)
            st.dataframe(df3)
        with col2:
            st.subheader('Entregas mais lentas')
            df2 = df1_filtrado.loc [:, ['Delivery_person_ID', 'City', 'Time_taken(min)' ]].groupby(['City', 'Delivery_person_ID']).max().sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index()
            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] =='Semi-Urban', :].head(10)
            df3 = pd.concat([df_aux01, df_aux02, df_aux03] ).reset_index(drop=True)

            st.dataframe(df3)
