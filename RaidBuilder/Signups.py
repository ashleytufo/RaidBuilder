class Signup:

    def __init__(self, signup_name, raid_dateTime):
        self.name = signup_name
        self.shortcode = self.name.lower().replace(" ", "_")
        self.dateTime = raid_dateTime
