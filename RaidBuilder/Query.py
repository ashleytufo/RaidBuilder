import sqlite3
import sys
from os import path


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)

class Query:
    db = sqlite3.connect(resource_path('raidbuilder.db'))
    cursor = db.cursor()

    def __init__(self, player=None, signee=None, signup=None):
        self.player = player
        self.signee = signee
        self.signup = signup

    def setPlayer(self, player):
        pass

    def setToon(self, toon):
        pass

    def setSignee(self, signup_id, name, wClass, role, status):
        params = (signup_id, name, wClass, role, status)
        command = """ INSERT INTO rb_signees (Signup_ID, Discord_Name,
                    Class, Role, Status) VALUES (?, ?, ?,
                    ?, ?); """
        self.cursor.execute(command, params)
        self.db.commit()

    def setSignup(self, signup_name, signup_shortcode, raid_dateTime,
                  signup_text):
        params = (signup_name, signup_shortcode, raid_dateTime, signup_text)
        command = """ INSERT INTO rb_signups (Signup_Name, Name_Shortcode,
                    Raid_Date_Time, Signup_Text) VALUES (?, ?, ?, ?); """
        self.cursor.execute(command, params)
        self.db.commit()

    def setRoster(self, raid, grp1, grp2, grp3, grp4, grp5, grp6, grp7, grp8, sb1, sb2):
        params = (raid, grp1, grp2, grp3, grp4, grp5, grp6, grp7, grp8, sb1, sb2)
        command = """ INSERT INTO rb_rosters (Raid, Group1, Group2, Group3, Group4,
                    Group5, Group6, Group7, Group8, Standby1, Standby2) VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """
        self.cursor.execute(command, params)
        self.db.commit()

    def getPlayers(self):
        command = """ SELECT ID, Discord_Name, RaidLead, Guildie, Buyer, Carry, Favorite, Shitlist from rb_players"""
        result = self.cursor.execute(command)
        return result

    def getPlayer(self, name):
        command = """ SELECT Discord_Name from rb_players
                    WHERE Abrv = '{}'; """.format(name)

        result = self.cursor.execute(command).fetchone()
        return result

    def getToon(self, toon):
        pass

    def getSignee(self, signupName=None, name=None, wClass=None, role=None,
                  status=None):
        if signupName is not None:
            command = """ SELECT Role, Discord_Name, Status FROM rb_signees
                        WHERE Signup_ID = (SELECT ID from rb_signups
                        WHERE Signup_Name = '{}'); """.format(signupName)

        result = self.cursor.execute(command)
        return result

    def getSignup(self, signupName=None, signupID=None):
        if signupName is None and signupID is None:
            command = """ SELECT Signup_Name FROM rb_signups ORDER BY ID; """
        elif signupName is None and signupID is not None:
            command = """ SELECT Signup_Name from rb_signups
                        WHERE Signup_ID = '{}'; """.format(signupID)
        elif signupName is not None and signupID is None:
            command = """ SELECT ID from rb_signups
                        WHERE Signup_Name = '{}'; """.format(signupName)

        result = self.cursor.execute(command)
        return result

    def getThisSignup(self, signupName):
        command = """ SELECT ID from rb_signups
                    WHERE Signup_Name = '{}'; """.format(signupName)

        result = self.cursor.execute(command).fetchone()
        return result

    def getSignupText(self, signupName):
        command = """ SELECT Signup_Text from rb_signups
                    WHERE Signup_Name = '{}'; """.format(signupName)

        result = self.cursor.execute(command)
        return result

    def getRoster(self, raid):
        command = """ SELECT Group1 from rb_rosters
                    WHERE Raid = '{}'; """.format(raid)

        result = self.cursor.execute(command).fetchone()
        return result

    def getRoles(self):
        command = "SELECT * from rb_roles; "
        result = self.cursor.execute(command)
        return result

    def getThisRole(self, icon):
        command = "SELECT * from rb_roles where IconName = '{}'; ".format(icon)
        result = self.cursor.execute(command).fetchone()
        return result
