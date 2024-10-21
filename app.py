import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

def generate_chart(data, title, xlabel, ylabel, color=['orange', 'green']):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(data['labels'], data['values'], color=color)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

def main():
    st.title('Dashboard da Produção de Mel 2023')
    
    # Carregar dados
    uploaded_file = st.file_uploader("Envie o arquivo CSV de produção de mel", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df['Produção 2023 L'] = pd.to_numeric(df['Produção 2023 L'], errors='coerce')
        df['Produção 2023 Kg'] = pd.to_numeric(df['Produção 2023 Kg'], errors='coerce')

        # Filtrar apenas os dados relevantes de produtores e produção total de mel
        produtores_validos = df['PRODUTOR'].dropna()
        producao_total_litros = df['Produção 2023 L'].fillna(0)
        producao_total_kg = df['Produção 2023 Kg'].fillna(0)

        # Garantir que todos os arrays tenham o mesmo comprimento
        produtores_validos = produtores_validos[:min(len(producao_total_litros), len(producao_total_kg))]
        producao_total_litros = producao_total_litros[:len(produtores_validos)]
        producao_total_kg = producao_total_kg[:len(produtores_validos)]

        st.header('Gráfico de Barras da Produção Total em Litros e Quilos (2023)')
        fig1 = generate_chart(
            data={'labels': produtores_validos, 'values': producao_total_litros + producao_total_kg},
            title='Produção Total em Litros e Quilos (2023)',
            xlabel='Produtor',
            ylabel='Produção (L e Kg)',
            color=['green', 'blue']
        )
        st.pyplot(fig1)
        
        # Cálculo da produção total para Litros e Quilos
        producao_total_litros_2023 = producao_total_litros.sum()
        producao_total_kg_2023 = producao_total_kg.sum()
        
        comparacao_data = {
            'labels': ['Produção em Litros 2023', 'Produção em Quilos 2023'],
            'values': [producao_total_litros_2023, producao_total_kg_2023]
        }

        st.header('Gráfico Comparativo da Produção Total em Litros e Quilos (2023)')
        fig2 = generate_chart(
            data=comparacao_data,
            title='Comparativo de Produção (Litros vs Quilos, 2023)',
            xlabel='Unidade de Medida',
            ylabel='Produção Total'
        )
        st.pyplot(fig2)

if __name__ == "__main__":
    main()
