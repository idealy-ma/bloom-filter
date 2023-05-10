#!/usr/bin/python
import hashlib

# creation d'une liste de mot de passe ok
# hachage des liste en sha256 et stockage dans un fichier texte
def readFile(origin):
    content = []
    with open(origin, "r") as origin:
        for line in origin :
            line = line.strip()
            content.append(line)

    return content

def singleSHA256(word):
    # Convertir le mot en byte
    word_bytes = word.encode('utf-8')

    # Transformer les mot en sha256
    hash_object = hashlib.sha256(word_bytes)
    hash_hex = hash_object.hexdigest()

    return hash_hex

def createSHA256(table):
    contentSHA256 = []

    for word in table :
        
        #ajouter le resultat
        contentSHA256.append(singleSHA256(word))

    return contentSHA256

def createHash(origin, destination):
    sha256Table = createSHA256(readFile(origin))
    
    with open(destination, "w+") as destination:
        for word in sha256Table :
            destination.write(word+"\n")


# creation des 3 fonction de hachage
def myHashOne(word):
    hash_value = 0
    for w in word:
        hash_value += ord(w)
    return(hash_value)

def myHashTwo(word):
    hash_val = 0
    for char in word :
        hash_val = (hash_val << 2) ^ (hash_val >> 28) ^ ord(char)
    return hash_val%1000000000

def myHashThree(word):
    hash_val = 0
    for char in word :
        hash_val = (hash_val << 2) ^ (hash_val >> 28) 
    return hash_value

# creation de tableau de bit de hashage
def bloomFilter(wordList):
    bloom = 0
    for word in wordList :
        resultOne = myHashOne(word)
        resultTwo = myHashTwo(word)

        bloom |= 1 << resultOne
        bloom |= 1 << resultTwo
    
    return bloom

# test du fonction bloom pour verifier si un mot existe dans la liste noir
def checkWord(word, bloom):
    resultOne = myHashOne(word)
    resultTwo = myHashTwo(word)

    set_one = bloom & (1 << resultOne)
    set_two = bloom & (1 << resultTwo)

    if set_one and set_two :
        return True
    else :
        return False

# verification pour un mot existant
def linearVerification(word, wordList):
    for w in wordList :
        if word == w:
            return True
    return False

# calcule de probabilite de faux positif
def checkFalsePositif(outsideWord, theOrigins):
    if checkWord(outsideWord,bloomFilter(theOrigins)) and (linearVerification(outsideWord, theOrigins) is False):
        return True
    return False

def probabilityOfFalse(outsideWords, theOrigins) :
    numberMaximal = 0
    falsePositifNumber = 0
    for word in outsideWords :
        numberMaximal += 1
        if checkFalsePositif(word, theOrigins) :
            falsePositifNumber += 1

    return falsePositifNumber/numberMaximal

# generation des millions de donnee pour le test de probabilite

# createHash('../data/listenoire', '../data/hash')
sha256Word = readFile('/home/idealy/Documents/GitHub/bloom-filter/data/hash')
word = singleSHA256("empathy")

print("Bloom Filter : ",checkWord(word,bloomFilter(sha256Word)))
print("Linear verification : ",linearVerification(word, sha256Word))