
class User:

    def __init__(self, fname, lname, username, topics):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.sport = (topics[0]['sport'], topics[0]['counter'])
        self.world = (topics[1]['world'], topics[1]['counter'])
        self.business = (topics[2]['business'], topics[2]['counter'])
        self.science = (topics[3]['science/tech'], topics[1]['counter'])
