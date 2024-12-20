import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("C:/Volume E/Downloads/Descarte/Analise de dados/US_Accidents_March23Parte1.csv", low_memory=False)

# link do note usado na apresentação https://colab.research.google.com/drive/1nbBtEQ8mPssXChsV8-IZIUCvdfUjhFjQ?usp=sharing#scrollTo=fGkKOUvXqqtG

#### Limpeza de dados Tarefa 1

# Exibir informações iniciais sobre o dataset
print("Informações iniciais do dataset:")
print(df.info())
print("\nResumo dos dados faltantes:")
print(df.isnull().sum())

# Remover duplicatas (se houver)
df_cleaned = df.drop_duplicates()

# Preencher valores faltantes
# Podemos preencher com a média, moda ou usar interpolação, dependendo da coluna
# Exemplo: preenchendo dados numéricos com a média
df_cleaned['Temperature(F)'] = df_cleaned['Temperature(F)'].fillna(df_cleaned['Temperature(F)'].mean())
df_cleaned['Humidity(%)'] = df_cleaned['Humidity(%)'].fillna(df_cleaned['Humidity(%)'].mean())
df_cleaned['Pressure(in)'] = df_cleaned['Pressure(in)'].fillna(df_cleaned['Pressure(in)'].mean())
df_cleaned['Visibility(mi)'] = df_cleaned['Visibility(mi)'].fillna(df_cleaned['Visibility(mi)'].mean())
df_cleaned['Wind_Speed(mph)'] = df_cleaned['Wind_Speed(mph)'].fillna(df_cleaned['Wind_Speed(mph)'].mean())

# Preencher colunas categóricas com a moda
df_cleaned['Weather_Condition'] = df_cleaned['Weather_Condition'].fillna(df_cleaned['Weather_Condition'].mode()[0])

# Verificar novamente valores faltantes após a limpeza
print("\nDados faltantes após limpeza:")
print(df_cleaned.isnull().sum())

# Salvar o dataset limpo em um novo arquivo CSV
df_cleaned.to_csv("US_Accidents_Cleaned.csv", index=False)

print("Limpeza de dados concluída e arquivo salvo como 'US_Accidents_Cleaned.csv'.")


#### Análise Exploratória Tarefa 2

#Identificar Correlações
corr = df.corr(numeric_only=True)

plt.figure(figsize=(12, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1, linecolor='white')
plt.title("Mapa de Correlação entre Variáveis")
plt.show()

#Distribuição de Acidentes por Estado
plt.figure(figsize=(15, 5))
sns.countplot(data=df, x='State', order=df['State'].value_counts().index)
plt.xticks(rotation=90)
plt.title("Distribuição de Acidentes por Estado")
plt.show()

#Acidentes por Tipo de Clima
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='Weather_Condition', order=df['Weather_Condition'].value_counts().head(10).index)
plt.xticks(rotation=45)
plt.title("Top 10 Condições Climáticas Durante Acidentes")
plt.show()

#Análise de Acidentes ao Longo do Tempo
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')

df_cleaned = df.dropna(subset=['Start_Time'])

df_cleaned['YearMonth'] = df_cleaned['Start_Time'].dt.to_period('M')

accidents_over_time = df_cleaned['YearMonth'].value_counts().sort_index()

# Plotar a evolução dos acidentes ao longo do tempo

sns.lineplot(x=accidents_over_time.index.astype(str), y=accidents_over_time.values)

plt.xticks(ticks=range(0, len(accidents_over_time), 6), rotation=45, ha='right')

plt.title("Evolução dos Acidentes ao Longo do Tempo")
plt.xlabel('Ano-Mês')
plt.ylabel('Número de Acidentes')

plt.tight_layout()
plt.show()

#### Visualizações Interativas Tarefa 3

# Visualização básica de um histograma com Seaborn (não interativo)
plt.figure(figsize=(10,6))
sns.histplot(df['Severity'], bins=30, kde=True)
plt.title('Distribuição de Severidade dos Acidentes')
plt.xlabel('Nível de Severidade')
plt.ylabel('Frequência')
plt.show()

# Visualização interativa com Plotly (transformando o gráfico em interativo)
fig = px.histogram(df, x='Severity', nbins=30, title='Distribuição de Severidade dos Acidentes (Interativo)')
fig.update_layout(xaxis_title='Nível de Severidade', yaxis_title='Frequência')
fig.show()

#### Análise Temporal Tarefa 4

df['Start_Time'] = df['Start_Time'].astype(str)
df['End_Time'] = df['End_Time'].astype(str)

df['Start_Time'] = df['Start_Time'].str.replace(r'\.000000000', '', regex=True)
df['End_Time'] = df['End_Time'].str.replace(r'\.000000000', '', regex=True)

df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df['End_Time'] = pd.to_datetime(df['End_Time'], errors='coerce')

invalid_times = df[df['Start_Time'].isna()]
print("Valores inválidos:", invalid_times)

df['Day_of_Week'] = df['Start_Time'].dt.day_name()
df['Hour'] = df['Start_Time'].dt.hour

accidents_by_time = df.groupby(['Day_of_Week', 'Hour']).size().unstack().fillna(0)

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

accidents_by_time = accidents_by_time.reindex(days_order)

plt.figure(figsize=(12, 6))
sns.heatmap(accidents_by_time, cmap='coolwarm', linewidths=.5)
plt.title('Acidentes por Hora do Dia e Dia da Semana')
plt.xlabel('Hora do Dia')
plt.ylabel('Dia da Semana')
plt.show()
