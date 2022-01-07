import pymongo

from utils.utils import User


class MongoConnection(object):
    URI = "mongodb+srv://Industrial:Application@sharedrobotaxi.gnvax.mongodb.net/SharedRobotaxi?retryWrites=true&w=majority"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(MongoConnection.URI)
        MongoConnection.DATABASE = client.SharedRobotaxi

    @staticmethod
    def collections():
        return MongoConnection.DATABASE.list_collection_names()

    @staticmethod
    def get_user(username):

        result = MongoConnection.DATABASE['Users'].find_one({"username": username})
        if result is not None:
            return User(result['fname'], result['lname'], result['username'], result['topics'])


    # restituisce None se non trova nulla altrimenti restituisce il documento aggiornato
    @staticmethod
    def add_username():
        result = MongoConnection.DATABASE['Users'].find_one_and_update({"fname": 'Armando'},
                                         {"$set": {"username": "armandomacri"}})



    @staticmethod
    def get_similar_score_users(username, topic, score):
        pipeline = [
            {"$match":
                 {"$and": [
                     {"username": {"$nin": [username]}},
                     {"topics."+topic+'.0':{"$gte": score-0.01}},
                     {"topics."+topic+'.0':{"$lte": score+0.01}}
                        ]
                },
            },
            {"$sort":{"topics."+topic+'.0': -1}},
            {'$limit': 5}
        ]

        results = MongoConnection.DATABASE['Users'].aggregate(pipeline)
        return results

    @staticmethod
    def update_topic_score(username, topic, score):
        return MongoConnection.DATABASE['Users'].update_one(
                                                    {"username": username},
                                                    {"$set": {"topics."+topic+'.0': score}, "$inc": {"topics."+topic+'.1': 1}},
                                                    upsert=True
                                                    )

if __name__ == '__main__':
    database = MongoConnection()
    database.initialize()

    #p = database.get_similar_score_users("ciao", "business", 0.9234763)

    #print(database.update_topic_score('armandomacri', 'business', 0.3452343))

    p = database.get_similar_score_users('armandomacri', 'business', 0.3452343)
    for doc in p:
        print(doc)


    #print(database.get_user('armandomacri'))



