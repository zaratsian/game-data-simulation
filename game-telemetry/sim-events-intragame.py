'''
Simulation Objectives/Outcomes:
- 4 player types/clusters should emerge based on "simPlayerType" (tournament player, casual, after-school, and weekender)
- Churn can be predicted based on "disengagement" lead time (which can range from a few days to a few weeks)
- Some players are more likely to buy and/or more likely to pay for high dollar items.

USAGE:
# Save as local JSON file
sim-events-intragame.py --dataLocation local --localFilename simulatedData.json

# Save to Google Cloud Storage
sim-events-intragame.py --dataLocation cloudstorage --gcpProjectId lunar-data-364510 --gcp_bucket_name udp-lunar-data-364510-datasets --gcp_object_name simulatedDataGCS.json

# Stream data into Google BigQuery
sim-events-intragame.py --dataLocation bigquerystream --gcpProjectId lunar-data-364510 --bigquery_dataset udp --bigquery_tablename testTable

# Real-time stream into PubSub
sim-events-intragame.py --dataLocation pubsub --gcpProjectId lunar-data-364510 --pubsub_topic gameTelemetryTopic
'''

import sys
import json
import time, datetime
import random
import argparse
import simConfig
import gcpHelpers
from google.cloud import pubsub_v1

class playerEvent:
    def __init__(self, username, userid):
        self.eventId = f'{int(time.time())}{random.randint(10000,99999)}'
        self.userid = userid
        self.username = username
        self.points = 0
        self.itemPayload = {'itemID':'', 'itemName':""}
        self.itemPrice = 0
        self.itemPayloadName = ""
        self.visitsToStore = 0
        self.minutesPlayed = 0
        self.gameType = ""
        self.newFriends = 0
        self.offensePercent = 0.0
        self.defensePercent = 0.0
        self.timeWithBall = 0.0
        self.scoredGoal = False
        self.scoredOn = False
        self.fieldPosition_DefendingLeftSidePct  = 0.0
        self.fieldPosition_DefendingRightSidePct = 0.0
        self.fieldPosition_AttackingLeftSidePct  = 0.0
        self.fieldPosition_AttackingRightSidePct = 0.0
        self.soccerPosition = random.choice(['goalie']*5 + ['defender']*25 + ['midfielder']*25 + ['forward']*45)
        self.simPlayerType = random.choice(['competitive']*10 + ['weekender']*30 + ['afterschool']*40 + ['casual']*20)
        self.platform = random.choice(['pc']*20 + ['mobile']*20 + ['nintendo switch']*20 + ['ps4']*5 + ['xbox']*20)
        self.simEventsToChurnCount = 0
        
        if self.simPlayerType == 'competitive':
            '''
                Churn:                      Very low probability
                Gametype Preference:        Tournaments
                Play Frequency:             Daily
                Play Duration (avg):        3 hours
                Purchase Freq:              25% of the time
                Purchase Price Sensitivity: Not price sensitive, isn't afraid to make high dollar purchases.
                Points/Rewards:             This player persona receives a random range of points through skill and tournament play.
                Visits to Store:            Doesn't visit store often, this player knows what they need and only goes there when something is needed.
            '''
            self.datetimepy = datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600))
            self.simEventsToChurn = random.triangular(712,903,900)
            self.simChurnDate = self.datetimepy + datetime.timedelta(days=random.triangular(712,903,900))
            self.simPurchaseFreq = random.randint(23,27)/100
        elif self.simPlayerType == 'weekender':
            '''
                Churn:                      Typically churns after a year.
                Gametype Preference:        Games focused on (1) rewards and (2) social games with friends.
                Play Frequency:             Plays on weekends (saturday and sunday)
                Play Duration (avg):        2 hours
                Purchase Freq:              40% of the time
                Purchase Price Sensitivity: Moderately price conscience and doesn't typically purchase high dollar items.
                Points/Rewards:             This player is very focused on points and earning rewards.
                Visits to Store:            Visits the store somewhat often and frequently buys.
            '''
            self.datetimepy = self.getNextWeekend(datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,14400)))
            self.simEventsToChurn = random.triangular(75,500,365)
            self.simChurnDate = self.datetimepy + datetime.timedelta(days=random.triangular(75,500,365))
            self.simPurchaseFreq = random.randint(35,42)/100
        elif self.simPlayerType == 'afterschool':
            '''
                Churn:                      Typically churns after a month or two.
                Gametype Preference:        Games focused on social games with friends.
                Play Frequency:             Mostly plays during the weekdays
                Play Duration (avg):        30 minutes
                Purchase Freq:              65% of the time
                Purchase Price Sensitivity: Purchases whatever, both large and small priced items.
                Points/Rewards:             This player likes earning rewards but is not their main focus.
                Visits to Store:            Visits the store often. Loves to buy things.
            '''
            self.datetimepy = self.getNextWeekday(datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600)))
            self.simEventsToChurn = random.triangular(10,200,30)
            self.simChurnDate = self.datetimepy + datetime.timedelta(days=random.triangular(10,200,30))
            self.simPurchaseFreq = random.randint(45,65)/100
        elif self.simPlayerType == 'casual':
            '''
                Churn:                      Typically churns after 6 months.
                Gametype Preference:        Mostly skill games and a little bit of reward focused games.
                Play Frequency:             Plays daily
                Play Duration (avg):        15 minutes
                Purchase Freq:              15% of the time
                Purchase Price Sensitivity: Very price conscience and doesn't typically purchase high dollar items.
                Points/Rewards:             This player is somewhat focused on points and earning rewards.
                Visits to Store:            Not interested in visiting the store, but sometimes pops in to buy things.
            '''
            self.datetimepy = datetime.datetime.strptime('2020-01-01','%Y-%m-%d') + datetime.timedelta(minutes=random.randint(1,21600))
            self.simEventsToChurn = random.triangular(30,500,180)
            self.simChurnDate = self.datetimepy + datetime.timedelta(days=random.triangular(30,500,180))
            self.simPurchaseFreq = random.randint(12,17)/100
        
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
        self.eventId = f'{int(time.time())}{random.randint(1000,9999)}'
        #self.points = random.randint(1,100)
        self.newFriends = int(random.gammavariate(1,1))
        self.simEventsToChurnCount += 0
        self.soccerPosition = random.choice(['goalie']*5 + ['defender']*25 + ['midfielder']*25 + ['forward']*45)
        
        if self.soccerPosition in ['goalie','defender']:
            self.defensePercent = random.triangular(1,99,80) / 100
            self.offensePercent = 1.0 - self.defensePercent
            self.scoredGoal = random.choice([False]*98 + [True]*2)
            self.scoredOn   = random.choice([False]*80 + [True]*20)
        else:
            self.offensePercent = random.triangular(1,99,80) / 100
            self.defensePercent = 1.0 - self.offensePercent
            self.scoredGoal = random.choice([False]*75 + [True]*25)
            self.scoredOn   = random.choice([False]*95 + [True]*5)
        
        self.fieldPosition_DefendingLeftSidePct  = self.defensePercent * random.random()
        self.fieldPosition_DefendingRightSidePct = (1-(self.fieldPosition_DefendingLeftSidePct / self.defensePercent)) * self.defensePercent
        self.fieldPosition_AttackingLeftSidePct  = self.offensePercent * random.random()
        self.fieldPosition_AttackingRightSidePct = (1-(self.fieldPosition_AttackingLeftSidePct / self.offensePercent)) * self.offensePercent
        
        if self.offensePercent > self.defensePercent:
            self.timeWithBall = random.triangular(1,99,85) / 100
        else:
            self.timeWithBall = random.triangular(1,99,35) / 100            
        
        if self.simPlayerType == 'competitive':
            self.datetimepy = self.datetimepy + datetime.timedelta(hours=random.randint(1,3))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = random.randint(1,100)
            self.minutesPlayed = random.triangular(120,480,180)
            self.itemPrice = random.randint(25,100) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPrice != 0 else {'itemID':'', 'itemName':""}
            self.visitsToStore = int(random.choice([0]*85 + [1]*12 + [2]*3)) if self.itemPrice == 0 else random.randint(1,3)
            self.gameType = random.choice(['tournament']*80 + ['skills game']*20)
            self.platform = random.choice(['pc']*90 + ['mobile']*0 + ['nintendo switch']*0 + ['ps4']*5 + ['xbox']*5)
        elif self.simPlayerType == 'weekender':
            self.datetimepy = self.getNextWeekend( self.datetimepy + datetime.timedelta(hours=random.randint(1,8)) )
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = int(random.triangular(1,100,75))
            self.minutesPlayed = random.triangular(15,240,120)
            self.itemPrice = random.randint(0,50) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPrice != 0 else {'itemID':'', 'itemName':""}
            self.visitsToStore = int(random.gammavariate(2,1)) if self.itemPrice == 0 else random.randint(1,4)
            self.gameType = random.choice(['tournament']*5 + ['play for rewards']*55 + ['match with friends']*40)
            self.platform = random.choice(['pc']*5 + ['mobile']*0 + ['nintendo switch']*0 + ['ps4']*40 + ['xbox']*55)
        elif self.simPlayerType == 'afterschool':
            self.datetimepy = self.getNextWeekday( self.datetimepy + datetime.timedelta(hours=random.randint(1,24)) )
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = int(random.triangular(1,65,5))
            self.minutesPlayed = random.triangular(5,180,30)
            self.itemPrice = random.randint(0,100) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPrice != 0 else {'itemID':'', 'itemName':""}
            self.visitsToStore = int(random.gammavariate(3,1)) if self.itemPrice == 0 else random.randint(1,5)
            self.gameType = random.choice(['match with friends']*75 + ['skills game']*10 + ['play for rewards']*10 + ['single match']*5)
            self.platform = random.choice(['pc']*5 + ['mobile']*5 + ['nintendo switch']*15 + ['ps4']*45 + ['xbox']*30)
        elif self.simPlayerType == 'casual':
            self.datetimepy = self.datetimepy + datetime.timedelta(hours=random.randint(1,72))
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = int(random.triangular(1,82,40))
            self.minutesPlayed = random.triangular(5,90,15)
            self.itemPrice = random.randint(0,10) if self.simPurchaseFreq >= random.random() else 0
            self.itemPayload = self.getItem() if self.itemPrice != 0 else {'itemID':'', 'itemName':""}
            self.visitsToStore = int(random.gammavariate(1,1)) if self.itemPrice == 0 else random.randint(1,3)
            self.gameType = random.choice(['single match']*10 + ['play for rewards']*25 + ['skills game']*70)
            self.platform = random.choice(['pc']*0 + ['mobile']*80 + ['nintendo switch']*10 + ['ps4']*5 + ['xbox']*5)
    
    def getEventData(self):
        if (self.simEventsToChurnCount <= self.simEventsToChurnCount) and (self.datetimepy <= datetime.datetime.now()):
            payload = {
                'eventId': self.eventId,
                'userid': self.userid,
                'username': self.username,
                'datetime': self.datetime,
                'points': self.points,
                'itemID': self.itemPayload['itemID'],
                'itemName': self.itemPayload['itemName'],
                'itemPrice': self.itemPrice,
                'visitsToStore': self.visitsToStore,
                'minutesPlayed': self.minutesPlayed,
                'gameType': self.gameType,
                'newFriends': self.newFriends,
                'offensePercentage': self.offensePercent,
                'defensePercentage': self.defensePercent,
                'timeWithBall': self.timeWithBall,
                'scoredGoal': self.scoredGoal,
                'scoredOn': self.scoredOn,
                'fieldPosition_DefendingLeftSidePct': self.fieldPosition_DefendingLeftSidePct,
                'fieldPosition_DefendingRightSidePct': self.fieldPosition_DefendingRightSidePct,
                'fieldPosition_AttackingLeftSidePct': self.fieldPosition_AttackingLeftSidePct,
                'fieldPosition_AttackingRightSidePct': self.fieldPosition_AttackingRightSidePct,
                #'soccerPosition': self.soccerPosition,
                'platform': self.platform,
            }
            return payload
        else:
            if (self.datetimepy >= self.simChurnDate):
                print(f'[ INFO ] Simulation complete for {self.username}. Player has churned on {self.datetime}, churn date of {self.simChurnDate}')
            elif (self.datetimepy > datetime.datetime.now()):
                print(f'[ INFO ] Simulation complete for {self.username}. Datetime ({self.datetimepy}) is equal to today.')
            return None


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataLocation',       type=str, required=True,  help='Where should the simulated data be saved: local, cloudstorage, bigquerybatch, bigquerystream, or spanner)')
    parser.add_argument('--gcpProjectId',       type=str, required=False, help='Google Cloud Project ID')
    parser.add_argument('--localFilename',      type=str, required=False, help='Name of local file, if dataLocation == "local"')
    parser.add_argument('--gcp_bucket_name',    type=str, required=False, help='Name of GCS bucket, if dataLocation == "cloudstorage"')
    parser.add_argument('--gcp_object_name',    type=str, required=False, help='Name of GCS object name, if dataLocation == "cloudstorage"')
    parser.add_argument('--bigquery_dataset',   type=str, required=False, help='Name of Bigquery Dataset, if dataLocation == "bigquery"')
    parser.add_argument('--bigquery_tablename', type=str, required=False, help='Name of Bigquery Table, if dataLocation == "bigquery"')
    parser.add_argument('--pubsub_topic',       type=str, required=False, help='PubSub Topic name, if dataLocation == "pubsub"')
    
    args = parser.parse_args()
    
    if args.dataLocation not in ['local', 'cloudstorage', 'bigquerystream', 'pubsub']:
        print(f'[ ERROR ] dataLocation argument is not valid. Options include local, cloudstorage, bigquerystream, pubsub')
        sys.exit()
    
    if args.dataLocation == 'pubsub':
        pubsub_publisher = pubsub_v1.PublisherClient()
        
        simulatedPlayerObj = {}
        
        while True:
            time.sleep(0.01)
            
            # Get random player and simulate data record
            player = random.choice(simConfig.playerNames)
            
            if player['username'] not in simulatedPlayerObj:
                simulatedPlayerObj[player['username']] = playerEvent(player['username'], player['userid'])
                playerPayload = simulatedPlayerObj[player['username']].getEventData()
            else:
                simulatedPlayerObj[player['username']].newEvent()
                playerPayload = simulatedPlayerObj[player['username']].getEventData()
                if playerPayload:
                    gcpHelpers.streamToPubSub(project_id=args.gcpProjectId, pubsub_publisher=pubsub_publisher, pubsub_topic=args.pubsub_topic, json_paylod=playerPayload)
                    print(f"[ INFO ] Simulated user: {player['username']}, playload: playerPayload: {playerPayload}")
    
    else:
        simulatedPlayerObj = {}
        output = []
        
        for player in simConfig.playerNames:
            print()
            playerPayload = {}
            if player['username'] not in simulatedPlayerObj:
                simulatedPlayerObj[player['username']] = playerEvent(player['username'], player['userid'])
                playerPayload = simulatedPlayerObj[player['username']].getEventData()
            
            counter = 0
            while playerPayload != None:
                counter += 1
                simulatedPlayerObj[player['username']].newEvent()
                playerPayload = simulatedPlayerObj[player['username']].getEventData()
                if playerPayload:
                    output.append(playerPayload)
        
        print(f'[ INFO ] Total Records: {len(output)}')
        newOutput = sorted(output, key=lambda d: d['datetime'])
        
        newLineDelmitedJSON = ''
        for line in newOutput:
            newLineDelmitedJSON += f'{json.dumps(line)}\n'
        
        if args.dataLocation == 'cloudstorage':
            gcpHelpers.saveObjectToCloudStorage(bucket_name=args.gcp_bucket_name, blob_name=args.gcp_object_name, data=newLineDelmitedJSON)
        
        elif args.dataLocation == 'bigquerystream':
            '''
            Use BQ Streaing API to load records directly in to BQ
            '''
            # Create Table
            gcpHelpers.createBQTable(gcpProjectID=args.gcpProjectId, bqDataset=args.bigquery_dataset, bqTable=args.bigquery_tablename, schema=simConfig.bqSchemaIntragame)
            
            # Stream batches of 500 records into BQ
            bqRecords = []
            for i, record in enumerate(newOutput):
                if i % 499 == 0:
                    bqRecords.append(record)
                    gcpHelpers.saveToBigQuery(gcpProjectID=args.gcpProjectId, bqDataset=args.bigquery_dataset, bqTable=args.bigquery_tablename, rows_to_insert=bqRecords)
                    bqRecords = []
                else:
                    bqRecords.append(record)
            
            # Send final bqRecord payload
            gcpHelpers.saveToBigQuery(gcpProjectID=args.gcpProjectId, bqDataset=args.bigquery_dataset, bqTable=args.bigquery_tablename, rows_to_insert=bqRecords)
        
        elif args.dataLocation == 'local':
            gcpHelpers.saveToLocal(outputFilename=args.localFilename, dataContent=newLineDelmitedJSON)
