import streamlit as st

def main():
    
    st.sidebar.header("Classificação Mercadológica")
    st.sidebar.markdown('Desenvolvido por: **Tiago Dias**')
    st.sidebar.markdown('Email para contato:')
    st.sidebar.markdown('diasctiago@gmail.com')
    st.sidebar.markdown('LinkedIn:')
    st.sidebar.markdown('https://www.linkedin.com/in/diasctiago')
    st.sidebar.markdown('GitHub:')
    st.sidebar.markdown('https://github.com/diasctiago')
    st.sidebar.markdown('D3:')
    st.sidebar.markdown('https://www.dadosaocubo.com')
    
    st.image('LogoD3.png',format='PNG')
    st.title('Classificação Mercadológica')
    st.subheader('**Classificação com NLP**')
    st.markdown('Descrever o que o app faz!')
    download = st.checkbox('Download Exemplo')

    st.subheader('**Selecione uma da Opções**')
    options = st.radio('O que deseja fazer?',('Carregar Arquivo', 'Digitar Itens'))

    st.subheader('**Dados Classificados**')
    st.markdown('Carregar DataFrame!')

    st.subheader('**Visualização dos Dados**')
    st.markdown('Carregar Gráficos!')

if __name__ == '__main__':
    main()
