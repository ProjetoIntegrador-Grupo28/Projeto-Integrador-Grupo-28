## Projeto Integrador - Grupo 28: Análise de Sobrevivência do Titanic

## 1. Tema do Projeto
*Análise de sobrevivência dos passageiros do RMS Titanic para identificação de padrões demográficos e socioeconômicos.*

## 2. Integrantes do Grupo
* **Vitor** - [(https://github.com/vitorhugoml)]
* **Karla** - [(https://github.com/karlam-lgtm)]
* **Natalia** - [(https://github.com/natrod141-coder)]
* **Matheus** - [(https://github.com/MatheusEduardo10)]
* **Isabella** - [(https://github.com/Bellasguarden)]
* **Emerson** - [(https://github.com/emerson-maker)]
* **Pedro** - [(https://github.com/pedrovilaca97)]

## 3. Acesso ao Dashboard 

## 3.1 (Online)

O painel interativo está disponível na nuvem para acesso imediato. Para explorar os dados e gráficos sem necessidade de instalação, utilize o link abaixo:

- **[Clique aqui para acessar o Dashboard do Titanic no Streamlit](COLOQUE_O_LINK_DO_STREAMLIT_AQUI)**

## 3.2 Como executar a aplicação localmente

Para rodar este projeto na sua máquina, certifique-se de ter o Python instalado. Depois, siga as etapas abaixo no seu terminal:

- **Clone o repositório e entre na pasta do projeto:**
  ```bash
  git clone [https://github.com/ProjetoIntegrador-Grupo28/Projeto-Integrador-Grupo-28.git](https://github.com/ProjetoIntegrador-Grupo28/Projeto-Integrador-Grupo-28.git)
  cd Projeto-Integrador-Grupo-28

- **Crie o ambiente virtual (venv):**
  Isso garante que o projeto rode em um ambiente isolado.
  ```bash
  python -m venv venv

**Ative o ambiente virtual:**
- Se estiver usando Windows (PowerShell):
 .\venv\Scripts\Activate.ps1

- Se estiver usando Mac ou Linux:
    ```bash
    source venv/bin/activate

- **Instale as dependências do projeto**
Com o ambiente ativado, instale as bibliotecas listadas no arquivo de requisitos:
- pip install -r requirements.txt

- **Execute o Dashboard:**
  Inicie a aplicação utilizando o Streamlit:
  ```bash
  streamlit run APP/app.py

## 4. Objetivo da Análise. 
Identificar quais fatores (como classe, idade e sexo) foram determinantes para a sobrevivência no naufrágio. A base utilizada é a "Titanic - Machine Learning from Disaster" do Kaggle.

## 5. Planejamento das Tarefas (Cronograma)
| Integrante | Atividade | Prazo | 
| :--- | :--- | :--- |
| **Matheus, Natália e Emerson** | ETL e processamento de dados | 24-04-2026 |
| **Vitor + Isabella/Pedro + Karla/Matheus + Natália** | Dashboard Streamlit  | 05-05-2026 |
| **Vitor** | Publicação no Streamlit Cloud  | 06/10-05-2026 |
| **Todos os integrantes** | Testes do streamlit | 06/10-05-2026 |
| **Karla, Emerson, Pedro e Natália** | Revisão final e atualização do README | 16/05/2026 |

## 6. Base de Dados
* **Fonte:** https://www.kaggle.com/datasets/dimplebathija/titanic-machine-learning-from-disaster
* **Contexto:** Titanic: Machine Learning from Disaster

O dataset Titanic – Machine Learning from Disaster, disponível na plataforma Kaggle, é um dos conjuntos de dados mais famosos utilizados para aprendizado de Ciência de Dados e Machine Learning. Ele contém informações sobre os passageiros que estavam a bordo do navio Titanic durante sua viagem inaugural em 1912, quando a embarcação colidiu com um iceberg e afundou no Oceano Atlântico. Esse desastre resultou em grande perda de vidas e se tornou um dos naufrágios mais conhecidos da história.

O objetivo principal desse dataset é permitir que pesquisadores e estudantes desenvolvam modelos de aprendizado de máquina capazes de prever quais passageiros sobreviveram ao desastre, com base em diferentes características presentes nos dados. Entre essas características estão fatores como idade, sexo, classe do passageiro, valor da passagem, número de familiares a bordo e porto de embarque.

O conjunto de dados é dividido em três arquivos principais:

train.csv: contém os dados dos passageiros juntamente com a informação de sobrevivência, sendo utilizado para treinar modelos de machine learning.

test.csv: possui os mesmos atributos, porém sem o resultado de sobrevivência, sendo utilizado para testar a capacidade de previsão do modelo desenvolvido.

gender_submission.csv: funciona como um gabarito de formato, servindo exclusivamente para orientar a criação do arquivo de submissão final do projeto, e não como fonte de dados para aprendizado de máquina.

A análise desses dados permite identificar padrões importantes relacionados à sobrevivência no Titanic. Estudos realizados com esse dataset indicam que fatores como gênero, idade e classe social tiveram forte influência nas chances de sobrevivência. Por exemplo, mulheres, crianças e passageiros de classes mais altas tiveram maior probabilidade de sobreviver em comparação com homens adultos e passageiros de classes mais baixas.

Dessa forma, o dataset Titanic é amplamente utilizado em projetos educacionais e competições de ciência de dados, pois permite aplicar diversas técnicas como análise exploratória de dados, limpeza de dados, engenharia de atributos e construção de modelos preditivos. Além de servir como introdução prática ao aprendizado de máquina, ele também ajuda a compreender como os dados podem revelar padrões e apoiar a tomada de decisões baseada em evidências.

## 7. Transformações Planejadas (Processamento com Pandas)

### 7.1 Padronização e Limpeza de Dados

| Ação | Descrição |
| :--- | :--- |
| **Renomeação de Colunas** | Tradução e padronização para `snake_case` (ex: `PassengerId` → `id_passageiro`, `Pclass` → `classe_pax`) |
| **Ajuste de Tipagem** | Conversão de variáveis categóricas (como porto de embarque) para o tipo `category`, reduzindo uso de memória |

---

### 7.2 Tratamento de Dados Ausentes (Data Imputation)

| Coluna | Estratégia | Justificativa |
| :--- | :--- | :--- |
| **Age** (Idade) | Preenchimento com a mediana agrupada por Classe e Sexo | Evita que a média geral ignore diferenças de perfil entre as cabines |
| **Embarked** (Porto) | Preenchimento com a moda — Porto `"S"` (Southampton) | É o ponto de partida da maioria dos passageiros |
| **Cabin** (Cabine) | Criação da categoria sinalizadora `"Nao_Informado"` | Transforma a ausência do dado em variável de análise |

---

### 7.3 Engenharia de Variáveis (Feature Engineering)

> Novas métricas que não existem no dataset original, mas que são cruciais para o Dashboard.

| Nova Variável | Origem | Descrição |
| :--- | :--- | :--- |
| `tamanho_familia` | `SibSp` + `Parch` + 1 | Representa o total de familiares a bordo incluindo o próprio passageiro |
| `viajava_sozinho` | Derivada de `tamanho_familia` | Variável binária (`Sim` / `Não`) |
| `titulo_social` | Extraída da coluna `Name` | Captura prefixos como `Mr.`, `Miss.`, `Master.`, `Dr.` para análise de status social |

---

### 7.4 Normalização e Agregações

| Transformação | Detalhamento |
| :--- | :--- |
| **Faixas Etárias** | `Criança` (0–12) · `Adolescente` (13–17) · `Adulto` (18–59) · `Idoso` (60+) |
| **Métricas de Sobrevivência** | Tabelas agregadas com Taxa de Sobrevivência (%) segmentada por classe, gênero e faixa etária para alimentação direta dos gráficos |

---

### 7.5 Geração da Base Final
```
/data/processed/titanic_cleaned.csv
```

> O arquivo final será a fonte de dados única e otimizada utilizada pelo Dashboard, consolidando todas as transformações acima.

## 8. Ideia Inicial do Dashboard (Métricas e Visualizações)

### 8.1 Métricas Gerais (KPIs)

| Métrica | Descrição |
| :--- | :--- |
| **Taxa de Sobrevivência Geral (%)** | Percentual total de sobreviventes em relação ao total de passageiros |
| **Total de Passageiros** | Contagem geral separada entre sobreviventes e não sobreviventes |
| **Média de Idade** | Comparativo de média de idade entre sobreviventes e não sobreviventes |
| **Taxa de Sobrevivência por Gênero (%)** | Percentual de sobrevivência separado entre homens e mulheres |

---

### 8.2 Visualizações Planejadas

| # | Visualização | Tipo | Variável Utilizada | Objetivo |
| :---: | :--- | :---: | :--- | :--- |
| 1 | Sobrevivência por Classe Social | Barras Agrupadas | `classe_pax` | Evidenciar o impacto do status socioeconômico |
| 2 | Sobrevivência por Gênero | Pizza / Donut | `sexo` | Reforçar o padrão "mulheres e crianças primeiro" |
| 3 | Sobrevivência por Faixa Etária | Barras | `faixa_etaria` | Verificar a influência da idade nas chances de sobrevivência |
| 4 | Sobrevivência por Título Social | Barras Horizontais | `titulo_social` | Analisar se o título influenciou na prioridade de salvamento |
| 5 | Sobrevivência por Tamanho de Família | Linha / Barras | `tamanho_familia` | Verificar se viajar acompanhado impactou a sobrevivência |
| 6 | Passageiros que Viajavam Sozinhos | Pizza | `viajava_sozinho` | Comparar taxa de sobrevivência entre passageiros sozinhos e acompanhados |
| 7 | Sobrevivência por Porto de Embarque | Barras | `porto_embarque` | Analisar correlação entre porto de embarque e sobrevivência |

---

### 8.3 Filtros Interativos Previstos

| Filtro | Opções |
| :--- | :--- |
| **Classe** | 1ª, 2ª, 3ª |
| **Gênero** | Masculino, Feminino |
| **Faixa Etária** | Criança, Adolescente, Adulto, Idoso |
| **Viajava Sozinho** | Sim, Não |