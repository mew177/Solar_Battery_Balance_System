class Utility:

    def __init__(self):
        self.UNIT_PRICING = [5.,5.,5.,5.,5.,5.,15.,15.,15.,15.,15.,15.,15.,15.,15.,15.,25.,25.,25.,25.,25.,25.,25.,25.]

    def pricing(self, time, rate):
        # time format: 2000/01/01 00:00
        # time period: 15 mins
        date, time = time.split(' ')
        hour, minitue = time.split(':')
        return rate * self.UNIT_PRICING[hour] / 4
