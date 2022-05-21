from unicodedata import normalize

def to_bagofwords():
    # abrindo arquivo
    df = open("qualquer.txt", "r")
    d1 = df.read()
    print(d1)
    #passando string para lowercase
    d1 = d1.lower()
    #removendo acentos
    d1 = normalize("NFKD",d1).encode('ASCII','ignore').decode("ASCII")
    #removendo pontuação
    punct = [',','.','!',';','?']
    for c in punct:
        d1 = d1.replace(c,"")
    #atribuindo lista de palavras em words
    words = d1.split()
    #removendo palavras duplicadas
    words = list(dict.fromkeys(words))
    #colocando em ordem alfabertica
    words.sort()
    return words
def printbag(bag):
    for c in bag:
        print(c)

bag = to_bagofwords()

vocabulario = open("vocabulario.txt", "w")
for i in bag:
    vocabulario.write(i + '\n')
vocabulario.close()
printbag(bag)


