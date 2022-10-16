from PyQt5.QtCore import QDateTime
from Query import Query
from Signees import Signee
from string import digits
import unidecode
import re


class Signup:
  # Signup class records data for each discord raid signup sheet

  # Constructor method to fill in signup attributes

  def __init__(self, signup_name, raid_date, raid_time, signup_text,
               signup_id=None):
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
      result = idQuery.getThisSignup(self.name)
      newId = result[0]
      self.signupID = newId
    else:
      signupNameQ = Query()
      result = signupNameQ.getThisSignupName(self.signupID)
      if result is not None:
        if result[0] != self.name:
          newQuery = Query()
          newQuery.updateSignup(self.name, self.shortcode,
                                self.dateTime, self.signupText,
                                self.signupID)
        else:
          newQuery = Query()
          newQuery.updateLimSignup(self.dateTime, self.signupText,
                                   self.signupID)

    self._parse_signees()

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

    # Replace characters in player signup text
    tempPlayer = tempPlayer.replace(" ", "")
    tempPlayer = tempPlayer.replace("[", "")
    tempPlayer = tempPlayer.replace("]", "")
    tempPlayer = tempPlayer.lstrip(digits)
    tempPlayer = tempPlayer.strip(digits)
    tempPlayer = tempPlayer.replace('\t', '').replace(u"\u00A0", '')
    tempPlayer = tempPlayer.strip()
    tempPlayer = unidecode.unidecode(tempPlayer)
    player = tempPlayer

    if player == ")" or len(player) < 1:
      pass
    elif self.signupID is not None:
      addPlayer = Signee(int(self.signupID), player, wClass, role, status)

  def _parse_others(self, line):
    lineList = []
    status = ""
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

  def _parse_gb_signees(self, roleList, textToList):
    roleList += ("Sign-ups",)
    split_points = []
    for role in roleList:
      if role in textToList:
        ind = textToList.index(role)
        split_points.append(ind)

    split_list = [textToList[i: j] for i, j in zip([0] + split_points,
                                                   split_points + [None])]
    newList = []
    # Replace GoodBot signup id aliases
    for i in split_list:
      if ":GBtank: Druid" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBtank: Druid",
                           ":Tank: Tank (1):").replace(":GBdruid:", ":Bear:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBtank: Paladin" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBtank: Paladin",
                           ":Tank: Tank (1):").replace(":GBpaladin:", ":ProtPaladin:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBtank: Warrior" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBtank: Warrior",
                           ":Tank: Tank (1):").replace(":GBwarrior:", ":Tank:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBhealer: Druid" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBhealer: Druid",
                           ":Druid: Druid (1):").replace(":GBdruid:", ":RestoDruid:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBhealer: Paladin" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBhealer: Paladin",
                           ":Paladin: Paladin (1) :").replace(":GBpaladin:", ":HolyPaladin:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBhealer: Priest" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBhealer: Priest",
                           ":Priest: Priest (1):").replace(":GBpriest:", ":Priest:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBhealer: Shaman" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBhealer:",
                           ":Shaman: Shaman (1):").replace(":GBshaman:", ":RestoShaman:")
          newI.append(newS)
        newList.append(newI)

      elif ":GBdps: Druid" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBdps: Druid",
                           ":Druid: Druid (1):").replace(":GBdruid:", ":FeralDruid:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBdps: Hunter" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBdps: Hunter",
                           ":Hunter: Hunter (1):").replace(":GBhunter:", ":Hunter:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBdps: Paladin" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBdps: Paladin",
                           ":Paladin: Paladin (1) :").replace(":GBpaladin:", ":RetribPaladin:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBdps: Rogue" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBdps: Rogue",
                           ":Rogue: Rogue (1):").replace(":GBrogue:", ":Rogue:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBdps: Shaman" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBdps: Shaman",
                           ":Shaman: Shaman (1):").replace(":GBshaman:", ":Enhancer:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBdps: Warrior" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBdps: Warrior",
                           ":Warrior: Warrior (1):").replace(":GBwarrior:", ":Warrior:")
          newI.append(newS)
        newList.append(newI)

      elif ":GBcaster: Druid" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBcaster: Druid",
                           ":Druid: Druid (1):").replace(":GBdruid:", ":Balance:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBcaster: Mage" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBcaster: Mage",
                           ":Mage: Mage (1):").replace(":GBmage:", ":Mage:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBcaster: Priest" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBcaster: Priest",
                           ":Priest: Priest (1):").replace(":GBpriest:", ":Shadow:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBcaster: Shaman" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBcaster: Shaman",
                           ":Shaman: Shaman (1):").replace(":GBshaman:", ":ElemShaman:")
          newI.append(newS)
        newList.append(newI)
      elif ":GBcaster: Warlock" in i:
        newI = []
        for s in i:
          newS = s.replace(":GBcaster: Warlock",
                           ":Warlock: Warlock (1):").replace(":GBwarlock:", ":Warlock:")
          newI.append(newS)
        newList.append(newI)

      else:
        newI = []
        for s in i:
          if "Maybe: " in s:
            newS = s.replace("Maybe: ",
                             ":Tentative: Tentative (1) : ")
            newI.append(newS)
          if "No: " in s:
            newS = s.replace("No: ",
                             ":Absence: Absence (1) : ")
            newI.append(newS)
        newList.append(newI)

    raidHelperFrmtList = []
    for i in newList:
      raidHelperFrmtList += i
    return raidHelperFrmtList

  def _parse_signees(self):
    roleList = (":GBtank: Druid", ":GBtank: Paladin", ":GBtank: Warrior",
                ":GBhealer: Druid", ":GBhealer: Paladin",
                ":GBhealer: Priest", ":GBhealer: Shaman", ":GBdps: Druid",
                ":GBdps: Hunter", ":GBdps: Paladin", ":GBdps: Rogue",
                ":GBdps: Shaman", ":GBdps: Warrior", ":GBcaster: Druid",
                ":GBcaster: Mage", ":GBcaster: Priest",
                ":GBcaster: Shaman", ":GBcaster: Warlock")
    goodBot = False

    textToList = self.signupText.split("\n")
    for role in roleList:
      if role in self.signupText:
        goodBot = True

    if goodBot is True:
      textToList = self._parse_gb_signees(roleList, textToList)

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
