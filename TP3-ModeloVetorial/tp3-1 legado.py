import numpy as np
import nltk
import os
from unicodedata import normalize

diretorio = 'C:/Users/andre/OneDrive/Área de Trabalho/ORI/TP3-ModeloVetorial/'
vocabulario = 'C:/Users/andre/OneDrive/Área de Trabalho/ORI/TP3-ModeloVetorial/vocabulario.txt'

#CASO DE TESTE
d1 = 'to do is to be to be is to do'
d2 = 'to be or not to be i am what i am'
d3 = 'i think therefore i am do be do be do'
d4 = 'do do do da da da let it be let it be'

documentos = [d1,d2,d3,d4]

splited_doc = [d1.split(),d2.split(),d3.split(),d4.split()]
#FIM CASO DE TESTE
'''
def lista_documentos(diretorio):
    documentos = list()
    punct = [',','.','!',';','?','(',')','[',']','{','}']
    for arquivo in os.listdir(diretorio):
      if arquivo != 'vocabulario.txt':
        if arquivo.endswith(".txt"):
          dr = open(arquivo,"r")
          d = dr.read()
          d = d.lower().replace('\n',' ')
          d = normalize("NFKD",d).encode('ASCII','ignore').decode("ASCII")
          for c in punct:
            d = d.replace(c,"")
          documentos.append(d)
    return documentos

documentos = lista_documentos(diretorio)
splited_doc = []
for d in documentos:
  splited_doc.append(d.split())
'''

vocabulario = open(vocabulario,'r')
vocabulario = vocabulario.read()
vocabulario = vocabulario.split()

contagem = {}
for d in splited_doc:
    for t in vocabulario:
      for p in d:
        if t == p:
          if t not in contagem:
            contagem[t] = 1
          else: contagem[t] += 1


n_words = {}
for palavra in vocabulario:
    words = []
    aux = 0
    for d in splited_doc:
        for p in d:
            if p == palavra:
                aux += 1
        words.append(aux)
        n_words[palavra] = words
        

idf = {}
for palavra in vocabulario:
  aux = 0
  for d in splited_doc:
    if palavra in d:
      aux += 1
    if aux is not 0:
      idf[palavra] = np.log2(len(splited_doc)/aux)
    else: idf[palavra] = 0

tf = {}
for palavra in vocabulario:
  tf_doc = []
  for d in splited_doc:
    aux = 0
    for p in d:
      if p == palavra:
        aux += 1
    if aux is not 0:
      tf_palavra = 1+ np.log2(aux)
      tf_doc.append(tf_palavra)
    else: tf_doc.append(0)
    tf[palavra] = tf_doc
  

#tf_df = pd.DataFrame.from_dict(tf).transpose()
#idf_df = pd.DataFrame(idf,index=[0]).transpose()

#idf_df = idf_df.rename(columns = {0:'idf'})
#aux_list = idf_df['idf'].to_list()

#score_df = tf_df.mul(aux_list)


tf_idf = tf.copy()

for p in tf.keys():
  tfidf = []
  for value in tf[p]:
    score = value * idf[p]
    tfidf.append(score)
  tf_idf.append(tfidf)

