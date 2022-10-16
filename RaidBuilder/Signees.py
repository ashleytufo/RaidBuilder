from Query import Query


class Signee:
  # Signee class records data for each discord player in signups

  # Constructor method to fill in signee attributes
  def __init__(self, signup_id, name, wClass=None, role=None, status="Present"):
    self.signup_id = signup_id
    self.name = name
    self.wClass = wClass
    self.role = role
    self.status = status

    newQuery = Query()
    abrvName = newQuery.getThisPlayer(str(self.name))
    if abrvName is not None:
      self.name = abrvName[0]
    newQuery = Query()
    newQuery.setSignee(self.signup_id, self.name, self.wClass, self.role, self.status)

  def getSignupId(self):
    return self.signup_id

  def getName(self):
    return self.name

  def getWclass(self):
    return self.wClass

  def getRole(self):
    return self.role

  def getStatus(self):
    return self.status

  def showInfo(self):
    print(self.signup_id)
    print(self.name)
    print(self.wClass)
    print(self.role)
    print(self.status)
