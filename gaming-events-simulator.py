
import time, datetime
import random

class playerEvent:
    def __init__(self, username):
        self.sessionId = f'{int(time.time())}{random.randint(10000,99999)}'
        self.username = username
        self.points = 0
        self.totalSpend = 0
        self.minutesPlayed = 0
        self.gameType = None
        self.friendCount = 0
        self.simPlayerType = random.choice(['competitive']*10 + ['weekender']*30 + ['afterschool']*40 + ['casual']*20)
        self.simEventsToChurnCount = 0
        
        if self.simPlayerType == 'competitive':
            self.datetimepy = datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600))
            self.simEventsToChurn = random.triangular(612,903,900)
            self.simPurchaseFreq = random.randint(4,6)/100
        elif self.simPlayerType == 'weekender':
            self.datetimepy = self.getNextWeekend(datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,14400)))
            self.simEventsToChurn = random.triangular(29,400,365)
            self.simPurchaseFreq = random.randint(8,12)/100
        elif self.simPlayerType == 'afterschool':
            self.datetimepy = self.getNextWeekday(datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600)))
            self.simEventsToChurn = random.triangular(1,101,30)
            self.simPurchaseFreq = random.randint(18,22)/100
        elif self.simPlayerType == 'casual':
            self.datetimepy = datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600))
            self.simEventsToChurn = random.triangular(1,367,180)
            self.simPurchaseFreq = random.randint(0,2)/100
        
        self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
        print(f'[ INFO ] User {self.username} initialized. simPlayerType: {self.simPlayerType}')
    
    def getNextWeekend(self, currentDatetime):
        nextDay = currentDatetime + datetime.timedelta(days=1)
        if nextDay.weekday() >= 5:
            return nextDay
        
        while nextDay.weekday() < 5:
            nextDay += datetime.timedelta(days=1)
        
        return nextDay
    
    def getNextWeekday(self, currentDatetime):
        nextDay = currentDatetime + datetime.timedelta(days=1)
        if nextDay.weekday() <= 4:
            return nextDay
        
        while nextDay.weekday() > 4:
            nextDay += datetime.timedelta(days=1)
        
        return nextDay
    
    def newEvent(self):
        self.sessionId = f'{int(time.time())}{random.randint(1000,9999)}'
        self.points = random.randint(1,100)
        self.friendCount += random.randint(1,10)
        self.simEventsToChurnCount += 0
        
        if self.simPlayerType == 'competitive':
            self.datetimepy = self.datetimepy + datetime.timedelta(minutes=random.randint(1300,3000))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(120,480,180)
            self.totalSpend = random.randint(25,100) if self.simPurchaseFreq >= random.random() else 0
            self.gameType = random.choice(['tournament']*80 + ['battle royale']*20)
        elif self.simPlayerType == 'weekender':
            self.datetimepy = self.getNextWeekend(self.datetimepy + datetime.timedelta(minutes=random.randint(1300,3000)))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(15,240,120)
            self.totalSpend = random.randint(0,50) if self.simPurchaseFreq >= random.random() else 0
            self.gameType = random.choice(['tournament']*5 + ['battle royale']*55 + ['creative']*40)
        elif self.simPlayerType == 'afterschool':
            self.datetimepy = self.getNextWeekday(self.datetimepy + datetime.timedelta(minutes=random.triangular(1300,2800,1440)))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(5,180,30)
            self.totalSpend = random.randint(0,100) if self.simPurchaseFreq >= random.random() else 0
            self.gameType = random.choice(['creative']*75 + ['battle royale']*15 + ['complete this stage']*10)
        elif self.simPlayerType == 'casual':
            self.datetimepy = self.datetimepy + datetime.timedelta(minutes=random.triangular(1300,10080,2800))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(5,90,15)
            self.totalSpend = random.randint(0,10) if self.simPurchaseFreq >= random.random() else 0
            self.gameType = random.choice(['complete this stage']*65 + ['creative']*25 + ['battle royale']*10)
    
    def getEventData(self):
        if (self.simEventsToChurnCount <= self.simEventsToChurnCount) and (self.datetimepy <= datetime.datetime.now()):
            payload = {
                'sessionId': self.sessionId,
                'username': self.username,
                'datetime': self.datetime,
                'points': self.points,
                'totalSpend': self.totalSpend,
                'minutesPlayed': self.minutesPlayed,
                'gameType': self.gameType,
                'friendCount': self.friendCount,
            }
            return payload
        else:
            if (self.simEventsToChurnCount > self.simEventsToChurnCount):
                print(f'[ INFO ] Simulation complete for {self.username}. Player has churned on {self.datetime}')
            elif (self.datetimepy > datetime.datetime.now()):
                print(f'[ INFO ] Simulation complete for {self.username}. Datetime ({self.datetimepy}) is equal to today.')
            return None
