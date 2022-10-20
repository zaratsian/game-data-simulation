import json
import time, datetime
import random

class playerEvent:
    def __init__(self, username, userid):
        self.sessionId = f'{int(time.time())}{random.randint(10000,99999)}'
        self.userid = userid
        self.username = username
        self.points = 0
        self.itemPayload = {'itemID':'', 'itemName':""}
        self.itemPayloadPrice = 0
        self.itemPayloadName = ""
        self.minutesPlayed = 0
        self.gameType = ""
        self.friendCount = 0
        self.offensePercent = 0.0
        self.defensePercent = 0.0
        self.timeWithBall = 0.0
        self.soccerPosition = random.choice(['goalie']*5 + ['defender']*25 + ['midfielder']*25 + ['forward']*45)
        self.simPlayerType = random.choice(['competitive']*10 + ['weekender']*30 + ['afterschool']*40 + ['casual']*20)
        self.simEventsToChurnCount = 0
        
        if self.simPlayerType == 'competitive':
            self.datetimepy = datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600))
            self.simEventsToChurn = random.triangular(712,903,900)
            self.simPurchaseFreq = random.randint(4,6)/100
        elif self.simPlayerType == 'weekender':
            self.datetimepy = self.getNextWeekend(datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,14400)))
            self.simEventsToChurn = random.triangular(75,500,365)
            self.simPurchaseFreq = random.randint(8,12)/100
        elif self.simPlayerType == 'afterschool':
            self.datetimepy = self.getNextWeekday(datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600)))
            self.simEventsToChurn = random.triangular(10,200,30)
            self.simPurchaseFreq = random.randint(18,22)/100
        elif self.simPlayerType == 'casual':
            self.datetimepy = datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600))
            self.simEventsToChurn = random.triangular(30,500,180)
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
    
    def getItem(self):
        items = [{'itemID':1001, 'itemName': 'Yellow Jersey'}]*10 +\
            [{'itemID':1002, 'itemName': 'Green Jersey'}]*20 +\
            [{'itemID':1003, 'itemName': 'Blue Jersey'}]*20 +\
            [{'itemID':1100, 'itemName': 'Black Shorts'}]*15 +\
            [{'itemID':1101, 'itemName': 'White Shorts'}]*5 +\
            [{'itemID':1200, 'itemName': 'Black Cleats'}]*15 +\
            [{'itemID':1201, 'itemName': 'Yellow Cleats'}]*2 +\
            [{'itemID':1202, 'itemName': 'Green Cleats'}]*3 +\
            [{'itemID':1203, 'itemName': 'Blue Cleats'}]*5 +\
            [{'itemID':1300, 'itemName': 'Green Socks'}]*4 +\
            [{'itemID':1400, 'itemName': 'Hat'}]*3 +\
            [{'itemID':1500, 'itemName': 'Soccer Ball'}]*3
        return random.choice(items)
    
    def newEvent(self):
        self.sessionId = f'{int(time.time())}{random.randint(1000,9999)}'
        self.points = random.randint(1,100)
        self.friendCount = random.triangular(0,10,0)
        self.simEventsToChurnCount += 0
        
        if self.soccerPosition in ['goalie','defender']:
            self.defensePercent = random.triangular(1,100,80) / 100
            self.offensePercent = 1.0 - self.defensePercent
        else:
            self.offensePercent = random.triangular(1,100,80) / 100
            self.defensePercent = 1.0 - self.offensePercent
        
        if self.offensePercent > self.defensePercent:
            self.timeWithBall = random.triangular(1,100,60) / 100
        else:
            self.timeWithBall = random.triangular(1,100,35) / 100            
        
        if self.simPlayerType == 'competitive':
            self.datetimepy = self.datetimepy + datetime.timedelta(minutes=random.randint(1300,3000))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(120,480,180)
            self.itemPayloadPrice = random.randint(25,100) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPayloadPrice != 0 else {'itemID':'', 'itemName':""}
            self.gameType = random.choice(['tournament']*80 + ['skills game']*20)
        elif self.simPlayerType == 'weekender':
            self.datetimepy = self.getNextWeekend(self.datetimepy + datetime.timedelta(minutes=random.randint(1300,3000)))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(15,240,120)
            self.itemPayloadPrice = random.randint(0,50) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPayloadPrice != 0 else {'itemID':'', 'itemName':""}
            self.gameType = random.choice(['tournament']*5 + ['play for rewards']*55 + ['match with friends']*40)
        elif self.simPlayerType == 'afterschool':
            self.datetimepy = self.getNextWeekday(self.datetimepy + datetime.timedelta(minutes=random.triangular(1300,2800,1440)))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(5,180,30)
            self.itemPayloadPrice = random.randint(0,100) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPayloadPrice != 0 else {'itemID':'', 'itemName':""}
            self.gameType = random.choice(['match with friends']*75 + ['skills game']*10 + ['play for rewards']*10 + ['single match']*5)
        elif self.simPlayerType == 'casual':
            self.datetimepy = self.datetimepy + datetime.timedelta(minutes=random.triangular(1300,10080,2800))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.minutesPlayed = random.triangular(5,90,15)
            self.itemPayloadPrice = random.randint(0,10) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPayloadPrice != 0 else {'itemID':'', 'itemName':""}
            self.gameType = random.choice(['single match']*10 + ['play for rewards']*25 + ['skills game']*70)
    
    def getEventData(self):
        if (self.simEventsToChurnCount <= self.simEventsToChurnCount) and (self.datetimepy <= datetime.datetime.now()):
            payload = {
                'sessionId': self.sessionId,
                'userid': self.userid,
                'username': self.username,
                'datetime': self.datetime,
                'points': self.points,
                'itemID': self.itemPayload['itemID'],
                'itemName': self.itemPayload['itemName'],
                'itemPrice': self.itemPayloadPrice,
                'minutesPlayed': self.minutesPlayed,
                'gameType': self.gameType,
                'friendCount': self.friendCount,
                'offensePercentage': self.offensePercent,
                'defensePercentage': self.defensePercent,
                'timeWithBall': self.timeWithBall,
                'soccerPosition': self.soccerPosition,
            }
            return payload
        else:
            if (self.simEventsToChurnCount > self.simEventsToChurnCount):
                print(f'[ INFO ] Simulation complete for {self.username}. Player has churned on {self.datetime}')
            elif (self.datetimepy > datetime.datetime.now()):
                print(f'[ INFO ] Simulation complete for {self.username}. Datetime ({self.datetimepy}) is equal to today.')
            return None
