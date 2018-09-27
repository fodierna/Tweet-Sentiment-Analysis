import elaborazione_tweet
from elaborazione_tweet import *
import os
import codecs
import json
import nltk
from classi import *
pathRisorse= "C:\\Users\\ODIERNA FRANCESCO\\PycharmProjects\\laboratoriodb\\Risorse"
outputTweetPath= "C:\\Users\\ODIERNA FRANCESCO\\PycharmProjects\\laboratoriodb\\Output"





''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def creaDB(name):
    conn = connect(name, host='localhost', port=27017)
    print conn[name]
    #conn.drop_database(name)
    return connect(name, host='localhost', port=27017)

# elimina le parole composte
def processWord(line):
    if line.find("_")==-1:
        line = re.sub("\n", "", line)
        return line
    else:
        return 0


def loadRisorse ():
    f = open("C:\Users\ODIERNA FRANCESCO\PycharmProjects\laboratoriodb\Tmp\oracle.txt", "w")
    for folderSentimento in os.listdir(pathRisorse):# per ogni sentimento
        sentimentList = {}

        for file in os.listdir(pathRisorse + "\\" + folderSentimento):              # per ogni file presente nelle cartelle sentimento (Anger, Anticipation, ecc...)
            path_of_file= pathRisorse + "\\" + folderSentimento + "\\" + file
            column=file.split("_")[0] # estrae dal file EMOSn, NRC o sentisense

            if file.endswith(".txt"):

                with open(path_of_file) as my_file:             # leggi file sentimento
                    lines = my_file.readlines()

                for line in lines:                      # processa le linee del file
                    line=processWord(line)

                    if line == 0:                       # _ presente nella parola -> next
                        continue
                    else:
                        if line not in sentimentList.keys():    # se parola non e' una chiave SentimentList aggiungila
                            sentimentList[line] = {}

                        sentimentList[line][column] = 1         # parola presente in uno dei file del sentimento






        # per ogni parola verifica la presenza nei file dello stesso sentimento

        posts = []
        for lemma in sentimentList.keys():
            # calcola di nuovo la colonna (per sentimento)
            cols = sentimentList[lemma].keys()

            # per specificare che la parola proviene dal file EmoSN o NRC o sentisense
            if "EmoSN" in cols:
                emoSNtmp = sentimentList[lemma]["EmoSN"]
            else:
                emoSNtmp = 0


            if "sentisense" in cols:
                sentisensetmp = sentimentList[lemma]["sentisense"]
            else:
                sentisensetmp = 0


            if "NRC" in cols:
                nrctmp = sentimentList[lemma]["NRC"]
            else:
                nrctmp = 0


            post_2 = risorsa(
                lemma=lemma,
                EmoSN=emoSNtmp,
                sentisense =sentisensetmp,
                NRC =nrctmp,
                sentiment = folderSentimento,
                frequency = 0
            )

            print >> f, lemma +" "+str(emoSNtmp) +" "+str(sentisensetmp)+" "+str(nrctmp)+" "+folderSentimento+","

            post_2.save()               #salva la risorsa sul DB
            posts.append(post_2)        #salva la risorsa come parola del sentimento corrente


        post = sentimento(
            name = folderSentimento, # nome cartella sentimento
            risorse = posts # parole nei relativi file con riferimento a risorsa
        )



        post.save()            # carica il sentimento sul database



def caricatweet():

    for file in os.listdir(outputTweetPath):                            #per ogni sentimento

        with codecs.open(os.path.join(outputTweetPath, file), "r", encoding="utf8") as ds:
            tweets = ds.read().replace("\\n", "") # eliminazione dei caratteri di escape \n
            sent = file.split("_")[2]   # estrai il sentimento corrente dai file contenuti in output

            print sent

            # creazione token list
            tokenList = word_tokenize(tweets) # nltk estrae le parole dai tweet
            tokenList = processSlang(tokenList) # sostituzione slang word con che sono nella token list
            tokenList = word_tokenize(" ".join(tokenList)) # dopo aver sostituito le slang word rieffettuo la tokenizzazione
            tokenList = processStopwords(tokenList) # eliminazione stop word
            sno = nltk.stem.PorterStemmer() # invocazione stemmer
            tokenList = [sno.stem(word) for word in tokenList] # eliminazione forme in ing, ed, ecc tramite lo stemmer
            # tokenList=nltk.pos_tag(tokenList) #tag pos della token list

            # preparazione del tweet per il caricamento nel DB

            post = tweet(
                name=sent,
                t=tokenList,
                emo=json.dumps((elaborazione_tweet.emojiList[sent])),
                hashtag=json.dumps((elaborazione_tweet.hashtag[sent]))

            )
            post.save()             #salva il tweet pulito insieme al dizionario degli hashtag e delle emo











''''''''''''''''''''''''''''''''''''''''___main___'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

if __name__ == "__main__":

    # creaDB("sentanalysis")
    # loadRisorse()
    # elaborazione_tweet.process()
    # caricatweet()