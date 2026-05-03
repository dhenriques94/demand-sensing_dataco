# Otimização Preditiva de Inventário: Impacto do Demand Sensing na Prevenção de Ruturas

## 📌 Resumo do Projeto
Este projeto foca-se na prototipagem e validação de um sistema preditivo de *Demand Sensing* para a DataCo. O objetivo é investigar e demonstrar que a integração de sinais de intenção digital (tráfego e navegação web) com o histórico transacional permite transitar de uma gestão de inventário reativa para um sistema proativo.

## ⚠️ O Problema de Negócio e a Lacuna do ERP
A empresa sofria com uma gestão baseada na inércia (olhar para o histórico de vendas passado). Uma vez que o ERP apresentava lacunas profundas na identificação direta de stock (a variável *Product Status* possuía zero variância), foi construída uma "Proxy de Rutura" e um "Score de Viabilidade" para isolar o *Top 5* de produtos mais críticos do catálogo. No cenário base de avaliação, esta gestão reativa culminou num volume crítico de 161 unidades em rutura numa única semana.

## 🧠 A Solução Tecnológica
Desenvolveu-se um motor preditivo (*Random Forest Regressor*) para atuar como um radar de intenção de compra, enriquecido através de Engenharia de Atributos (criação de *lags* de cliques e médias móveis temporais).
*   **Linguagem:** Python
*   **Machine Learning:** Scikit-Learn (*Random Forest Regressor* com `max_depth=5` para regularização e estabilidade matemática)
*   **Simulação Logística:** *Dashboard* executivo interativo construído em Streamlit

## 📊 Resultados Principais (Stress-Test de 7 Dias)
*   **Precisão Estatística:** O modelo atingiu um $R^2$ de **72.2%** em dados estritamente de teste, superando largamente a heurística do *Baseline* simples (que explicava apenas 37.7% da volatilidade).
*   **Eficiência Operacional:** Num cenário com um *Lead Time* exigente fixado em 6 dias, o modelo reduziu os incidentes críticos logísticos em **74.5%** (passando de 161 para apenas 41 falhas face à realidade histórica).
*   **Retorno Financeiro (ROI):** A antecipação inteligente da procura evitou a disrupção severa na entrega e gerou uma Receita Protegida de **$18.128,69**.

## 🚀 Como Executar Localmente
1. Clonar o repositório.
2. Instalar dependências necessárias: `pip install -r requirements.txt`
3. Executar o protótipo localmente: `streamlit run app/app.py` *(ajustar caminho consoante a pasta)*

> **Nota sobre os Dados:** Devido às restrições de tamanho do GitHub e boas práticas de versionamento, os *datasets* originais em `.csv` não estão incluídos neste repositório. A pasta de dados completa encontra-se disponível no diretório *Cloud* partilhado diretamente com o júri.
