import streamlit as st


def uploader():
    st.markdown("""
    <style>
    div[data-testid="stFileUploader"] {
        position: relative;
        border: 2px dashed #C0C0C0;
        border-radius: 20px;
        background-color: #F8F9FA;
        padding: 1rem 2rem;
        text-align: center;
        transition: all 0.25s ease;
        overflow: hidden;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #1E88E5;
        background-color: #F1F6FB;
    }
    section[data-testid="stFileUploaderDropzone"] {
        opacity: 0 !important;
        position: absolute !important;
        inset: 0 !important;
        z-index: 10 !important;
        cursor: pointer !important;
    }
    div[data-testid="stFileUploader"]::before {
        content: "Arraste seu arquivo aqui ou";
        color: #1E88E5;
        font-weight: 600;
        font-size: 1rem;
        display: block;
        margin-bottom: -1rem;
        z-index: 1;
        position: relative;
    }
    div[data-testid="stFileUploader"]::after {
        content: "Selecionar arquivo";
        display: inline-block;
        background-color: #1E88E5;
        color: #FFFFFF;
        padding: 0.6rem 1.5rem;
        border-radius: 6px;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        z-index: 1;
        position: relative;
    }
    div[data-testid="stFileUploader"]:hover::after {
        background-color: #1565C0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    div[data-testid="stFileUploader"] div[role="listitem"] {
        display: none !important;
    }
    div[data-testid="stFileUploader"] *:not([role="listitem"]) {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
def uploader_depois(filename):
    return f"""
    <style>
    @keyframes fadeZoom {{
        0% {{ opacity: 0; transform: scale(0.95); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}
    div[data-testid="stFileUploader"] {{
        position: relative;
        border: 2px dashed #43A047;
        border-radius: 20px;
        background-color: #E8F5E9;
        padding: 1rem 1rem;
        text-align: center;
        overflow: hidden;
        animation: fadeZoom 0.5s ease-in-out;
    }}
    section[data-testid="stFileUploaderDropzone"] {{
        opacity: 0 !important;
        position: absolute !important;
        inset: 0 !important;
        z-index: 10 !important;
        cursor: pointer !important;
    }}
    div[data-testid="stFileUploader"]::before {{
        content: "✅ Arquivo carregado";
        color: #388E3C;
        font-weight: 600;
        font-size: 1rem;
        display: block;
        margin-bottom: -4rem;
        z-index: 1;
        position: relative;
        animation: fadeZoom 0.6s ease-in-out;
    }}
    div[data-testid="stFileUploader"]::after {{
        content: "{filename}";
        display: inline-block;
        background-color: #43A047;
        color: #FFFFFF;
        padding: 0.6rem 1.5rem;
        border-radius: 6px;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
        z-index: 1;
        position: relative;
        animation: fadeZoom 0.8s ease-in-out;
    }}
    div[data-testid="stFileUploader"]:hover::after {{
        background-color: #2E7D32;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }}
    div[data-testid="stFileUploader"] div[role="listitem"] {{
        display: none !important;
    }}
    div[data-testid="stFileUploader"] *:not([role="listitem"]) {{
        background: transparent !important;
        border: none !important;
        color: transparent !important;
    }}
    </style>
    """