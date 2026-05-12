import pandas as pd

df = pd.read_csv('data/train.csv')

# passo 6.1 tratamento das colunas
# renomeação das colunas para snake_case
mapeamento_colunas = {
    'PassengerId': 'id_passageiro',
    'Survived': 'sobreviveu',
    'Pclass': 'classe_pax',
    'Name': 'nome',
    'Sex': 'sexo',
    'Age': 'idade',
    'SibSp': 'irmaos_conjuges',
    'Parch': 'pais_filhos',
    'Ticket': 'bilhete',
    'Fare': 'tarifa',
    'Cabin': 'cabine',
    'Embarked': 'porto_embarque'
}

df.rename(columns=mapeamento_colunas, inplace=True)

colunas_categoricas = ['sexo', 'porto_embarque', 'classe_pax', 'sobreviveu']

for coluna in colunas_categoricas:
    df[coluna] = df[coluna].astype('category')

print(df.info())

# passo 6.2 tratamento de nulos

df['cabine'] = df['cabine'].fillna('Nao_Informado')

moda_porto = df['porto_embarque'].mode()[0]

df['porto_embarque'] = df['porto_embarque'].fillna(moda_porto)

df['idade'] = df['idade'].fillna(
    df.groupby(['classe_pax', 'sexo'])['idade'].transform('median')
)


print("\n--- Contagem de valores nulos após o tratamento ---")
print(df.isnull().sum())

# passo 6.3 Engenharia de Variáveis 

# 1. Variável: tamanho_familia
# SibSp = irmãos/cônjuges
# Parch = pais/filhos
# +1 = o próprio passageiro

df['tamanho_familia'] = df['irmaos_conjuges'] + df['pais_filhos'] + 1

# 2. Variável: viajava_sozinho
# Se tamanho_familia == 1 → viajava sozinho

df['viajava_sozinho'] = df['tamanho_familia'].apply(lambda x: 'Sim' if x == 1 else 'Não')

# 3. Variável: titulo_social
# Extraindo o título do nome (Mr, Miss, Mrs, Dr, etc.)

# 3. Variável: titulo_social
# Extraindo o título do nome e agrupando os incomuns em 'outros'
def extrair_titulo(nome):
    titulo = nome.split(',')[1].split('.')[0].strip()
    titulos_comuns = ['Mr', 'Miss', 'Mrs', 'Master']
    if titulo in titulos_comuns:
        return titulo
    else:
        return 'Outros'

df['titulo_social'] = df['nome'].apply(extrair_titulo)

# Visualizar resultado
print(df[['nome', 'irmaos_conjuges', 'pais_filhos', 'tamanho_familia', 'viajava_sozinho', 'titulo_social']].head())

# passo 6.4 normalização e agregações

# faixas etárias
def classificar_faixa_etaria(idade):
    if idade <= 12:
        return 'Criança'
    elif idade <= 17:
        return 'Adolescente'
    elif idade <= 59:
        return 'Adulto'
    else:
        return 'Idoso'

df['faixa_etaria'] = df['idade'].apply(classificar_faixa_etaria)
df['faixa_etaria'] = df['faixa_etaria'].astype('category')

# taxas de sobrevivência agregadas por segmento
sobrevivencia_classe = df.groupby('classe_pax', observed=True)['sobreviveu'].apply(
    lambda x: (x.astype(int).sum() / len(x) * 100).round(1)
).reset_index()
sobrevivencia_classe.columns = ['classe_pax', 'taxa_sobrevivencia']

sobrevivencia_sexo = df.groupby('sexo', observed=True)['sobreviveu'].apply(
    lambda x: (x.astype(int).sum() / len(x) * 100).round(1)
).reset_index()
sobrevivencia_sexo.columns = ['sexo', 'taxa_sobrevivencia']

sobrevivencia_faixa = df.groupby('faixa_etaria', observed=True)['sobreviveu'].apply(
    lambda x: (x.astype(int).sum() / len(x) * 100).round(1)
).reset_index()
sobrevivencia_faixa.columns = ['faixa_etaria', 'taxa_sobrevivencia']

print("\n--- Taxa de sobrevivência por classe ---")
print(sobrevivencia_classe)
print("\n--- Taxa de sobrevivência por sexo ---")
print(sobrevivencia_sexo)
print("\n--- Taxa de sobrevivência por faixa etária ---")
print(sobrevivencia_faixa)

# passo 6.5 geração da base final
import os

os.makedirs('data/processed', exist_ok=True)
df.to_csv('data/processed/titanic_cleaned.csv', index=False)

print("\n--- Base final gerada com sucesso ---")
print(f"Arquivo salvo em: data/processed/titanic_cleaned.csv")
print(f"Shape final do dataframe: {df.shape}")
print(f"\nColunas disponíveis:\n{list(df.columns)}")
