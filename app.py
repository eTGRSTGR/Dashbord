import pandas as pd
import streamlit as st
import plotly.express as px

# Load data from CSV file
df = pd.read_csv('/Producao_de_mel_2023_limpo.csv')

# Streamlit app setup
st.set_page_config(page_title='Dashboard de Produção de Mel', layout='wide')
st.title('Operação - Produção de Mel 2023')

# Sidebar filters
st.sidebar.header('Filtros')
produtor_selecionado = st.sidebar.multiselect('Selecionar Produtores', df['PRODUTOR'].unique())

# Apply filters if any
if produtor_selecionado:
    df = df[df['PRODUTOR'].isin(produtor_selecionado)]

# KPI cards
st.header('Hoje')
col1, col2, col3, col4 = st.columns(4)

# Calcular KPIs
total_producao_kg = df['Produção 2023 Kg'].sum()
total_colmeias = df['Qntd. Colmeia'].sum()
total_colmeias_produtivas = df['Qntd. Colmeia produtiva'].sum()
media_coe = df['COE'].mean()

# Display KPIs
col1.metric('Produção Total (Kg)', f"{total_producao_kg:.2f} Kg")
col2.metric('Total de Colmeias', int(total_colmeias))
col3.metric('Colmeias Produtivas', int(total_colmeias_produtivas))
col4.metric('Média COE', f"R$ {media_coe:.2f}")

# Produção por produtor
st.header('Produção por Produtor')
for produtor in df['PRODUTOR'].unique():
    produtor_data = df[df['PRODUTOR'] == produtor]
    st.subheader(produtor)
    col1, col2, col3 = st.columns(3)
    col1.metric('Produção Total (Kg)', f"{produtor_data['Produção 2023 Kg'].sum():.2f} Kg")
    col2.metric('Colmeias', int(produtor_data['Qntd. Colmeia'].sum()))
    col3.metric('COE', f"R$ {produtor_data['COE'].mean():.2f}")

# Produção Mensal
st.header('Produção Mensal')
fig = px.bar(df.groupby('PRODUTOR', as_index=False).sum(), x='PRODUTOR', y='Produção 2023 Kg', title='Produção Total por Produtor')
st.plotly_chart(fig)

# SLA (indicador fictício para exemplo)
sla = 99.68
st.header('SLA')
st.metric('SLA', f"{sla}%")

# Gráfico de Produção por Colheita
st.header('Produção por Colheita')
df_melted = df.melt(id_vars=['PRODUTOR'], value_vars=['1ª Colheita', '2ª  Colheita', '3ª  Colheita', '4ª  Colheita', '5ª  Colheita', '6ª Colheita'], 
                    var_name='Colheita', value_name='Produção (Kg)')
df_melted.dropna(inplace=True)
fig = px.bar(df_melted, x='Colheita', y='Produção (Kg)', color='PRODUTOR', barmode='group', title='Produção por Colheita')
st.plotly_chart(fig)

# Gráfico de Colmeias Produtivas
st.header('Colmeias Produtivas por Produtor')
fig = px.pie(df, values='Qntd. Colmeia produtiva', names='PRODUTOR', title='Distribuição de Colmeias Produtivas por Produtor')
st.plotly_chart(fig)

# Tabela de Detalhes
st.header('Detalhes da Produção')
st.dataframe(df)
