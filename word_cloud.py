import numpy as np # linear algebra
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import  pymongo
from wordcloud import WordCloud, STOPWORDS
import sys
from subprocess import check_output
from elaborazione_tweet import elaboraWC




def plotWordCloud(v, t):

    wc = WordCloud(stopwords=stopwords).generate_from_frequencies(v)
    plt.title(t)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()



'''  main '''

stopwords = set(STOPWORDS)
client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)
db = client.get_database('sentanalysis')
collection = db['myresults']

anger={}
anticipation={}
joy={}
trust={}
disgust={}
fear={}
sadness={}
surprise={}

soglia=1000

for x in collection.find({"value.anger":{'$gte': soglia}}):
    anger[x["_id"]]= x["value"]["anger"]
for x in collection.find({"value.anticipation":{'$gte': soglia}}):
    anticipation[x["_id"]]= x["value"]["anticipation"]
for x in collection.find({"value.joy":{'$gte': soglia}}):
    joy[x["_id"]]= x["value"]["joy"]
for x in collection.find({"value.trust":{'$gte': soglia}}):
    trust[x["_id"]]= x["value"]["trust"]
for x in collection.find({"value.disgust":{'$gte': soglia}}):
    disgust[x["_id"]]= x["value"]["disgust"]
for x in collection.find({"value.fear":{'$gte': soglia}}):
    fear[x["_id"]]= x["value"]["fear"]
for x in collection.find({"value.sadness":{'$gte': soglia}}):
    sadness[x["_id"]]= x["value"]["sadness"]
for x in collection.find({"value.surprise":{'$gte': soglia}}):
    surprise[x["_id"]]= x["value"]["surprise"]

vettori=[surprise, anger, joy, fear, trust, anticipation, disgust, sadness ]
titoli=["Surprise", "Anger", "Joy", "Fear", "Trust", "Anticipation", "Disgust", "Sadness" ]

print vettori
print titoli

for i in range(0, len(vettori)):
    plotWordCloud(vettori[i], titoli[i])




