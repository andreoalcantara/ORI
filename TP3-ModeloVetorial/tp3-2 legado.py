import numpy as np
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import os
from unicodedata import normalize

diretorio = 'C:/Users/andre/OneDrive/Área de Trabalho/ORI/TP3-ModeloVetorial/'
vocabulario = 'C:/Users/andre/OneDrive/Área de Trabalho/ORI/TP3-ModeloVetorial/vocabulario.txt'

stop_words = set(stopwords.words('portuguese'))
ps = PorterStemmer()

punct = [',','.','!',';','?','(',')','[',']','{','}']
consulta = input("Digite a cosulta: ")
consulta = consulta.lower().replace('\n', ' ')
consulta = normalize("NFKD",consulta).encode('ASCII','ignore').decode("ASCII")
for c in punct:
    consulta= consulta.replace(c, '')
consulta = word_tokenize(consulta) 
for w in consulta:
    ps.stem(w)

#CASO DE TEST
#d1 = 'to do is to be to be is to do'
#d2 = 'to be or not to be i am what i am'
#d3 = 'i think therefore i am do be do be do'
#d4 = 'do do do da da da let it be let it be'

#documentos = [d1,d2,d3,d4]

#splited_doc = [d1.split(),d2.split(),d3.split(),d4.split()]
#FIM CASO DE TESTE

def lista_documentos(diretorio):
    documentos = list()
    for arquivo in os.listdir(diretorio):
      if arquivo != 'vocabulario.txt' and arquivo != 'vocabulario_teste.txt':
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
    splited_doc.append(word_tokenize(d))
for d in splited_doc:
    for w in d:
        ps.stem(w)
    
#splited_doc = []
#for d in documentos:
#  splited_doc.append(d.split())


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

idf_consulta = {}
for palavra in vocabulario:
  aux = 0
  if palavra in consulta:
    aux += 1
  if aux is not 0:
    idf_consulta[palavra] = np.log2(len(splited_doc)/aux)
  else: idf_consulta[palavra] = 0

tf_consulta = {}
for palavra in vocabulario:
  tf_con = []
  aux = 0
  for p in consulta:
    if p == palavra:
        aux += 1
  if aux is not 0:
      tf_termo = 1+ np.log2(aux)
      tf_con.append(tf_termo)
  else: tf_con.append(0)
  tf_consulta[palavra] = tf_con

tf_idf = {}
for k1, v1 in tf.items():
    for k2,v2 in idf.items():
        if k1==k2:
            val = []
            for i in range(len(v1)):
                val.append( v1[i]*v2)
            tf_idf[k1] = val

tf_idf_consulta = {}
for k1, v1 in tf_consulta.items():
    for k2,v2 in idf_consulta.items():
        if k1==k2:
            val = []
            for i in range(len(v1)):
                val.append( v1[i]*v2)
            tf_idf_consulta[k1] = val
