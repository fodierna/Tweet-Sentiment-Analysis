from bson.code import Code
import pymongo
from pymongo import MongoClient

client = MongoClient("localhost", 27017, maxPoolSize=50)
db = client.get_database('sentanalysis')
sentimentoCol = db['sentimento']
risorsaCol = db['risorsa']
tweetCol = db['tweet']

mapper = Code("""
               function () {
               var x =this.name; 

                    this.t.forEach(function(z){ 
                            emit(z,{a:x ,b:1}); 
                    });
                }
            """)


reducer = Code("""
                function (key, values) {
                var tot=0;
                var totalAnger = 0;
                var totalDisgust = 0;
                var totalFear = 0;
                var totalJoy = 0;
                var totalSadness = 0;
                var totalSurprise = 0;
                var totalAnticipation=0;
                var totalTrust=0
                for (var i = 0; i < values.length; i++) { 
                    if (values[i].a=="anger"){
                    totalAnger += values[i].b;
                    }

                  if (values[i].a=="anticipation"){
                    totalAnticipation += values[i].b;
                    }

                  if (values[i].a=="disgust"){

                    totalDisgust += values[i].b;
                    }

                  if (values[i].a=="fear"){
                        totalFear += values[i].b;
                  }
                  if (values[i].a=="joy"){

                    totalJoy += values[i].b;
                  }
                  if (values[i].a=="sadness"){

                    totalSadness += values[i].b;
                  }
                  if (values[i].a=="surprise"){

                    totalSurprise += values[i].b;
                  }
                  if (values[i].a=="trust"){

                    totalTrust += values[i].b;
                  }
                  }
                  return {anger:totalAnger, anticipation:totalAnticipation, disgust:totalDisgust,fear:totalFear,joy:totalJoy,sadness:totalSadness,surprise:totalSurprise,trust:totalTrust};


                }
                """)



result = tweetCol.map_reduce(mapper, reducer, "myresults")
for x in result.find({}):
    print (x)
