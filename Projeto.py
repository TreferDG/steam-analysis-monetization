"""
Projeto: Análise de Monetização e Engajamento de Gêneros na Steam
Autor: Danilo
Descrição: Pipeline em Python/Pandas para limpeza, desmembramento de gêneros híbridos,
           filtragem de softwares utilitários e agregação de métricas de engajamento (tempo de jogo).
"""

import pandas as pd

# 1. Carregamento do dataset
df = pd.read_csv('games.csv')

# 2. Seleção de colunas e limpeza inicial
df_analise = df[['AppID', 'Genres', 'Price', 'Average playtime forever', 'Positive', 'Negative']]
df_analise['Total_Avaliacoes'] = df_analise['Positive'] + df_analise['Negative']

df_analise = df_analise.dropna()
df_analise = df_analise[df_analise['Total_Avaliacoes'] > 0]

# 3. Tratamento de Gêneros Híbridos (.explode)
df_analise['Genero_Lista'] = df_analise['Genres'].str.split(',')
df_analise = df_analise.explode('Genero_Lista')
df_analise['Genero_Lista'] = df_analise['Genero_Lista'].str.strip()

# 4. Filtro de Softwares e Utilitários
softwares_utilitarios = [
    'Audio Production', 'Web Publishing', 'Video Production', 
    'Utilities', 'Software Training', 'Animation & Modeling', 
    'Design & Illustration', 'Photo Editing', 'Education', 'Game Development','Massively Multiplayer'
]

df_apenas_jogos = df_analise[~df_analise['Genero_Lista'].isin(softwares_utilitarios)].copy()

# 5. Agrupamento e Métricas de Engajamento
top_generos = df_apenas_jogos.groupby('Genero_Lista').agg(
    Qtd_Jogos=('AppID', 'count'),
    Tempo_Medio_Minuto=('Average playtime forever', 'mean'),
    Total_Positivas=('Positive', 'sum'),
    Total_Avaliacoes=('Total_Avaliacoes', 'sum')
)

# 6. Conversões, Arredondamentos e Seleção do Top 10
top_generos['Taxa_Aprovacao_Pct'] = (top_generos['Total_Positivas'] / top_generos['Total_Avaliacoes']) * 100
top_generos['Taxa_Aprovacao_Pct'] = top_generos['Taxa_Aprovacao_Pct'].round(2)

top_generos['Tempo_Medio_Minuto'] = top_generos['Tempo_Medio_Minuto'].round(0)

top_10_jogos = top_generos.sort_values(by='Tempo_Medio_Minuto', ascending=False).head(10)

# Exibição do resultado no terminal
print(top_10_jogos)

top_10_jogos.to_csv('top_10_generos_steam.csv', index=False)
print("Ficheiro 'top_10_generos_steam.csv' gerado com sucesso!")