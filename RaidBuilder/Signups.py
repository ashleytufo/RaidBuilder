from PyQt5.QtCore import QDateTime
from Query import Query
from Signees import Signee
from string import digits
import unidecode
import re

class Signup:

    def __init__(self, signup_name, raid_date, raid_time, signup_text, signup_id=None):
        self.name = signup_name
        self.shortcode = self.name.lower().replace(" ", "_")
        self.date = raid_date
        self.time = raid_time
        self.dateTime = QDateTime(self.date, self.time).toPyDateTime()
        self.signupText = signup_text
        self.signupID = signup_id

        if signup_id is None:
            newQuery = Query()
            newQuery.setSignup(self.name, self.shortcode, self.dateTime,
                               self.signupText)
            idQuery = Query()
            result = newQuery.getThisSignup(self.name)
            newId = result[0]
            self.signupID = newId
        else:
            signupNameQ = Query()
            result = signupNameQ.getThisSignupName(self.signupID)
            if result is not None:
                if result[0] != self.name:
                    newQuery = Query()
                    newQuery.updateSignup(self.name, self.shortcode, self.dateTime,
                                        self.signupText, self.signupID)
                else:
                    newQuery = Query()
                    newQuery.updateLimSignup(self.dateTime, self.signupText, self.signupID)

        self._parse_signees()

    def setName(self):
        pass

    def setDate(self):
        pass

    def setTime(self):
        pass

    def setText(self):
        pass

    def getName(self):
        pass

    def getDate(self):
        pass

    def getTime(self):
        pass

    def getText(self):
        return self.signupText

    def _add_signees(self, line, status="Present"):
        res = re.search(':(.*):', line)
        role = None
        wClass = None
        tempPlayer = str(line)
        if res is not None:
            icon = res.group(0)
            tempPlayer = tempPlayer.replace(icon, "")
            newQuery = Query()
            result = newQuery.getThisRole(icon)
            if result is not None:
                role = result[2]
                wClass = result[3]

        tempPlayer = tempPlayer.replace(" ", "")
        tempPlayer = tempPlayer.lstrip(digits)
        tempPlayer = tempPlayer.replace('\t', '')\
            .replace(u"\u00A0", '')
        tempPlayer = tempPlayer.strip()
        tempPlayer = unidecode.unidecode(tempPlayer)
        player = tempPlayer

        if player == ")" or len(player) < 1:
            pass
        else:
            addPlayer = Signee(int(self.signupID), player, wClass, role, status)

    def _parse_others(self, line):
        lineList = []
        if ":Tentative:" in line:
            status = "Tentative"
            newLine = line.replace(":Tentative: Tentative (", "")\
                .replace(" : ", ", ")
            lineList = newLine.split(",")
        elif ":Absence:" in line:
            status = "Absent"
            newLine = line.replace(":Absence: Absence (", "")\
                .replace(" : ", ", ")
            lineList = newLine.split(",")
        elif ":Late:" in line:
            status = "Late"
            newLine = line.replace(":Late: Late (", "").replace(" : ", ", ")
            lineList = newLine.split(",")
        elif ":Bench:" in line:
            status = "Bench"
            newLine = line.replace(":Bench: Bench (", "").replace(" : ", ", ")
            lineList = newLine.split(",")

        for item in lineList:
            self._add_signees(item, status)

    def _parse_signees(self):
        textToList = self.signupText.split("\n")

        for line in textToList:
            if len(line) < 1:
                pass
            elif "Tentative" in line or "Absence" in line or "Late" in line\
                    or "Bench" in line:
                self._parse_others(line)
            else:
                match = re.search('^.*?\([^\d]*(\d+)[^\d]*\).*$', line)
                if match is not None or len(line) < 1:
                    pass
                else:
                    self._add_signees(line)
