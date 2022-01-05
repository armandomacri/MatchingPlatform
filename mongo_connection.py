import pymongo

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
        return MongoConnection.DATABASE['Users'].find_one({"username": username})


    # restituisce None se non trova nulla altrimenti restituisce il documento aggiornato
    @staticmethod
    def add_username():
        return MongoConnection.DATABASE['Users'].find_one_and_update({"fname": 'Armando'},
                                         {"$set": {"username": "armandomacri"}})

if __name__ == '__main__':
    database = MongoConnection()
    database.initialize()
    print(database.get_user('armandomacri'))

