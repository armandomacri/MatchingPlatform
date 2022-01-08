
class User:

    def __init__(self, fname, lname, username, topics):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.sport = (topics['sport'][0], topics['sport'][1])
        self.world = (topics['world'][0], topics['world'][1])
        self.business = (topics['business'][0], topics['business'][1])
        self.science = (topics['science/tech'][0], topics['science/tech'][1])
