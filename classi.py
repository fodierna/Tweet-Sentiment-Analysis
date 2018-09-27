from mongoengine import *


# modella la risorsa

class risorsa(Document):
    lemma = StringField(required=True)
    sentiment = StringField(required=True)
    EmoSN = IntField()
    sentisense = IntField()
    NRC = IntField()
    frequency = IntField()

# modella il sentimento e lega risorse a risorsa

class sentimento(Document):
    name=StringField()
    risorse = ListField(ReferenceField(risorsa))

#modella il tweet

class tweet(Document):
    name=StringField()
    t=ListField(StringField())
    emo = StringField()
    hashtag = StringField()
