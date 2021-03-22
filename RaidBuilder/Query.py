import sqlite3
import sys
from os import path
import logging


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)


class Query:
    pyClassLog = logging.getLogger(__name__)
    db = sqlite3.connect(resource_path('raidbuilder.db'))
    # cursor = db.cursor()

    def __init__(self, player=None, signee=None, signup=None):
        self.player = player
        self.signee = signee
        self.signup = signup

    def setPlayer(self, discName, rl, guildie, buyer, carry, favorite, sl,
                  prio, aliases, toons):
        cursor = self.db.cursor()
        params = (discName, rl, guildie, buyer, carry, favorite, sl, prio,
                  aliases, toons)
        command = """ INSERT INTO rb_players (Discord_Name, RaidLead, Guildie,
                    Buyer, Carry, Favorite, Shitlist, Priority, Aliases, Toons)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.debug("Player %s created in db", discName)

    def setToons(self, toon):
        pass

    def setSignee(self, signup_id, name, wClass, role, status):
        cursor = self.db.cursor()
        params = (signup_id, name, wClass, role, status)
        command = """ INSERT INTO rb_signees (Signup_ID, Discord_Name,
                    Class, Role, Status) VALUES (?, ?, ?,
                    ?, ?); """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.debug("%s added to signup %d", name, signup_id)

    def setSignup(self, signup_name, signup_shortcode, raid_dateTime,
                  signup_text):
        cursor = self.db.cursor()
        params = (signup_name, signup_shortcode, raid_dateTime, signup_text)
        command = """ INSERT INTO rb_signups (Signup_Name, Name_Shortcode,
                    Raid_Date_Time, Signup_Text) VALUES (?, ?, ?, ?); """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.info("Signup %s created in db", (signup_name))

    def setRoster(self, name, raid, roster, created):
        cursor = self.db.cursor()
        params = (name, raid, roster, created)
        command = """ INSERT INTO rb_rosters (Name, Raid, Roster, CreatedOn) VALUES
                    (?, ?, ?, ?); """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.info("Roster %s created in db", (name))
    
    def deleteSignup(self, signup_id):
        cursor = self.db.cursor()
        params = (signup_id, signup_id)
        command = "DELETE FROM rb_signees WHERE Signup_ID = ?;DELETE FROM rb_signups WHERE ID = ?;"
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.info("Signup %d and all signees deleted from db", (signup_id))

    def deleteRoster(self, name):
        cursor = self.db.cursor()
        params = (name,)
        command = "DELETE FROM rb_rosters WHERE Name = ?"
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.info("Roster %s was deleted from db", (name))

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

    def updatePlayer(self, discName, rl, guildie, buyer, carry, favorite, sl,
                     prio, aliases, toons, p_id):
        cursor = self.db.cursor()
        params = (discName, rl, guildie, buyer, carry, favorite, sl, prio,
                  aliases, toons, p_id)
        command = """ UPDATE rb_players Discord_Name=?, RaidLead=?, Guildie=?, Buyer=?, Carry=?,
                    Favorite=?, Shitlist=?, Priority=?, Aliases=?, Toons=? WHERE ID = ?; """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.debug("Player %s updated in db", discName)

    def updateLimPlayer(self, rl, guildie, buyer, carry, favorite, sl,
                        prio, aliases, toons, p_id):
        cursor = self.db.cursor()
        params = (rl, guildie, buyer, carry, favorite, sl, prio,
                  aliases, toons, p_id)
        command = """ UPDATE rb_players RaidLead=?, Guildie=?, Buyer=?, Carry=?,
                    Favorite=?, Shitlist=?, Priority=?, Aliases=?, Toons=? WHERE ID = ?; """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.debug("Player with ID %s updated in db", p_id)

    def updateSignup(self, signup_name, signup_shortcode, raid_dateTime,
                     signup_text, signupID):
        cursor = self.db.cursor()
        params = (signup_name, signup_shortcode, raid_dateTime, signup_text, signupID)
        command = """ UPDATE rb_signups SET Signup_Name=?, Name_Shortcode=?,
                    Raid_Date_Time=?, Signup_Text=? WHERE ID = ?; """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.debug("Signup %s(%d) updated in db", signup_name, signupID)
    
    def updateLimSignup(self, raid_dateTime, signup_text, signupID):
        cursor = self.db.cursor()
        params = (raid_dateTime, signup_text, signupID)
        command = """ UPDATE rb_signups SET Raid_Date_Time=?, Signup_Text=? WHERE ID = ?; """
        cursor.execute(command, params)
        self.db.commit()
        self.pyClassLog.info("Signup %d updated in db", (signupID))

    def getPlayers(self):
        cursor = self.db.cursor()
        command = """ SELECT ID, Discord_Name, RaidLead, Guildie, Buyer, Carry,
                    Favorite, Shitlist, Priority, Aliases, Toons FROM rb_players"""
        result = cursor.execute(command)
        self.pyClassLog.debug("All players retrieved from db")
        return result

    def getSearchedPlayers(self, searchText):
        cursor = self.db.cursor()
        command = """ SELECT ID, Discord_Name, RaidLead, Guildie, Buyer, Carry,
                    Favorite, Shitlist, Priority, Aliases, Toons FROM rb_players WHERE Discord_Name LIKE
                    '%{}%' OR Aliases LIKE
                    '%{}%';""".format(searchText, searchText)
        result = cursor.execute(command)
        self.pyClassLog.debug("%s retrieved from db", (searchText))
        return result

    def getSelectedPlayersInfo(self, p_id):
        cursor = self.db.cursor()
        command = """ SELECT Aliases, RaidLead, Guildie, Buyer, Carry,
                    Favorite, Shitlist FROM rb_players
                    WHERE ID = {};""".format(p_id)
        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Player ID %d info retrieved from db", (p_id))
        return result

    def getSelectedPlayersToons(self, p_id):
        cursor = self.db.cursor()
        command = """ SELECT Toons FROM rb_players
                    WHERE ID = {};""".format(p_id)
        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Player ID %d toons retrieved from db", (p_id))
        return result

    def getSelectedPlayersID(self, p_name):
        cursor = self.db.cursor()
        command = """ SELECT ID FROM rb_players
                    WHERE Discord_Name = '{}';""".format(p_name)
        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Player %s ID retrieved from db", (p_name))
        return result

    def getThisPlayer(self, name):
        cursor = self.db.cursor()
        command = """ SELECT Discord_Name from rb_players
                    WHERE Abrv = '{}'; """.format(name)

        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Player %s abbreviation retrieved from db", (name))
        return result

    def getToon(self, p_name):
        cursor = self.db.cursor()
        command = """ SELECT Toons from rb_players
                    WHERE Discord_Name = '{}'; """.format(p_name)

        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Player %s toons retrieved from db", (p_name))
        return result

    def getSignee(self, signupName=None, name=None, wClass=None, role=None,
                  status=None):
        cursor = self.db.cursor()
        if signupName is not None:
            command = """ SELECT Role, Discord_Name, Status FROM rb_signees
                        WHERE Signup_ID = (SELECT ID from rb_signups
                        WHERE Signup_Name = '{}'); """.format(signupName)

        result = cursor.execute(command)
        self.pyClassLog.debug("Signees for signup %s retrieved from db", str(signupName))
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
        self.pyClassLog.debug("Signup %s retrieved from db", (signupName))
        return result

    def getThisSignupName(self, signupID):
        cursor = self.db.cursor()
        command = """ SELECT Signup_Name from rb_signups
                    WHERE ID = {}; """.format(signupID)

        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Signup with ID of %d retrieved from db", (signupID))
        return result

    def getSignupText(self, signupName):
        cursor = self.db.cursor()
        command = """ SELECT Signup_Text from rb_signups
                    WHERE Signup_Name = '{}'; """.format(signupName)

        result = cursor.execute(command)
        self.pyClassLog.debug("Signup %s retrieved from db", (signupName))
        return result
    
    def getSignupDateTime(self, signupName):
        cursor = self.db.cursor()
        command = """ SELECT Raid_Date_Time from rb_signups
                    WHERE Signup_Name = '{}'; """.format(signupName)

        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Signup %s retrieved from db", (signupName))
        return result

    def getRoster(self, name):
        cursor = self.db.cursor()
        command = """ SELECT Roster from rb_rosters
                    WHERE Name = '{}'; """.format(name)

        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Roster %s retrieved from db", (name))
        return result
    
    def getRosterID(self, name):
        cursor = self.db.cursor()
        command = """ SELECT ID from rb_rosters
                    WHERE Name = '{}'; """.format(name)

        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Roster %s retrieved from db", (name))
        return result

    def getRosterRaid(self, name):
        cursor = self.db.cursor()
        command = """ SELECT Raid from rb_rosters
                    WHERE Name = '{}'; """.format(name)

        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("Roster %s retrieved from db", (name))
        return result
    
    def getAllRosters(self):
        cursor = self.db.cursor()
        command = """ SELECT Roster from rb_rosters; """

        result = cursor.execute(command)
        self.pyClassLog.debug("All rosters retrieved from db")
        return result

    def getRosters(self):
        cursor = self.db.cursor()
        command = """ SELECT Name FROM rb_rosters ORDER BY CreatedOn; """

        result = cursor.execute(command)
        self.pyClassLog.debug("All rosters retrieved from db")
        return result

    def getRoles(self):
        cursor = self.db.cursor()
        command = "SELECT * from rb_roles; "
        result = cursor.execute(command)
        self.pyClassLog.debug("All roles retrieved from db")
        return result

    def getThisRole(self, icon):
        cursor = self.db.cursor()
        command = "SELECT * from rb_roles where IconName = '{}'; ".format(icon)
        result = cursor.execute(command).fetchone()
        self.pyClassLog.debug("%s role retrieved from db", (icon))
        return result

