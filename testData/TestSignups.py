from Signups import Signup


text = """:Tank: Tank (5):
:Tank: 3 torontocap
:Bear: 7 Kanzabear/Kanz
:Bear: 11 Olykos
:Tank: 42 Dartanko/Darho
:Tank: 43 Mink
‎
:Hunter: Hunter (7):
:Hunter: 1 ⇝𝕸𝖎𝖎𝖘𝖙𝖎
:Hunter: 22 Pickwick
:Hunter: 24 Wraithsexual
:Hunter: 26 Pinkee/Inthewa
:Hunter: 45 Mo(Tom/Alpha)
:Hunter: 59 melch
:Hunter: 60 skyehawk
‎
:Druid: Druid (2):
:RestoDruid: 19 Razor/Chibs
:RestoDruid: 20 Zuludelta
‎
:Warrior: Warrior (9):
:Warrior: 6 Gombos
:Warrior: 12 Warsoldier
:Warrior: 14 dpsmeharder/cr
:Warrior: 18 beefiboi
:Warrior: 27 Käbäl
:Warrior: 40 Rageup
:Warrior: 46 cwarrior
:Warrior: 50 Havvokk
:Warrior: 58 Dapqu
‎
:Mage: Mage (7):
:Mage: 5 Venable
:Mage: 8 Siyanti/Reneca
:Mage: 15 Kazrik
:Mage: 16 Roundeye
:Mage: 21 Durdle
:Mage: 36 Healthledger-A
:Mage: 48 Dangle/Ambr
‎
:Shaman: Shaman (8):
:RestoShaman: 4 Anck
:RestoShaman: 32 Cozymend
:RestoShaman: 33 Moontotemz
:RestoShaman: 38 Snookies
:RestoShaman: 49 Vaevictís
:RestoShaman: 51 Reshal
:RestoShaman: 56 Kahl
:Enhancer: 57 Gallos
‎
:Rogue: Rogue (2):
:Rogue: 2 Leithia
:Rogue: 13 Bettywight/Ath
‎
:Warlock: Warlock (5):
:Warlock: 25 Pharmz
:Warlock: 29 Bobjira
:Warlock: 31 Shadowboxx
:Warlock: 53 Metrocard
:Warlock: 55 Ferk
‎
:Priest: Priest (8):
:Priest: 9 Zawmb
:Priest: 10 Epyca/Tarjah
:Shadow: 17 Winderella/Jin
:Priest: 23 Treyen
:Priest: 30 Twit
:Priest: 35 Syzzurp
:Priest: 39 Kengy
:Priest: 47 Faustuss/Aerod
‎

:Tentative: Tentative (2) : :Hunter: 41 Flexor(a)/Dedd, :Priest: 44 Dro<Antiquity>, :Shadow: 17 Winderella/Jin, :RestoShaman: 56 Kahl, :Enhancer: 57 Gallos
:Absence: Absence (5) : 28 Karellia, 34 Sardand, 37 Alizzah, 52 Lichttraeger, 54 Rainseeker,"""

signupname = "Test1"
raid_date = "02/19/2021"
raid_time = "21:00"

newSignup = Signup(signupname, raid_date, raid_time, text)
newSignup._parse_signees()