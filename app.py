import streamlit as st
import pandas as pd
import io

# 1. Configuração da Página e Estilo (Verde Escuro com Borda no Topo)
st.set_page_config(page_title="Conciliador Grupo D", layout="wide")

st.markdown("""
    <style>
    /* Cor de fundo da página (Verde Floresta Suave) */
    .stApp {
        background-color: #e1ede2;
        /* BORDA DE CIMA PINTADA: Verde bem escuro e grossinha */
        border-top: 15px solid #1b5e20;
    }
    
    /* Botão de Download (Verde Bem Escuro) */
    .stDownloadButton>button {
        background-color: #1b5e20 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 2px solid #003300 !important;
        padding: 0.7rem 2.5rem !important;
    }
    
    /* Títulos em Verde Musgo */
    h1, h2, h3 {
        color: #1b5e20;
    }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #c8e6c9;
        border-top: 15px solid #1b5e20; /* Borda também na lateral para alinhar */
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Título
st.title("Grupo D")
st.write("---")

# 3. Painel Lateral com nomes D1 a D4
with st.sidebar:
    st.header("🛠️ Painel de Controlo")
    st.success("Robô Ativo e Seguro")
    st.write("**Empresas Registadas:**")
    st.write("- Empresa **D1**")
    st.write("- Empresa **D2**")
    st.write("- Empresa **D3**")
    st.write("- Empresa **D4**")
    
    st.divider()
    st.markdown("### 📖 Regras de Cálculo:")
    st.info("Sinal para Fornecedores:\n**Crédito (+)**\n**Débito (-)**")

# 4. Área de Trabalho (Upload)
st.subheader("📥 Área de Anexos .xlsx")
arquivos_subidos = st.file_uploader(
    "Carregar planilhas do Sistema Domínio", 
    type="xlsx", 
    accept_multiple_files=True
)

if arquivos_subidos:
    forn_list = []
    adiant_list = []
    
    for arq in arquivos_subidos:
        df = pd.read_excel(arq)
        nome_bq = arq.name.lower()
        
        # Regra de Ouro do Daniel (C+ / D-)
        if 'Crédito' in df.columns and 'Débito' in df.columns:
            df['Saldo_Ajustado'] = df['Crédito'] - df['Débito']
        
        df['Identificador'] = arq.name
        
        if "adiantamento" in nome_bq:
            adiant_list.append(df)
            st.write(f"✔️ **Adiantamento lido:** {arq.name}")
        else:
            forn_list.append(df)
            st.write(f"✔️ **Fornecedor lido:** {arq.name}")

    # 5. Processamento para Download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if forn_list:
            pd.concat(forn_list).to_excel(writer, index=False, sheet_name='Fornecedores_D')
        if adiant_list:
            pd.concat(adiant_list).to_excel(writer, index=False, sheet_name='Adiantamentos_D')
        if forn_list or adiant_list:
            pd.concat(forn_list + adiant_list).to_excel(writer, index=False, sheet_name='Geral_D1_D4')

    st.write("---")
    st.(✅)
    
    st.download_button(
        label="📥 DESCARREGAR RELATÓRIO FINAL (D1-D4)",
        data=output.getvalue(),
        file_name="Relatorio_Conciliacao_GrupoD.xlsx",
        mime="application/vnd.ms-excel"
    )

else:
    st.warning("A aguardar os ficheiros...")

st.divider()
st.caption("🔒 Segurança Máxima: Este robô utiliza apenas memória temporária.")
