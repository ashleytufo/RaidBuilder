import json
from string import digits
import unidecode
import re
from Signees import Signee
from Query import Query
import sqlite3

test2Tanks = ["Solu"]
test2Hunters = ["Pinkee/Inthewa"]
test2Druids = ["Andarin"]
test2Warriors = ["Kraw"]
test2Mages = ["HoesKnows"]
test2Shamans = ["Whipsnchains"]
test2Rogues = ["skown"]
test2Warlocks = ["Saccharine-P"]
test2Priests = ["Syzzurp"]
test2Other = [":Late: Late (2) : :Hunter: 16 Babadook/Botanist,", ":Bench: Bench (1) : :Hunter: 54 VeeVee/Scryugemcduk,", ":Tentative: Tentative (2) : :Warrior: 43 Tohroo/Medaka,", ":Absence: Absence (8) : 3 Hellohidead,"]

test3Tanks = ["Dartanko/Darho"]
test3Hunters = ["~Miistie", "Pickwick"]
test3Druids = ["Pamaelic/Ski", "Nale", "Andarin"]
test3Warriors = ["Unkillable(UKZ", "Konquest", "Kraw"]
test3Mages = ["Joshu/Murdok", "Mightymagus", "HoesKnows"]
test3Shamans = ["Ashleys", "Gomes", "Whipsnchains"]
test3Rogues = ["Bettywight/Ath", "Leithia", "skown"]
test3Warlocks = ["Baitlock", "Ashley", "Saccharine-P"]
test3Priests = ["Vöodûwôlf", "Vaevictís", "Dro<Antiquity>", "Epyca/Tarjah", "Syzzurp"]
test3Other = [":Late: Late (2) : :Hunter: 16 Babadook/Botanist, :Hunter: 33 qip,", ":Bench: Bench (1) : :Hunter: 54 VeeVee/Scryugemcduk,", ":Tentative: Tentative (2) : :Warrior: 43 Tohroo/Medaka, :Warlock: 55 Zelgadiss,", ":Absence: Absence (8) : 3 Hellohidead, 13 Quix, 15 kakau, 27 Clatrina/Wingsß, 32 Kaldastr, 40 tyrilae, 42 Decoilani, 45 pewpewboom,"]

def ReadFile(roles, file):
    rolesList = []
    Players = {}
    with open(roles) as f:
        rolesJson = json.load(f)
        for item in rolesJson:
            rolesList.append(item)

    with open(file, 'r', encoding='utf8') as f:
        data = f.readlines()
        other = []
        for line in data:
            if "Tentative" in line or "Absence" in line or "Late" in line or "Bench" in line:
                other.append(line.replace("\n", ""))
            else:

                for icon in rolesList:
                    name = rolesJson[icon]["name"]
                    wClass = rolesJson[icon]["class"]
                    classSum = icon + " " + name + " ("
                    
                    if classSum in line or len(line) < 1:
                        pass
                    else:
                        tempPlayer = str(line)
                        role = rolesJson[icon]["name"]
                        if icon in tempPlayer:
                            tempPlayer = tempPlayer.replace(icon, "")
                            tempPlayer = tempPlayer.replace(" ", "")
                            tempPlayer = tempPlayer.lstrip(digits)
                            tempPlayer = tempPlayer.replace('\t', '')\
                                .replace(u"\u00A0", '')
                            tempPlayer = tempPlayer.strip()
                            tempPlayer = unidecode.unidecode(tempPlayer)
                            player = tempPlayer
                            addPlayer = Signee(3, player, wClass, role)
                            
                            addPlayer.showInfo()
                            print("\n")
                            Players[player] = role

    tanks = []
    hunters = []
    druids = []
    warriors = []
    mages = []
    shamans = []
    rogues = []
    warlocks = []
    priests = []

    for p in Players:
        if Players[p] in ("Tank", "BearTank"):
            tanks.append(p)
        if Players[p] in ("Hunter"):
            hunters.append(p)
        if Players[p] in ("RestoDruid", "FeralDruid", "BalanceDruid"):
            druids.append(p)
        if Players[p] in ("Warrior"):
            warriors.append(p)
        if Players[p] in ("Mage"):
            mages.append(p)
        if Players[p] in ("EnhShaman", "RestoShaman", "ElemShaman"):
            shamans.append(p)
        if Players[p] in ("Rogue"):
            rogues.append(p)
        if Players[p] in ("Warlock"):
            warlocks.append(p)
        if Players[p] in ("Priest", "ShadowPriest"):
            priests.append(p)
    
    # if test2Tanks == tanks:
    #     print("tanks has passed!")
    #     print(tanks)
    # else:
    #     print("tanks has failed!")
    #     print(tanks)
    # if test2Hunters == hunters:
    #     print("hunters has passed!")
    #     print(hunters)
    # else:
    #     print("hunters has failed!")
    #     print(hunters)
    # if test2Druids == druids:
    #     print("druids has passed!")
    #     print(druids)
    # else:
    #     print("druids has failed!")
    #     print(druids)
    # if test2Warriors == warriors:
    #     print("warriors has passed!")
    #     print(warriors)
    # else:
    #     print("warriors has failed!")
    #     print(warriors)
    # if test2Mages == mages:
    #     print("mages has passed!")
    #     print(mages)
    # else:
    #     print("mages has failed!")
    #     print(mages)
    # if test2Shamans == shamans:
    #     print("shamans has passed!")
    #     print(shamans)
    # else:
    #     print("shamans has failed!")
    #     print(shamans)
    # if test2Rogues == rogues:
    #     print("rogues has passed!")
    #     print(rogues)
    # else:
    #     print("rogues has failed!")
    #     print(rogues)
    # if test2Warlocks == warlocks:
    #     print("warlocks has passed!")
    #     print(warlocks)
    # else:
    #     print("warlocks has failed!")
    #     print(warlocks)
    # if test2Priests == priests:
    #     print("priests has passed!")
    #     print(priests)
    # else:
    #     print("priests has failed!")
    #     print(priests)
    # if test2Other == other:
    #     print("other has passed!")
    #     print(other)
    # else:
    #     print("other has failed!")
    #     print(other)



    # if test3Tanks == tanks:
    #     print("tanks has passed!")
    #     print(tanks)
    # else:
    #     print("tanks has failed!")
    #     print(tanks)
    # if test3Hunters == hunters:
    #     print("hunters has passed!")
    #     print(hunters)
    # else:
    #     print("hunters has failed!")
    #     print(hunters)
    # if test3Druids == druids:
    #     print("druids has passed!")
    #     print(druids)
    # else:
    #     print("druids has failed!")
    #     print(druids)
    # if test3Warriors == warriors:
    #     print("warriors has passed!")
    #     print(warriors)
    # else:
    #     print("warriors has failed!")
    #     print(warriors)
    # if test3Mages == mages:
    #     print("mages has passed!")
    #     print(mages)
    # else:
    #     print("mages has failed!")
    #     print(mages)
    # if test3Shamans == shamans:
    #     print("shamans has passed!")
    #     print(shamans)
    # else:
    #     print("shamans has failed!")
    #     print(shamans)
    # if test3Rogues == rogues:
    #     print("rogues has passed!")
    #     print(rogues)
    # else:
    #     print("rogues has failed!")
    #     print(rogues)
    # if test3Warlocks == warlocks:
    #     print("warlocks has passed!")
    #     print(warlocks)
    # else:
    #     print("warlocks has failed!")
    #     print(warlocks)
    # if test3Priests == priests:
    #     print("priests has passed!")
    #     print(priests)
    # else:
    #     print("priests has failed!")
    #     print(priests)
    # if test3Other == other:
    #     print("other has passed!")
    #     print(other)
    # else:
    #     print("other has failed!")
    #     print(other)

ReadFile("testData/Roles.json", "testData/Naxx_2-19.txt")
