import streamlit as st
import pandas as pd
import io

# 1. Configuração da Página e Estilo (Fundo Verdinho)
st.set_page_config(page_title="Conciliador Grupo D", layout="wide")

st.markdown("""
    <style>
    /* Cor de fundo da página toda (Verdinho claro) */
    .stApp {
        background-color: #f0f9f1;
    }
    /* Estilo do botão de download (Verde escuro) */
    .stDownloadButton>button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
    }
    /* Estilo do título */
    h1 {
        color: #1e7e34;
    }
    /* Estilo da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #e8f5e9;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Título e Identificação
st.title("🟢 Robô Conciliador: Grupo D")
st.write("---")

# 3. Painel Lateral com os nomes D1 a D4
with st.sidebar:
    st.header("🛠️ Configurações")
    st.success("Status: Robô Online")
    st.write("**Empresas do Grupo:**")
    st.write("- **Empresa D1**")
    st.write("- **Empresa D2**")
    st.write("- **Empresa D3**")
    st.write("- **Empresa D4**")
    
    st.divider()
    st.markdown("### 📖 Regra Aplicada:")
    st.info("**Para Fornecedor e Adiantamento:**\nCrédito é POSITIVO (+)\nDébito é NEGATIVO (-)")

# 4. Área de Trabalho (Upload)
st.subheader("📥 Suba os Razões (Fornecedores e Adiantamentos)")
st.write("Você pode selecionar vários arquivos de uma vez.")

arquivos_subidos = st.file_uploader(
    "Arraste os arquivos .xlsx do Sistema Domínio aqui", 
    type="xlsx", 
    accept_multiple_files=True
)

if arquivos_subidos:
    lista_fornecedores = []
    lista_adiantamentos = []
    
    for arq in arquivos_subidos:
        # Lendo o Excel
        df = pd.read_excel(arq)
        nome_arquivo = arq.name.lower()
        
        # --- APLICANDO A SUA REGRA DE SINAL ---
        # Crédito (+) e Débito (-)
        if 'Crédito' in df.columns and 'Débito' in df.columns:
            df['Saldo_Ajustado'] = df['Crédito'] - df['Débito']
        
        # Guardando o nome da empresa/arquivo
        df['Origem_Arquivo'] = arq.name
        
        # Separando o que é Adiantamento do que é Fornecedor Normal
        if "adiantamento" in nome_arquivo:
            lista_adiantamentos.append(df)
            st.write(f"✅ **Adiantamento** identificado: {arq.name}")
        else:
            lista_fornecedores.append(df)
            st.write(f"✅ **Fornecedor** identificado: {arq.name}")

    # 5. Criando o Excel final com abas separadas
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        
        # Aba de Fornecedores
        if lista_fornecedores:
            df_forn = pd.concat(lista_fornecedores)
            df_forn.to_excel(writer, index=False, sheet_name='Fornecedores_D')
        
        # Aba de Adiantamentos
        if lista_adiantamentos:
            df_adant = pd.concat(lista_adiantamentos)
            df_adant.to_excel(writer, index=False, sheet_name='Adiantamentos_D')
            
        # Aba Geral (Tudo junto para conferência)
        if lista_fornecedores or lista_adiantamentos:
            df_geral = pd.concat(lista_fornecedores + lista_adiantamentos)
            df_geral.to_excel(writer, index=False, sheet_name='Geral_D1_D4')

    st.write("---")
    st.balloons() # Celebração!
    
    # Botão de Download Verde
    st.download_button(
        label="📥 BAIXAR CONCILIAÇÃO COMPLETA (D1-D4)",
        data=output.getvalue(),
        file_name="Conciliacao_Grupo_D_Final.xlsx",
        mime="application/vnd.ms-excel"
    )

else:
    st.warning("Estou aguardando os arquivos para começar...")

st.divider()
st.caption("🛡️ Projeto Protegido: Nomes reais e dados sensíveis não são salvos no código.")
