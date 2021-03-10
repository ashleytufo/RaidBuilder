import sqlite3
import sys
from os import path


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)


class Query:
    db = sqlite3.connect(resource_path('raidbuilder.db'))
    # cursor = db.cursor()

    def __init__(self, player=None, signee=None, signup=None):
        self.player = player
        self.signee = signee
        self.signup = signup

    def setPlayer(self, player):
        pass

    def setToon(self, toon):
        pass

    def setSignee(self, signup_id, name, wClass, role, status):
        cursor = self.db.cursor()
        params = (signup_id, name, wClass, role, status)
        command = """ INSERT INTO rb_signees (Signup_ID, Discord_Name,
                    Class, Role, Status) VALUES (?, ?, ?,
                    ?, ?); """
        cursor.execute(command, params)
        self.db.commit()

    def setSignup(self, signup_name, signup_shortcode, raid_dateTime,
                  signup_text):
        cursor = self.db.cursor()
        params = (signup_name, signup_shortcode, raid_dateTime, signup_text)
        command = """ INSERT INTO rb_signups (Signup_Name, Name_Shortcode,
                    Raid_Date_Time, Signup_Text) VALUES (?, ?, ?, ?); """
        cursor.execute(command, params)
        self.db.commit()

    def setRoster(self, name, raid, roster, created):
        cursor = self.db.cursor()
        params = (name, raid, roster, created)
        command = """ INSERT INTO rb_rosters (Name, Raid, Roster, CreatedOn) VALUES
                    (?, ?, ?, ?); """
        cursor.execute(command, params)
        self.db.commit()
    
    def deleteSignup(self, signup_id):
        cursor = self.db.cursor()
        params = (signup_id, signup_id)
        command = "DELETE FROM rb_signees WHERE Signup_ID = ?;DELETE FROM rb_signups WHERE ID = ?;"
        cursor.execute(command, params)
        self.db.commit()

    def deleteAllSignees(self, signup_id):
        cursor = self.db.cursor()
        params = (str(signup_id),)
        command = "DELETE FROM rb_signees WHERE Signup_ID = ?;"
        cursor.execute(command, params)
        self.db.commit()

    def deleteThisSignee(self, signup_id, signee_id):
        cursor = self.db.cursor()
        params = (signup_id, signee_id)
        command = "DELETE FROM rb_signees WHERE Signup_ID = ? and ID = ?;"
        cursor.execute(command, params)
        self.db.commit()

    def updateSignup(self, signup_name, signup_shortcode, raid_dateTime,
                     signup_text, signupID):
        cursor = self.db.cursor()
        params = (signup_name, signup_shortcode, raid_dateTime, signup_text, signupID)
        command = """ UPDATE rb_signups SET Signup_Name=?, Name_Shortcode=?,
                    Raid_Date_Time=?, Signup_Text=? WHERE ID = ?; """
        cursor.execute(command, params)
        self.db.commit()
    
    def updateLimSignup(self, raid_dateTime, signup_text, signupID):
        cursor = self.db.cursor()
        params = (raid_dateTime, signup_text, signupID)
        command = """ UPDATE rb_signups SET Raid_Date_Time=?, Signup_Text=? WHERE ID = ?; """
        cursor.execute(command, params)
        self.db.commit()

    def getPlayers(self):
        cursor = self.db.cursor()
        command = """ SELECT ID, Discord_Name, RaidLead, Guildie, Buyer, Carry,
                    Favorite, Shitlist, Priority, Aliases, Toons FROM rb_players"""
        result = cursor.execute(command)
        return result

    def getSearchedPlayers(self, searchText):
        cursor = self.db.cursor()
        command = """ SELECT ID, Discord_Name, RaidLead, Guildie, Buyer, Carry,
                    Favorite, Shitlist, Priority, Aliases, Toons FROM rb_players WHERE Discord_Name LIKE
                    '%{}%' OR Aliases LIKE
                    '%{}%';""".format(searchText, searchText)
        result = cursor.execute(command)
        return result

    def getSelectedPlayersInfo(self, p_id):
        cursor = self.db.cursor()
        command = """ SELECT Aliases, RaidLead, Guildie, Buyer, Carry,
                    Favorite, Shitlist FROM rb_players
                    WHERE ID = {};""".format(p_id)
        result = cursor.execute(command).fetchone()
        return result

    def getSelectedPlayersToons(self, p_id):
        cursor = self.db.cursor()
        command = """ SELECT Toons FROM rb_players
                    WHERE ID = {};""".format(p_id)
        result = cursor.execute(command).fetchone()
        return result

    def getSelectedPlayersID(self, p_name):
        cursor = self.db.cursor()
        command = """ SELECT ID FROM rb_players
                    WHERE Discord_Name = '{}';""".format(p_name)
        result = cursor.execute(command).fetchone()
        return result

    def getThisPlayer(self, name):
        cursor = self.db.cursor()
        command = """ SELECT Discord_Name from rb_players
                    WHERE Abrv = '{}'; """.format(name)

        result = cursor.execute(command).fetchone()
        return result

    def getToon(self, p_name):
        cursor = self.db.cursor()
        command = """ SELECT Toons from rb_players
                    WHERE Discord_Name = '{}'; """.format(p_name)

        result = cursor.execute(command).fetchone()
        return result

    def getSignee(self, signupName=None, name=None, wClass=None, role=None,
                  status=None):
        cursor = self.db.cursor()
        if signupName is not None:
            command = """ SELECT Role, Discord_Name, Status FROM rb_signees
                        WHERE Signup_ID = (SELECT ID from rb_signups
                        WHERE Signup_Name = '{}'); """.format(signupName)

        result = cursor.execute(command)
        return result

    def getSignup(self, signupName=None, signupID=None):
        cursor = self.db.cursor()
        if signupName is None and signupID is None:
            command = """ SELECT Signup_Name FROM rb_signups ORDER BY ID; """
        elif signupName is None and signupID is not None:
            command = """ SELECT Signup_Name from rb_signups
                        WHERE ID = {}; """.format(signupID)
        elif signupName is not None and signupID is None:
            command = """ SELECT ID from rb_signups
                        WHERE Signup_Name = '{}'; """.format(signupName)

        result = cursor.execute(command)
        return result

    def getThisSignup(self, signupName):
        cursor = self.db.cursor()
        command = """ SELECT ID from rb_signups
                    WHERE Signup_Name = '{}'; """.format(signupName)

        result = cursor.execute(command).fetchone()
        return result

    def getThisSignupName(self, signupID):
        cursor = self.db.cursor()
        command = """ SELECT Signup_Name from rb_signups
                    WHERE ID = {}; """.format(signupID)

        result = cursor.execute(command).fetchone()
        return result

    def getSignupText(self, signupName):
        cursor = self.db.cursor()
        command = """ SELECT Signup_Text from rb_signups
                    WHERE Signup_Name = '{}'; """.format(signupName)

        result = cursor.execute(command)
        return result

    def getRoster(self, name):
        cursor = self.db.cursor()
        command = """ SELECT Roster from rb_rosters
                    WHERE Name = '{}'; """.format(name)

        result = cursor.execute(command).fetchone()
        return result

    def getRosterRaid(self, name):
        cursor = self.db.cursor()
        command = """ SELECT Raid from rb_rosters
                    WHERE Name = '{}'; """.format(name)

        result = cursor.execute(command).fetchone()
        return result

    def getRosters(self):
        cursor = self.db.cursor()
        command = """ SELECT Name FROM rb_rosters ORDER BY CreatedOn; """

        result = cursor.execute(command)
        return result

    def getRoles(self):
        cursor = self.db.cursor()
        command = "SELECT * from rb_roles; "
        result = cursor.execute(command)
        return result

    def getThisRole(self, icon):
        cursor = self.db.cursor()
        command = "SELECT * from rb_roles where IconName = '{}'; ".format(icon)
        result = cursor.execute(command).fetchone()
        return result

