import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="DataCo Predictive - Inventory Control", 
    page_icon="📦", 
    layout="wide"
)

# Estilo CSS para métricas e interface
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 35px; color: #1E3A8A; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARREGAMENTO DE DADOS
@st.cache_data
def load_data():
    try:
        # Dados da Operação (Setembro)
        df_ia = pd.read_csv('dados_finais.csv') 
        df_ia['Data'] = pd.to_datetime(df_ia['Data']).dt.date
        
        # Dados do Histórico BI (3 Anos)
        df_bi = pd.read_csv('dados_bi.csv')
        df_bi['Data'] = pd.to_datetime(df_bi['Data']).dt.date
        
        return df_ia, df_bi
    except Exception as e:
        st.error(f"Erro ao carregar ficheiros: {e}")
        return None, None

df_ia, df_bi = load_data()

# TÍTULO DA APLICAÇÃO
st.title("📦 Sistema de Demand Sensing e Gestão Preditiva de Inventário")

if df_ia is not None and df_bi is not None:
    # --- BARRA LATERAL ---
    st.sidebar.header("🕹️ Painel de Controlo")
    
    datas_disponiveis = sorted(df_ia['Data'].unique())
    data_simulada = st.sidebar.select_slider(
        "Data de Hoje:", 
        options=datas_disponiveis, 
        value=datas_disponiveis[0]
    )
    
    margem_seguranca = st.sidebar.slider("Margem de Segurança (%)", 0, 30, 10)
    
    st.sidebar.divider()
    st.sidebar.info(f"**Lead Time:** 6 dias (Fixo)\n\n**Horizonte preditivo:**\n{data_simulada} + 6 dias.")

    # --- LÓGICA DE ATIVAÇÃO DO MODELO (TRANSPARÊNCIA) ---
    data_ativacao = datetime.date(2017, 9, 20)
    
    if data_simulada < data_ativacao:
        st.info(
            "⏳ **Fase de Calibração (Cold Start):** "
            "Até ao dia 19 de Setembro, o algoritmo está a acumular histórico para estabilizar os sinais digitais. "
            "As ordens apresentadas são valores estáticos de segurança (Fallback)."
        )
    else:
        st.success(
            "✅ **Modelo Preditivo Ativo:** "
            "O motor de Machine Learning está a operar em tempo real, reagindo à volatilidade da procura e aos sinais web."
        )

    # --- SEPARADORES ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Histórico (BI)", 
        "🚨 Alertas Diários", 
        "🎯 Análise Produto", 
        "📈 Impacto (ROI)", 
        "🧠 Motor Preditivo"
    ])

    # --- TAB 1: DIAGNÓSTICO BI ---
    with tab1:
        st.header("Diagnóstico de Operações (Histórico Mensal)")
        st.write("Análise da performance antes da implementação do modelo preditivo.")
        
        c1, c2 = st.columns(2)
        c1.metric("Volume Histórico Processado", "180.519 transações")
        c2.metric("Taxa Global de Atraso", "54.8%", delta="Crítico", delta_color="inverse")
        
        st.divider()
        df_bi_plot = df_bi.copy()
        df_bi_plot['Data'] = pd.to_datetime(df_bi_plot['Data'])
        df_bi_mensal = df_bi_plot.groupby(df_bi_plot['Data'].dt.to_period('M')).agg({
            'Vendas Totais': 'sum',
            'Falhas Totais': 'sum'
        }).reset_index()
        df_bi_mensal['Data'] = df_bi_mensal['Data'].astype(str)
        
        col_v, col_f = st.columns(2)
        with col_v:
            st.subheader("📊 Vendas Mensais (Unidades)")
            fig_v = px.bar(df_bi_mensal, x='Data', y='Vendas Totais', color_discrete_sequence=['#3b82f6'])
            fig_v.update_layout(xaxis_title=None, yaxis_title=None, height=350)
            st.plotly_chart(fig_v, use_container_width=True)
            
        with col_f:
            st.subheader("⚠️ Falhas Mensais (Ruturas)")
            fig_f = px.bar(df_bi_mensal, x='Data', y='Falhas Totais', color_discrete_sequence=['#ef4444'])
            fig_f.update_layout(xaxis_title=None, yaxis_title=None, height=350)
            st.plotly_chart(fig_f, use_container_width=True)

    # --- TAB 2: ALERTAS DIÁRIOS ---
    with tab2:
        st.header("Alertas de Stock - Resumo Diário")
        df_hoje = df_ia[df_ia['Data'] == data_simulada].copy()
        
        # Cálculo das sugestões dinâmicas
        df_hoje['Sugerido'] = (df_hoje['Ordem_Emitida_IA'] / 1.1) * (1 + (margem_seguranca/100))
        df_hoje['Sugerido'] = df_hoje['Sugerido'].round().astype(int)
        
        resumo = df_hoje[['Produto', 'Disp_IA', 'Sugerido']].copy()
        resumo.columns = ['Produto', 'Stock Disponível (Manhã)', 'Encomenda Sugerida (Modelo)']
        
        st.dataframe(resumo, use_container_width=True, hide_index=True)
        st.info("💡 As encomendas sugeridas visam garantir a disponibilidade para o horizonte de 6 dias (Lead Time).")

    # --- TAB 3: ANÁLISE PRODUTO ---
    with tab3:
        produto_selecionado = st.selectbox("Selecione o Produto:", sorted(df_ia['Produto'].unique()))
        df_f = df_ia[(df_ia['Data'] == data_simulada) & (df_ia['Produto'] == produto_selecionado)]
        
        if not df_f.empty:
            dados = df_f.iloc[0]
            previsao_base = dados['Ordem_Emitida_IA'] / 1.1
            nova_ordem = round(previsao_base * (1 + (margem_seguranca / 100)))
            
            c_p1, c_p2, c_p3 = st.columns(3)
            c_p1.metric("📦 Stock em Armazém", f"{int(dados['Disp_IA'])} un.")
            c_p2.metric("📈 Procura Prevista (T+6)", f"{round(previsao_base)} un.")
            c_p3.metric("🛒 Ordem Sugerida", f"{nova_ordem} un.", delta=f"+{margem_seguranca}% Seg.")
            
            st.divider()
            st.write(f"#### Comportamento de Inventário: {produto_selecionado}")
            df_hist = df_ia[(df_ia['Produto'] == produto_selecionado) & (df_ia['Data'] <= data_simulada)]
            
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Scatter(x=df_hist['Data'], y=df_hist['Disp_IA'], name='Nível de Stock', line=dict(color='#2ecc71', width=3)))
            fig_hist.add_trace(go.Scatter(x=df_hist['Data'], y=df_hist['Vendas'], name='Vendas Reais', line=dict(color='#e74c3c', width=3, dash='dot')))
            fig_hist.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0), legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig_hist, use_container_width=True)

    # --- TAB 4: IMPACTO (ROI) ---
    with tab4:
        st.header("Eficiência Financeira e Redução de Ruturas")
        st.subheader("Receita Protegida (Semana de Teste): $18,128.69")
        
        col_r1, col_r2 = st.columns(2)
        col_r1.metric("❌ Ruturas (Gestão por Inércia)", "161", delta="Sistema Reativo", delta_color="inverse")
        col_r2.metric("✅ Ruturas (Modelo Preditivo)", "41", delta="-74.5% de Atrasos")
        
        st.divider()
        st.markdown("""
        **Análise de Impacto:**
        * O modelo preditivo permitiu detetar antecipadamente os picos de procura através dos sinais digitais.
        * A redução de 74.5% nas ruturas traduz-se em maior fidelização e poupança em envios de emergência.
        """)

    # --- TAB 5: MOTOR PREDITIVO ---
    with tab5:
        st.header("Métricas do Modelo de Machine Learning")
        st.write("Explicabilidade e performance do algoritmo Random Forest:")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.success("**Importância das Variáveis:**")
            st.write("1. **Média Móvel (3 dias):** Estabilidade da procura.")
            st.write("2. **Lags de Cliques (t-1 a t-3):** Antecipação de picos.")

        
        with col_m2:
            st.info("**Performance Técnica:**")
            st.write("- **Algoritmo:** Random Forest Regressor")
            st.write("- **Precisão (R²):** 0.72")


else:
    st.error("Erro: Certifica-te de que os ficheiros CSV estão na mesma pasta do script.")