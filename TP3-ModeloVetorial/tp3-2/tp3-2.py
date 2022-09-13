import os
from unicodedata import normalize
import numpy as np
import nltk

diretorio = 'C:/Users/andre/OneDrive/Área de Trabalho/ORI/TP3-ModeloVetorial/tp3-2/'
punct = [',','.','!',';','?','(',')','[',']','{','}']
stop = nltk.corpus.stopwords.words('portuguese')
stopwords = []
for i in stop:
    stopwords.append(normalize("NFKD",i).encode('ASCII','ignore').decode("ASCII"))
stopwords[:] = np.unique(stopwords)
    
def abrirArquivo(arquivo):
    a = open(arquivo,'r',encoding="utf8")
    c = a.read()
    return c

def listaDocumentos(diretorio):
    documentos = []
    for arquivo in os.listdir(diretorio):
      if arquivo != 'vocabulario.txt' and arquivo.endswith(".txt") :
          documentos.append(arquivo)
    return documentos

def listaDocumento(doc):
    c = abrirArquivo(doc)
    c = normalize("NFKD",c).encode('ASCII','ignore').decode("ASCII")
    for i in punct:
        c = c.replace(i, "")
    splitedDoc = c.lower().split()
    splitedDoc.sort()
    for t in splitedDoc:
        if t in stopwords:
            splitedDoc.remove(t)
    return splitedDoc
    
def separarDocumento(doc):
    c = abrirArquivo(doc)
    c =  normalize("NFKD",c).encode('ASCII','ignore').decode("ASCII")
    for i in punct:
        c = c.replace(i, "")
    splitedDoc = c.lower().split()
    splitedDoc[:] = np.unique(splitedDoc)
    return splitedDoc

def criaVocabulario(docs):
    vocabulario = []
    for d in docs:
        doc = separarDocumento(d)
        vocabulario = vocabulario + doc
    vocabulario[:] = np.unique(vocabulario)
    return vocabulario

def calculaFrequencias(vocabulario,doc):
    bagOfWords = []
    for t in vocabulario:
        for p in doc:
            if p in vocabulario:
                aux = doc.count(t)
                bagOfWords.append(aux)
                break
            else:
                bagOfWords.append(0)
                break
    return bagOfWords

def calculaTF(bagOfWords):
    tf = []
    for i in bagOfWords:
        if i == 0:
            tf.append(0)
        else:
            tf.append(round(1 + np.log2(i),2))
    return tf

def bagOfWords_TF(vocabulario,docs):
    for d in docs:
        bagOfWords = []
        doc = listaDocumento(d)
        bagOfWords = calculaFrequencias(vocabulario,doc)
        tf = calculaTF(bagOfWords)
        return tf

def calculaIDF(vocabulario, docs):
    idf = []
    for t in vocabulario:
        aux = 0
        for p in docs:
            doc = separarDocumento(p)
            if t in doc:
                aux += 1
        idf.append(aux)
    for i in range(len(idf)):
       idf[i] = round(np.log2(len(docs)/idf[i]),2)
    return idf

def calculaTF_IDF(vocabulario, docs):
    tf_idf = []
    for d in docs:
        tfidf = []
        doc = listaDocumento(d)
        bagOfWords = calculaFrequencias(vocabulario, doc)
        tf = calculaTF(bagOfWords)
        for i in range(len(tf)):
            tfidf.append(round(tf[i]*idf[i],2))
        tf_idf.append(tfidf)
    return tf_idf

def calculaTF_IDF_Consulta(vocabulario, docs, consulta):
    tf_idf_consulta = []
    termos = normalize("NFKD",consulta).encode('ASCII','ignore').decode("ASCII")
    for i in punct:
        termos = termos.replace(i,'')
    termos = termos.lower().split()
    for t in termos:
        if t in stopwords:
            termos.remove(t)
    bag_consulta = calculaFrequencias(vocabulario, termos)
    tf_consulta = calculaTF(bag_consulta)
    for i in range(len(tf_consulta)):
        tf_idf_consulta.append(round(tf_consulta[i]*idf[i],2))
    return tf_idf_consulta

def similaridade_calc(tf_idf_docs, tf_idf_consulta):
    pi = 0
    for i in range (len(tf_idf_docs)):
        aux = tf_idf_docs[i]*tf_idf_consulta[i]
        pi += aux

    norm_tf_idf = np.linalg.norm(tf_idf_docs)
    norm_tf_idf_consulta = np.linalg.norm(tf_idf_consulta)
    norm = norm_tf_idf*norm_tf_idf_consulta
    if norm!=0:
        similaridade = round(pi/norm,2)
    else:
        similaridade = 0
    
    return similaridade
            
def calculaSimilaridade(tf_idf_consulta):
    vetor_similaridade=[]
    for i in range(len(tf_idf)):
        vetor_similaridade.append(similaridade_calc(tf_idf[i],tf_idf_consulta))
    
    return vetor_similaridade
        
def processaConsulta(vocabulario,docs,consulta):
    tf_idf_consulta = calculaTF_IDF_Consulta(vocabulario, docs, consulta)
    similaridade = calculaSimilaridade(tf_idf_consulta)
    return similaridade

docs = listaDocumentos(diretorio)
vocabulario = criaVocabulario(docs)
idf = calculaIDF(vocabulario, docs)
tf_idf = calculaTF_IDF(vocabulario,docs)
consulta = input("Digite a consulta:")
similaridade = processaConsulta(vocabulario,docs,consulta)

for i in range(len(similaridade)):
    print(f'Documento:{docs[i]} : {similaridade[i]}')

maisSimilar = max(similaridade)
posi = similaridade.index(maisSimilar)
print(f'\nDocumento mais similar: {docs[posi]}')