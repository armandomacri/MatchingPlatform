
class User:

    def __init__(self, fname, lname, username, topics):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.sport = [topics['sport'][0], topics['sport'][1]]
        self.world = [topics['world'][0], topics['world'][1]]
        self.business = [topics['business'][0], topics['business'][1]]
        self.science = [topics['science/tech'][0], topics['science/tech'][1]]
        self.alfa = 0.4

    def updateScore(self, topic, score):

        if topic == "sport":
            self.sport[0] = ((self.alfa * self.sport[0]) + ((1 - self.alfa) * score))
            self.sport[1] = self.sport[1] + 1
            return self.username, self.sport[0], self.sport[1]
        if topic == "world":
            self.world[0] = ((self.alfa * self.world[0]) + ((1 - self.alfa) * score))
            self.world[1] = self.world[1] + 1
            return self.username, self.world[0], self.world[1]
        if topic == "business":
            self.business[0] = self.alfa * self.business[0] + (1 - self.alfa) * score
            self.business[1] = self.business[1] + 1
            return self.username, self.business[0], self.business[1]
        if topic == "science/tech":
            self.science[0] = ((self.alfa * self.science[0]) + ((1 - self.alfa) * score))
            self.science[1] = self.science[1] + 1
            return self.username, self.science[0], self.science[1]
