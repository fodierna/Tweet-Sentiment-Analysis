import os
import re
import codecs
import emoji
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



##################### SLANG WORD
slang_words = {'omg': 'oh my god','afaik': 'as far as i know', 'afk': 'away from keyboard', 'asap': 'as soon as possible', 'atk': 'at the keyboard', 'atm': 'at the moment', 'a3': 'anytime, anywhere, anyplace', 'bak': 'back at keyboard', 'bbl': 'be back later', 'bbs': 'be back soon', 'bfn/b4n': 'bye for now', 'brb': 'be right back', 'brt': 'be right there', 'btw': 'by the way', 'b4n': 'bye for now', 'cu': 'see you', 'cul8r': 'see you later', 'cya': 'see you', 'faq': 'frequently asked questions', 'fc': 'fingers crossed', 'fwiw': 'for what it\'s worth', 'fyi': 'for your information', 'gal': 'get a life', 'gg': 'good game', 'gmta': 'great minds think alike', 'gr8': 'great!', 'g9': 'genius', 'ic': 'i see', 'icq': 'i seek you', 'ilu': 'ilu: i love you', 'imho': 'in my honest opinion', 'imo': 'in my opinion', 'iow': 'in other words', 'irl': 'in real life', 'kiss': 'keep it simple, stupid', 'ldr': 'long distance relationship', 'lmao': 'laugh my a.. off', 'lol': 'laughing out loud', 'ltns': 'long time no see', 'l8r': 'later', 'mte': 'my thoughts exactly', 'm8': 'mate', 'nrn': 'no reply necessary', 'oic': 'oh i see', 'pita': 'pain in the a..', 'prt': 'party', 'prw': 'parents are watching', 'qpsa?': 'que pasa?', 'rofl': 'rolling on the floor laughing', 'roflol': 'rolling on the floor laughing out loud', 'rotflmao': 'rolling on the floor laughing my a.. off','sk8': 'skate', 'stats': 'your sex and age', 'asl': 'age, sex, location', 'thx': 'thank you', 'ttfn': 'ta-ta for now!', 'ttyl': 'talk to you later', 'u': 'you', 'u2': 'you too', 'u4e': 'yours for ever', 'wb': 'welcome back', 'wtf': 'what the f...', 'wtg': 'way to go!', 'wuf': 'where are you from?', 'w8': 'wait...', '7k': 'sick:-d laugher'}
slang_words["bfn"] = slang_words["bfn/b4n"]
slang_words["b4n"] = slang_words["bfn/b4n"]
hashtag={}
emojiList={}


##################### PATTERN EMOJI
try:
    # UCS-4
    patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
except re.error:
    # UCS-2
    patt = re.compile(
        u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')

# pattern emoji regexp per estrapolare empoji dal testo
muf = re.compile(emoji.get_emoji_regexp())


##################### PATH
tweets ="C:\\Users\\ODIERNA FRANCESCO\\PycharmProjects\\laboratoriodb\\Tweets"
tmp ="C:\\Users\\ODIERNA FRANCESCO\\PycharmProjects\\laboratoriodb\\Tmp"
outputPath="C:\\Users\\ODIERNA FRANCESCO\\PycharmProjects\\laboratoriodb\\Output"

# estrapola parole che non c'entrano
def elaboraWC(diz):
    v=["...", "o_o", "f", "a..", "p", "na", "dx", "fml"]


    for x in v:
        if diz.has_key(x):
            diz.pop(x)

    return diz

##################### ELIMINA PUNTEGGIATURA E SIMBOLI
def processPunt(tweet):

    tweet = re.sub(r'[^\w]', ' ', tweet) # regexp che conserva solo i caratteri

    return tweet


##################### CONTEGGIO E RIMOZIONE HASHTAG per parola
def processHash(tweet, sent):

    for word in (tweet.split(" ")):
        if str(word).startswith("#"): # se la parola e' un hashtag
            word = re.sub("\n", "", str(word))
            #print word ##################################################
            if hashtag.has_key(word): # se l'hashtag esiste gia'
                if hashtag[word].has_key(sent): # ed e' un sentimento presente nella collezione
                    hashtag[word][sent]+=1 #lo conta
                else:
                    hashtag[word][sent] = 1 # altrimenti crea il sentimento
            else:
                hashtag[word]={} # se non esiste crea l'hashtag
                hashtag[word][sent] = 1 # lo associa al sentimento e conta 1 occorrenza

            tweet = re.sub("#", "", tweet)
    return tweet

##################### CONTEGGIO E RIMOZIONE HASHTAG per sentimento
def processHashnew(tweet, sent):

    for word in (tweet.split(" ")):
        if str(word).startswith("#"):
            word = re.sub("\n", "", str(word))
            #print word ##################################################
            if hashtag.has_key(sent): # se il sentimento e' presente nella collezione
                if hashtag[sent].has_key(word): # e se l'hashtag e' gia' presente
                    hashtag[sent][word]+=1 # lo conta
                else:
                    hashtag[sent][word] = 1 # altimenti crea l'hashtag
            else:
                hashtag[sent]={} # se il sentimento non esiste, lo crea
                hashtag[sent][word] = 1 # lo associa alla parola e conta 1 occorrenza

            tweet = re.sub("#", " ", tweet)
    return tweet
##################### ELIMINAZIONE EMOJI

def processEmo(text, sent):
    text_has_emoji(text, sent) # controlla se ci emoji sono nel testo e le mette nel vettore (emoji divise per sentimento, quindi e' una matrice)
    return re.sub(muf, " ", text) # elimina le emoji dal testo




def text_has_emoji(text, sent):
    tot=0
    if emojiList.has_key(sent): # se nella emoji list e' gia' presente il sentimento, va avanti
        pass
    else:
        emojiList[sent]={} # altrimenti lo aggiunge


    for character in text:
        if character in emoji.UNICODE_EMOJI: # se il carattere considerato e' una emoji
            tot+=1 # conta le emoji

            #print character
            if emojiList[sent].has_key(character): # se la collezione considerata per sentimento ha il carattere
                emojiList[sent][character] += 1 # lo conta

            else:
                emojiList[sent][character]=1 # altrimenti lo crea e lo setta a 1



    print tot
    #print emojiList
    return text

##################### PROCESSAMENTO RIGHE TWEETS
def processRow(tweet, sent):

    # elimina gli URl
    tweet = re.sub("URL", ' ', tweet).strip()

    # elimina gli USERNAME
    tweet = re.sub("USERNAME", ' ', tweet).strip()

    # porta tutto il tweet in lowecase
    tweet.lower()

    # rimuove gli hashtag dal tweet
    tweet = processHashnew(tweet, sent)

    # elimina la punteggiatura, quindi anche le emoticon
    tweet = processPunt(tweet)

    # rimuove gli spazi bianchi addizionali
    tweet=re.sub("\d+", ' ', tweet)

    # elimina gli underscore inserendo uno spazio vuoto
    tweet=re.sub("_", ' ', tweet)

    # elimina gli spazi indipendentemente dall loro lunghezza
    tweet = re.sub('[\s]+', ' ', tweet)

    # elimina i new line
    tweet = re.sub('[\n]+', ' ', tweet)


    return tweet


##################### PROCESSAMENTO STOP WORDS DA LISTA
def processStopwords(word_list):
    processed_word_list = []
    for word in word_list:
        if (word) not in stopwords.words("english"):
            processed_word_list.append(word)
    return processed_word_list

def processSlang(tweetList):
    for index,word in enumerate(tweetList):
        if word in slang_words.keys():
            tweetList[index]=slang_words[word]

    return tweetList


def process():

    newtext=""
    for file in os.listdir(tweets):
        fp = open(os.path.join(outputPath, file), "w")
        with codecs.open(os.path.join(tweets, file), 'r', encoding='utf8')as data:
            sent=file.split("_")[2]
            print sent
            text81 = data.read() # legge il file
            prova = processEmo(text81, sent) # processa le emoji
        data.close()

        fpp = codecs.open(os.path.join(tmp, file), 'w', encoding='utf8')
        fpp.write(prova)
        fpp.close()

        with open((os.path.join(tmp, file)), "r") as ds:
            lines = ds.readlines()
            for line in lines:
                newline = processRow(line, sent)
                fp.write(newline + "\n") # scrive il file tmp per righe

            ds.close()

        fp.close()
       #print hashtag


    for file in os.listdir(tmp):
        os.remove(os.path.join(tmp, file))



