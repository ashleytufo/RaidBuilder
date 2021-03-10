from Query import Query
import datetime


class Roster:

    def __init__(self, raid, rosterJson):
        self.raid = raid
        self.roster = rosterJson
        self.createdOn = datetime.datetime.now()
        self.tempDate = self.createdOn.strftime("%d/%b/%y @%H:%M")
        self.name = self.raid + " (saved " + str(self.tempDate) + ")"
        newQuery = Query()
        newQuery.setRoster(self.name, self.raid, self.roster, self.createdOn)

    def getRaid(self):
        return self.raid

    def getCreatedOn(self):
        return self.createdOn

    def getName(self):
        return self.name

    def getRoster(self):
        return self.roster
