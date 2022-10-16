from Query import Query


class Player:
  # Players class records data for each discord player in signups

  # Constructor method to fill in player attributes
  def __init__(self, name, aliases, toons=None, raidlead=False, guildie=False, buyer=False, carry=False,
               fav=False, badList=False, prio=0, p_id=None):
    """
    discord: the nickname that appears in the signup
    guildie: True if the player belongs to UBI or Antiquity
    buyer: True if the player mainly comes to buy gear
    carry: True if the player can carry others through
    prio: Numeric value representing their priority for raid building.
        Highest num = highest prio
    """
    self.discord = name
    self.aliases = aliases
    self.toons = toons
    self.raidlead = raidlead
    self.guildie = guildie
    self.buyer = buyer
    self.carry = carry
    self.fav = fav
    self.badList = badList
    self.prio = prio
    self.p_id = p_id

    # TODO: Add Player functionality
    # if p_id is None:
    # newQuery = Query()
    # newQuery.setPlayer()
    # idQuery = Query()
    # result = idQuery.getThisPlayer(self.discord)
    # newId = result[0]
    # self.p_id = newId
    # pass
    # else:
    # signupNameQ = Query()
    # result = signupNameQ.getThisSignupName(self.signupID)
    # if result is not None:
    #     if result[0] != self.name:
    #         newQuery = Query()
    #         newQuery.updateSignup(self.name, self.shortcode, self.dateTime,
    #                             self.signupText, self.signupID)
    #     else:
    #         newQuery = Query()
    #         newQuery.updateLimSignup(self.dateTime, self.signupText, self.signupID)
    # pass
    # TODO: Set toons
    # if self.toons is not None:
    #     newQuery = Query()
    #     newQuery.setToons(self.toons)

  def getDiscord(self):
    return self.discord

  def setDiscord(self, newDisc):
    self.discord = newDisc

  def getGuildie(self):
    return self.guildie

  def setGuildie(self, newGuildie):
    self.guildie = newGuildie
    self._set_Prio()

  def getBuyer(self):
    return self.buyer

  def setBuyer(self, newBuyer):
    self.buyer = newBuyer
    self._set_Prio()

  def getCarry(self):
    return self.carry

  def setCarry(self, newCarry):
    self.carry = newCarry
    self._set_Prio()

  def getFav(self):
    return self.fav

  def setFav(self, newFav):
    self.fav = newFav
    self._set_Prio()

  def getBadList(self):
    return self.badList

  def setBadList(self, newBad):
    self.badList = newBad
    self._set_Prio()

  def getPrio(self):
    return self.prio

  def _set_Prio(self):
    r = 0
    g = 0
    b = 0
    c = 0

    if self.raidlead:
      r = 1
    if self.guildie:
      g = 3
    if self.buyer:
      b = 3
    if self.carry:
      c = 3

    if self.badList:
      newPrio = -10
    elif self.fav:
      newPrio = 10
    else:
      newPrio = r + g + b + c

    self.prio = newPrio
