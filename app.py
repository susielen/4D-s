import streamlit as st
import pandas as pd
import io

# 1. Configuração da Página
st.set_page_config(
    page_title="Grupo 4D's",
    page_icon="🚗🧑🏼‍🔧",
    layout="wide"
)

# 2. O ESTILO (Cores Suaves, Letra Moderna e Fundo Profissional)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800&display=swap');

    /* FUNDO LILÁS LAVANDA (Suave para os olhos) */
    .stApp {
        background-color: #20B2AA; 
        background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
        background-attachment: fixed;
    }

    /* BARRA LATERAL E TOPO (Roxo Pastel) */
    header[data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #008080 !important;
    }

    /* ESCONDER A COROA E ÍCONES DO TOPO */
    button[kind="headerNoPadding"], .stApp header svg {
        display: none !important;
    }

    /* TÍTULO FINO E ELEGANTE */
    .titulo {
        font-family: 'Montserrat', sans-serif;
        color: #3CB371; /* Roxo escuro para contraste */
        font-size: 28px; 
        font-weight: 800; 
        text-align: center; 
        padding: 8px; 
        background-color: rgba(230, 224, 255, 0.9);
        border-radius: 10px;
        border: 1px solid #9B8ADE;
        margin-top: -35px;
        margin-bottom: 25px;
    }

    /* TEXTOS DA BARRA LATERAL EM NEGRITO */
    [data-testid="stSidebar"] * {
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* CAIXA DE UPLOAD LILÁS CLARO */
    [data-testid="stFileUploaderDropzone"] {
        background-color: rgba(255, 255, 255, 0.4) !important; 
        border: 2px dashed #9B8ADE !important;
        border-radius: 12px !important;
    }

    /* --- ESTA É A PARTE QUE MUDA A COR DO BROWSE FILES --- */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #E6E0FF !important; /* Cor igual a caixinha */
        color: #3CB371 !important; /* Letra roxa */
        border: 1px solid #9B8ADE !important;
        border-radius: 8px !important;
        transition: 0.3s; /* Deixa o efeito suave */
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #9B8ADE !important; /* Cor igual ao corredor (lilás mais forte) */
        color: white !important; /* Letra fica branca */
    }
    
    /* BOTÃO DE DOWNLOAD PERSONALIZADO */
    .stDownloadButton button {
        background-color: #9B8ADE !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    </style>
    
    <p class="titulo"> Grupo 4D's 🚗</p>
    """, unsafe_allow_html=True)


# 3. Painel Lateral com nomes D1 a D4
with st.sidebar:
    st.header("🛠️ Painel de Controlo")
    st.success("Robô Ativo e Seguro")
    st.write("**Empresas Registadas:**")
    st.write("- Empresa **D1**")
    st.write("- Empresa **D2**")
    st.write("- Empresa **D3**")
    st.write("- Empresa **D4**")
    
   
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
