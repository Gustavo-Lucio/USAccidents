import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Volume E/Downloads/Descarte/Analise de dados/US_Accidents_March23_v1.csv", low_memory=False)


#### Análise Exploratória Tarefa 2

#Identificar Correlações
corr = df.corr(numeric_only=True)

plt.figure(figsize=(12, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Mapa de Correlação entre Variáveis")
plt.show()

#Análise de Padrões
plt.figure(figsize=(15, 5))
sns.countplot(data=df, x='State', order=df['State'].value_counts().index)
plt.xticks(rotation=90)
plt.title("Distribuição de Acidentes por Estado")
plt.show()

#Tipo de Clima
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='Weather_Condition', order=df['Weather_Condition'].value_counts().head(10).index)
plt.xticks(rotation=45)
plt.title("Top 10 Condições Climáticas Durante Acidentes")
plt.show()

#Análise de Acidentes ao Longo do Tempo
df['Start_Time'] = pd.to_datetime(df['Start_Time'])

df['YearMonth'] = df['Start_Time'].dt.to_period('M')

accidents_over_time = df['YearMonth'].value_counts().sort_index()

plt.figure(figsize=(12, 5))
sns.lineplot(x=accidents_over_time.index.astype(str), y=accidents_over_time.values)
plt.xticks(rotation=45)
plt.title("Evolução dos Acidentes ao Longo do Tempo")
plt.show()