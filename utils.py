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


import unicodedata
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import spacy


# Baixar recursos necessários do nltk
# nltk.download('punkt')
# nltk.download('stopwords')

import nltk

# Baixar apenas se não existir
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


def preprocess(text):

    # 1 - minúsculas
    text = text.lower()

    # 2 - remover pontuação simples
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 3 - tokenização NLTK
    tokens = word_tokenize(text)

    # 4 - stemming antes de remover stopwords
    stemmer = RSLPStemmer()
    stems = [stemmer.stem(t) for t in tokens]

    # 5 - remover stopwords *depois* do stemming
    stop = set(stopwords.words("portuguese"))
    stems_clean = [s for s in stems if s not in stop]

    # 6 - manter lista, não set()
    return stems_clean


def preprocess_Exemplo_1(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    stop_words = set(stopwords.words('portuguese'))
    #print(stop_words)
    tokens = [t for t in tokens if t not in stop_words]
    return tokens


# Pré-processamento de texto
def preprocess_Exemplo_2(text):

    # Etapa 1: Normalizacao

    text = text.lower()                                                                                                                     # Converter para minúsculas
    text = unicodedata.normalize('NFD', text)                                                                       # Quebrar caracteres acentuados
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')                                  # Remover acentos
    texto_normalizado = text.translate(str.maketrans('', '', string.punctuation))      # Remover pontuação

    # Etapa 2: Tokenização
    
    tokens = word_tokenize(texto_normalizado)                                                                 # - Separação do texto em palavras (tokens)

    # Etapa 3: Remoção de Stopwords

    stopwords_pt = set(stopwords.words('portuguese'))   
    tokens_sem_stopwords = [t for t in tokens if t not in stopwords_pt]                     # - Palavras comuns que não carregam significado importante (ex: a, de, que, etc.)
    
    # Etapa 4: Stemming
    
    stemmer = RSLPStemmer()
    tokens_stemmed = [stemmer.stem(t) for t in tokens_sem_stopwords]                # - Redução das palavras ao seu radical (ex: ganhado → ganh)

    # Etapa 4: Lemmatizacao 
    # mecanismo mais inteligente de reduzir ao radical ....para o exemplo usaremos steemming

    # nlp = spacy.load("pt_core_news_sm")
    # doc = nlp(' '.join(tokens_sem_stopwords))
    # tokens_lemma = [token.lemma_ for token in doc if token.lemma_ not in stopwords_pt]
    # print("\nTokens após lematização:\n", tokens_lemma)

    # ETAPA 5: Conjunto final de termos representativos
    # - Lista única com os termos úteis para representar o documento
    # termos_representativos_lemma = set(tokens_lemma)
    # termos_representativos_stem = set(tokens_stemmed)


    return tokens_stemmed





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



