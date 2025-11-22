# biblioteas necessarias
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import string

# Baixar recursos necessários do nltk
nltk.download('punkt')
nltk.download('stopwords')
# Pré-processamento de texto
def preprocess(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    stop_words = set(stopwords.words('portuguese'))
    #print(stop_words)
    tokens = [t for t in tokens if t not in stop_words]
    return tokens




if __name__=='__main__':
    # Documentos do exemplo dos slides (simplificados para português)
    docs = [
        "notícias sobre vestibular unicamp",
        "notícias sobre comida orgânica na unicamp",
        "notícias do vestibular Unicamp",
        "notícias do vestibular Unicamp vestibular 2020",
        "notícias de moradia Unicamp Unicamp Unicamp"
    ]

    query = "Unicamp vestibular 2020"
    
    docs_tokens = [preprocess(doc) for doc in docs]
    
    query_tokens = preprocess(query)

    # Matriz termo-documento binária
    count_vect = CountVectorizer(binary=True)
    X_bin = count_vect.fit_transform(docs)
    query_vec_bin = count_vect.transform([query])
    query_vec_bin

    # 2. Matriz termo-documento com frequência
    count_vect_freq = CountVectorizer(binary=False)
    X_freq = count_vect_freq.fit_transform(docs)
    #query = "notícias sobre vestibular unicamp"
    print(query)
    query_vec_freq = count_vect_freq.transform([query])

    # Similaridade cosseno com frequência
    cosine_sim = cosine_similarity(query_vec_freq, X_freq)
    # No. de elementos em cosine_sim representa no. de documentos
    # print(docs)
    # TF-IDF
    tfidf_vect = TfidfVectorizer()
    X_tfidf = tfidf_vect.fit_transform(docs)
    query_vec_tfidf = tfidf_vect.transform([query])
    cosine_sim_tfidf = cosine_similarity(query_vec_tfidf, X_tfidf)
    # BM25
    bm25 = BM25Okapi(docs_tokens)
    bm25_scores = bm25.get_scores(query_tokens)

    print('bm25_scores>>>>',bm25_scores)
    # Organização dos resultados em DataFrame
    df_resultado = pd.DataFrame({
        "Documento"                     : docs,
        "Produto Escalar (Binário)"     : (query_vec_bin @ X_bin.T).toarray()[0],
        "Produto Escalar (Frequência)"  : (query_vec_freq @ X_freq.T).toarray()[0],
        "Similaridade Cosseno (Freq)"   : cosine_sim.flatten(),
        "Similaridade Cosseno (TF-IDF)" : cosine_sim_tfidf.flatten(),
        "BM25"                          : bm25_scores
    })
    # Ordenar pelo melhor score (BM25)
    df_resultado = df_resultado.sort_values("BM25", ascending=False)

    print(df_resultado.head)



