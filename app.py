import streamlit as st
import pandas as pd
from joblib import load
import matplotlib.pyplot as plt
#from wordcloud import WordCloud
import base64

def clean (df):
    df['nova_descricao'] = df['descricao'].copy()
    df['nova_descricao'] = df['nova_descricao'].str.replace('[,.:;!?]+', ' ', regex=True).copy()
    df['nova_descricao'] = df['nova_descricao'].str.replace('[/<>()|\+\-\$%&#@\'\"]+', ' ', regex=True).copy()
    df['nova_descricao'] = df['nova_descricao'].str.replace('[0-9]+', '', regex=True)
    return df.nova_descricao

def model(df):
    cvt = load('models/cvt.joblib') 
    tfi = load('models/tfi.joblib') 
    clf = load('models/clf.joblib') 
    new_cvt = cvt.transform(df)
    new_tfi = tfi.transform(new_cvt)
    result = clf.predict(new_tfi)
    return result

def get_download(df, arq):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() 
    href = f'<a href="data:file/csv;base64,{b64}" download="'+arq+'.csv">Download</a>'
    return href
    
def main():
    
    st.sidebar.header('Tiago Dias')
    st.sidebar.markdown('Email para contato:')
    st.sidebar.markdown('diasctiago@gmail.com')
    st.sidebar.markdown('LinkedIn:')
    st.sidebar.markdown('https://www.linkedin.com/in/diasctiago')
    st.sidebar.markdown('GitHub:')
    st.sidebar.markdown('https://github.com/diasctiago')
    st.sidebar.markdown('D3:')
    st.sidebar.markdown('https://www.dadosaocubo.com')
    
    st.image('LogoD3.png', format='PNG')
    st.title('Classificação Mercadológica')
    st.subheader('**Classificação com NLP**')
    st.markdown('Este app faz a classificação mercadológica, a partir da descrição dos itens é feita a classificação por departamento. Com técnicas de **NLP e aprendizagem de máquina**, foi treinado um modelo capaz de categorizar itens em **53 departamentos**. Você pode testar a aplicação fazendo o download de uma relação de itens exemplos no botão (**Link Exemplo**), com o seu próprio arquivo csv (apenas uma coluna com a descrição dos itens), ou escolhendo a opção (**Digitar Itens**) e inserir manualmente os itens separados apenas por vírgula. Você vai poder visualizar exemplos dos dados gerados, alguns gráficos e ao final é possível fazer o download do arquivo classificado. A precisão deste classificador é de **95%**')
    if st.button('Link Exemplo'):
        exemplo = pd.read_csv('https://raw.githubusercontent.com/dadosaocubo/streamlit/master/itens.csv')
        st.markdown(get_download(exemplo, 'itens'), unsafe_allow_html=True)
            
    dados = ''
    stop_words = ['em','sao','ao','de','da','do','para','c','kg','un','ml',
                  'pct','und','das','no','ou','pc','gr','pt','cm','vd','com',
                  'sem','gfa','jg','la','1','2','3','4','5','6','7','8','9',
                  '0','a','b','c','d','e','lt','f','g','h','i','j','k','l',
                  'm','n','o','p','q','r','s','t','u','v','x','w','y','z']
    
    st.subheader('**Selecione uma das Opções**')
    options = st.radio('O que deseja fazer?',('Carregar Arquivo', 'Digitar Itens'))
    if options == 'Carregar Arquivo':
        data = st.file_uploader('Escolha o dataset (.csv)', type = 'csv')
        if data is not None:
            df = pd.read_csv(data)
            df['nova_descricao'] = clean(df)
            result = model(df['nova_descricao'])
            df['departamento'] = result
            st.subheader('**Dados Classificados**')
            qtd = st.slider('Quantos itens?', 0, 50, 5)
            st.dataframe(df[['descricao','departamento']].head(qtd))
            dados = 'ok'
            
    if options == 'Digitar Itens':
        text = st.text_input('Digite os itens separados por vírgulas (Ex: Arroz, Feijão, Açúcar) :')
        if text is not '':
            itens = {'descricao': text.split(',')}
            df = pd.DataFrame(itens)
            df['nova_descricao'] = clean(df)
            result = model(df['nova_descricao'])
            df['departamento'] = result
            st.subheader('**Dados Classificados**')
            st.dataframe(df[['descricao','departamento']].head())
            dados = 'ok'

    st.subheader('**Visualização dos Dados**')
    if dados is not '':
        if st.checkbox('WordCloud'):
            all_words = ' '.join(s for s in df['nova_descricao'].values)
            # criar uma wordcloud
            #wc = WordCloud(stopwords=stop_words, background_color="black", width=1600, height=800)
            #wordcloud = wc.generate(all_words)
            # plotar wordcloud
            #fig, ax = plt.subplots(figsize=(10,6))
            #ax.imshow(wordcloud, interpolation='bilinear')
            #ax.set_axis_off()
            #st.pyplot()
        if st.checkbox('Top10 Departamentos'):
            chart_data = df['departamento'].value_counts().head(10)
            st.bar_chart(chart_data)
        if st.checkbox('Bottom10 Departamentos'):
            chart_data = df['departamento'].value_counts().tail(10)
            st.bar_chart(chart_data)

    if dados is not '':
        st.subheader('**Download dos Dados**')
        st.markdown(get_download(df[['descricao','departamento']], 'Result'), unsafe_allow_html=True)

            
if __name__ == '__main__':
    main()
