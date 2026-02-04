import streamlit as st
import pandas as pd
import io

# 1. Configuração da Página e Cores (Visual Verdinho)
st.set_page_config(page_title="Conciliador Grupo Daniel", layout="wide")

st.markdown("""
    <style>
    /* Deixa o botão de baixar bem verdinho e destacado */
    .stDownloadButton>button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
    }
    /* Estilo para títulos */
    h1 {
        color: #1e7e34;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Título Principal
st.title("🟢 Robô Conciliador: Grupo Daniel")
st.write("---")

# 3. Regras de Negócio (Explicação simples)
with st.sidebar:
    st.header("🛠️ Configurações")
    st.success("Status: Robô Online")
    st.write("**Empresas do Grupo:**")
    st.write("1. Tarantelli")
    st.write("2. Extrema")
    st.write("3. Acessórios")
    st.write("4. Michelin")
    
    st.divider()
    st.markdown("### 📖 Regras Aplicadas:")
    st.info("**Fornecedor/Adiantamento:**\nCrédito é (+) e Débito é (-)")

# 4. Área de Upload
st.subheader("📥 Suba os Razões das Empresas")
st.write("Pode arrastar todos os arquivos de Fornecedores e Adiantamentos de uma vez!")

arquivos_subidos = st.file_uploader(
    "Selecione os arquivos .xlsx", 
    type="xlsx", 
    accept_multiple_files=True
)

if arquivos_subidos:
    # Listas para organizar as abas
    lista_fornecedores = []
    lista_adiantamentos = []
    
    for arq in arquivos_subidos:
        # Lê o Excel
        df = pd.read_excel(arq)
        
        # Nome do arquivo em minúsculo para facilitar a busca
        nome_arquivo = arq.name.lower()
        
        # --- APLICA A SUA REGRA (Crédito (+) e Débito (-)) ---
        # OBS: O código assume que as colunas se chamam 'Crédito' e 'Débito'
        # Se no seu Excel estiver 'Vl. Crédito', troque os nomes abaixo:
        if 'Crédito' in df.columns and 'Débito' in df.columns:
            df['Saldo_Ajustado'] = df['Crédito'] - df['Débito']
        
        df['Arquivo_Origem'] = arq.name
        
        # Separa o que é Adiantamento do que é Fornecedor Normal
        if "adiantamento" in nome_arquivo:
            lista_adiantamentos.append(df)
            st.write(f"✅ Lido: {arq.name} (Adiantamento)")
        else:
            lista_fornecedores.append(df)
            st.write(f"✅ Lido: {arq.name} (Fornecedor)")

    st.write("---")
    
    # 5. Criação do arquivo final com ABAS SEPARADAS
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        
        if lista_fornecedores:
            df_forn = pd.concat(lista_fornecedores)
            df_forn.to_excel(writer, index=False, sheet_name='Fornecedores_Normal')
        
        if lista_adiantamentos:
            df_adant = pd.concat(lista_adiantamentos)
            df_adant.to_excel(writer, index=False, sheet_name='Adiantamentos')
            
        # Aba Geral (Cruzamento)
        if lista_fornecedores or lista_adiantamentos:
            df_geral = pd.concat(lista_fornecedores + lista_adiantamentos)
            df_geral.to_excel(writer, index=False, sheet_name='Geral_Conciliado')

    # Mostra balões quando termina
    st.balloons()
    
    # Botão de Download
    st.download_button(
        label="📥 BAIXAR CONCILIAÇÃO COMPLETA (VERDE)",
        data=output.getvalue(),
        file_name="Conciliacao_Grupo_Daniel_Final.xlsx",
        mime="application/vnd.ms-excel"
    )

else:
    st.warning("Aguardando o envio dos arquivos para começar...")

# Rodapé de segurança
st.divider()
st.caption("🔒 Ambiente Seguro: O processamento é feito em memória e não salva arquivos no servidor.")
