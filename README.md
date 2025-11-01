# 🛢️ Pretoleira Gamarra — Simulação de Dados de uma Empresa Fictícia de Petróleo

**Pretoleira Gamarra** é um projeto de ciência de dados que simula de forma realista a operação e finanças de uma empresa fictícia de petróleo no Brasil. O objetivo é gerar **datasets mensais de 2005 a 2025** com informações de produção, preços, custos e lucros, permitindo análises financeiras, validações de dados e previsões futuras usando Python.

---

## 🚀 Objetivos do Projeto

- Criar **datasets fictícios realistas** de uma empresa de petróleo brasileira.  
- Gerar séries históricas de produção, receita, custos e lucro, com **sazonalidade, ruído e curvas de produção realistas**.  
- Permitir **sanity checks e validação de dados** para garantir consistência.  
- Facilitar a **análise e visualização** em Power BI ou Python.  
- Servir como base para **projetos de machine learning** em previsão financeira ou produção de petróleo.

---

## 🗂 Estrutura do Projeto

pretoleira_gamarra/
│
├── src/
│ ├── data_generation/
│ │ ├── generate_preco_petroleo.py # Gera séries históricas de preço do petróleo
│ │ ├── generate_cambio.py # Gera séries históricas de câmbio USD/BRL
│ │ ├── generate_campos.py # Cria dados de campos petrolíferos fictícios
│ │ ├── generate_producao_mensal.py # Calcula produção mensal e receita por campo
│ │ ├── generate_custos.py # Calcula custos operacionais e gerais
│ │ └── compute_financials.py # Calcula lucro líquido e consolida agregados
│ │
│ └── utils/
│ └── sanity_checks.py # Sanity checks e geração de relatórios
│
├── notebooks/
│ ├── 01_generate_data.ipynb
│ ├── 02_gerar_producao_mensal.ipynb
│ ├── 03_gerar_custos.ipynb
│ ├── 04_compute_financials.ipynb
│ └── 05_sanity_checks.ipynb
│
├── data/
│ ├── raw/ # Dados brutos intermediários (Excel, CSV)
│ └── processed/ # Agregados consolidados e dados finais
│
└── docs/
└── data_dictionary.md # Descrição detalhada das colunas

---

## 🛠 Funcionalidades

1. **Gerar dados base**  
   - Preço do barril em USD com séries mensais de 2005 a 2025  
   - Taxa de câmbio USD/BRL mensal  
   - Campos petrolíferos fictícios (nome, estado, tipo de petróleo, capacidade)

2. **Produção mensal por campo**  
   - Curva de produção: rampa inicial, pico, declínio e estabilização  
   - Sazonalidade e ruído aplicados para maior realismo  
   - Receita calculada como `volume_barris * preco_brl`

3. **Custos operacionais e gerais**  
   - Custo variável por barril + custo fixo proporcional à capacidade  
   - Custos gerais administrativos, logísticos e de manutenção com inflação e sazonalidade  
   - Margem bruta e lucro líquido calculados por campo

4. **Consolidação financeira**  
   - Lucro líquido por campo: `receita - custo_operacional - share_custos_gerais`  
   - Agregados mensais consolidados para Power BI  
   - Sanity checks automáticos: cobertura de datas, valores ausentes, correlações

---

## 📊 Saída / Entregáveis

- `data/raw/producao_mensal.xlsx` — Produção mensal por campo com receita, custos e lucro  
- `data/raw/custos_gerais.xlsx` — Custos gerais mensais  
- `data/processed/financials_consolidated.xlsx` — Agregados consolidados para análises e Power BI  
- `docs/data_dictionary.md` — Dicionário de dados detalhado  
- `docs/sanity_report.txt` — Relatório de sanity checks

---

## 💻 Tecnologias

- Python 3.13  
- Pandas, NumPy  
- Jupyter Notebook  
- Git para versionamento  

---

## ⚡ Aplicações

- Estudos de **simulação financeira** e análise de produção  
- Validação de séries temporais fictícias para **Machine Learning**  
- Preparação de dados para **Power BI** ou outras ferramentas de visualização  
- Projeto educativo em **ciência de dados aplicada ao setor de petróleo**

---

## 📌 Observações

- Todos os dados são **fictícios**, mas consistentes com padrões reais de produção e finanças  
- Moeda padrão: **BRL**  
- Todas as séries são mensais de **2005-01 até 2025-12**
