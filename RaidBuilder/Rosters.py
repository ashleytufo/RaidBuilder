class Roster:

    def __init__(self, raid, tanks=[], healers=[], melee=[], ranged=[],
                 standby1=[], standby2=[]):
        self.raid = raid
        self.tanks = tanks
        self.healers = healers
        self.melee = melee
        self.ranged = ranged
        self.standby1 = standby1
        self.standby2 = standby2