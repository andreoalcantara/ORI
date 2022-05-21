from unicodedata import normalize

def open_vocabulario():
    # abrindo arquivo
    df = open("vocabulario.txt", "r")
    d1 = df.read()
    d1 = d1.split()
    return d1

def abretexto():

    # abrindo arquivo
    df = open("texto.txt", "r")
    d1 = df.read()
    # passando string para lowercase
    d1 = d1.lower()
    # removendo acentos
    d1 = normalize("NFKD",d1).encode('ASCII','ignore').decode("ASCII")
    # removendo pontuação
    punct = [',', '.', '!']
    for c in punct:
        d1 = d1.replace(c, "")
    # atribuindo lista de palavras em words
    words = d1.split()
    # removendo palavras duplicadas
    words = list(dict.fromkeys(words))
    # colocando em ordem alfabertica
    words.sort()
    return words

vocabulario = open_vocabulario()
texto = abretexto()
bagofwords=list()

for i in vocabulario:
    if i in texto:
        bagofwords.append(1)
    else: bagofwords.append(0)

print(bagofwords)