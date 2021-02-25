from Query import Query
import pickle


class Roster:

    def __init__(self, raid, grp1=[], grp2=[], grp3=[], grp4=[],
                 grp5=[], grp6=[], grp7=[], grp8=[], sb1=[], sb2=[]):
        self.raid = raid
        self.group1 = grp1
        print(self.group1)
        self.group2 = grp2
        self.group3 = grp3
        self.group4 = grp4
        self.group5 = grp5
        self.group6 = grp6
        self.group7 = grp7
        self.group8 = grp8
        self.standby1 = sb1
        self.standby2 = sb2
        newQuery = Query()
        newQuery.setRoster("Hey", pickle.dumps(self.group1), self.group2, self.group3, self.group4, self.group5, self.group6, self.group7, self.group8, self.standby1, self.standby2)
    
    def getGroup(self):
        return self.group1