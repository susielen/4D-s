import streamlit as st
import pandas as pd
import io

# 1. Configuração da Página e Estilo (Verde mais Escuro)
st.set_page_config(page_title="Grupo 4D's", layout="wide")

st.markdown("""
    <style>
    /* Cor de fundo da página (Verde Floresta Suave) */
    .stApp {
        background-color: #e1ede2;
    }
    /* Botão de Download (Verde Bem Escuro e Forte) */
    .stDownloadButton>button {
        background-color: #1b5e20 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 2px solid #003300 !important;
        padding: 0.7rem 2.5rem !important;
    }
    /* Hover do botão (mudar cor ao passar o rato) */
    .stDownloadButton>button:hover {
        background-color: #0d3c11 !important;
        color: #ffffff !important;
    }
    /* Títulos em Verde Musgo */
    h1, h2, h3 {
        color: #1b5e20;
    }
    /* Barra lateral em tom de verde fechado */
    [data-testid="stSidebar"] {
        background-color: #c8e6c9;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Título
st.title("Grupo D")
st.write("---")

# 3. Painel Lateral
with st.sidebar:
    st.header("🛠️ Painel de Controle")
    st.success("Conciliação Ativa e Segura")
    st.write("**Empresas Registadas:**")
    st.write("- Empresa **D1**")
    st.write("- Empresa **D2**")
    st.write("- Empresa **D3**")
    st.write("- Empresa **D4**")


# 4. Área de Upload
st.subheader("📥 Central de Arquivos .xlsx")
st.write("Selecione os Razões de Fornecedores e Adiantamentos:")

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
        
        # Aplicação da Regra de Ouro (C+ / D-)
        if 'Crédito' in df.columns and 'Débito' in df.columns:
            df['Saldo_Ajustado'] = df['Crédito'] - df['Débito']
        
        df['Identificador'] = arq.name
        
        if "adiantamento" in nome_bq:
            adiant_list.append(df)
            st.write(f"✔️ **Adiantamento:** {arq.name}")
        else:
            forn_list.append(df)
            st.write(f"✔️ **Fornecedor:** {arq.name}")

    # 5. Processamento do Excel Final
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if forn_list:
            pd.concat(forn_list).to_excel(writer, index=False, sheet_name='Fornecedores_D')
        if adiant_list:
            pd.concat(adiant_list).to_excel(writer, index=False, sheet_name='Adiantamentos_D')
        if forn_list or adiant_list:
            pd.concat(forn_list + adiant_list).to_excel(writer, index=False, sheet_name='Geral_D1_D4')

    st.write("---")
    st.balloons()
    
    # Botão de Download Verde Escuro
    st.download_button(
        label="📥 DESCARREGAR RELATÓRIO FINAL (D1-D4)",
        data=output.getvalue(),
        file_name="Relatorio_Conciliacao_GrupoD.xlsx",
        mime="application/vnd.ms-excel"
    )

else:
    st.warning("A aguardar os ficheiros para processamento...")

st.divider()
st.caption("🔒 Segurança Máxima: Este robô utiliza apenas memória temporária para os cálculos.")
