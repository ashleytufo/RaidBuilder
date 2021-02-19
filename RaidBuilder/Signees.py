import json
from string import digits
import unidecode
import re
from Query import Query

class Signee:
    def __init__(self, signup_id, name, wClass=None, role=None, 
                 status="Present"):
        self.signup_id = signup_id
        self.name = name
        self.wClass = wClass
        self.role = role
        self.status = status

        newQuery = Query()
        newQuery.setSignee(self.signup_id, self.name, self.wClass, self.role, self.status)
        # command = """ INSERT INTO rb_signees (Signup_ID, Discord_Name,
        #                                 Class, Role, Status) VALUES ({}, '{}', '{}',
        #                                 '{}', 'Present'); """.format(3, player, wClass, role)

    def setSignupId(self):
        pass

    def setName(self):
        pass

    def setWclass(self):
        pass

    def setRole(self):
        pass

    def setStatus(self):
        pass

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
