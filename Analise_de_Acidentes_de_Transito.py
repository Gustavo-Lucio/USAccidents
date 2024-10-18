import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Volume E/Downloads/Descarte/Analise de dados/US_Accidents_March23.csv", low_memory=False)

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