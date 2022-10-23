'''
Simulation Objectives/Outcomes:
- Themes should emerge for "simPlayerType" in any analysis / ML
- Churn can be predicted based on "disengagement" lead time
- Some players are more likely to buy and/or more likely to pay for high dollar items.
'''

import json
import time, datetime
import random

class playerEvent:
    def __init__(self, username, userid):
        self.eventId = f'{int(time.time())}{random.randint(10000,99999)}'
        self.numberSessions = 0
        self.userid = userid
        self.username = username
        self.points = 0
        self.totalTransactionAmount = 0.0
        self.itemsPurchased = 0
        self.visitsToStore = 0
        self.minutesPlayed = 0
        self.gameType = ""
        self.newFriends = 0
        self.offensePercent = 0.0
        self.defensePercent = 0.0
        self.timeWithBall = 0.0
        self.soccerPosition = random.choice(['goalie']*5 + ['defender']*25 + ['midfielder']*25 + ['forward']*45)
        self.platform = random.choice(['pc']*20 + ['mobile']*20 + ['nintendo switch']*20 + ['ps4']*5 + ['xbox']*20)
        self.simPlayerType = random.choice(['competitive']*10 + ['weekender']*30 + ['afterschool']*40 + ['casual']*20)
        self.simEventsToChurnCount = 0
        self.simPlayerDisengaged = False
        self.simPlayerDisengagedLeadTime = 0
        
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
            self.simPlayerDisengagedLeadTime = random.randint(1,3)
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
            self.simPlayerDisengagedLeadTime = random.randint(30,40)
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
            self.simPlayerDisengagedLeadTime = random.randint(14,21)
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
            self.simPlayerDisengagedLeadTime = random.randint(5,60)
            self.simPurchaseFreq = random.randint(12,17)/100
        
        self.simEventsUntilDisengaged = self.simEventsToChurn - self.simPlayerDisengagedLeadTime
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
        self.simEventsUntilDisengaged -= 1
        self.soccerPosition = random.choice(['goalie']*5 + ['defender']*25 + ['midfielder']*25 + ['forward']*45)
        
        if self.soccerPosition in ['goalie','defender']:
            self.defensePercent = random.triangular(1,99,80) / 100
            self.offensePercent = 1.0 - self.defensePercent
        else:
            self.offensePercent = random.triangular(1,99,80) / 100
            self.defensePercent = 1.0 - self.offensePercent
        
        if self.offensePercent > self.defensePercent:
            self.timeWithBall = random.triangular(1,99,85) / 100
        else:
            self.timeWithBall = random.triangular(1,99,35) / 100            
        
        if self.simPlayerType == 'competitive':
            self.numberSessions = int(random.triangular(1,15,6))
            self.datetimepy = self.datetimepy + datetime.timedelta(days= int(random.choice([1]*9 + [2]*1)) )
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = random.randint(1,100)
            self.minutesPlayed = random.triangular(120,480,180)
            self.totalTransactionAmount = random.randint(25,100) if self.simPurchaseFreq >= random.random() else 0
            self.itemsPurchased = int(random.choice([1]*85 + [2]*12 + [3]*3 + [4]*0 + [5]*0 + [6]*0 + [7]*0)) if self.totalTransactionAmount != 0 else 0
            self.visitsToStore = int(random.choice([0]*85 + [1]*12 + [2]*3)) if self.itemsPurchased == 0 else random.randint(1,3)
            self.gameType = random.choice(['tournament']*80 + ['skills game']*20)
            self.platform = random.choice(['pc']*90 + ['mobile']*0 + ['nintendo switch']*0 + ['ps4']*5 + ['xbox']*5)
        elif self.simPlayerType == 'weekender':
            self.numberSessions = int(random.triangular(1,10,5))
            self.datetimepy = self.getNextWeekend( self.datetimepy + datetime.timedelta(days= int(random.choice([1]*10 + [2]*0)) ) )
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = int(random.triangular(1,100,75))
            self.minutesPlayed = random.triangular(15,240,120)
            self.totalTransactionAmount = random.randint(0,50) if self.simPurchaseFreq >= random.random() else 0
            self.itemsPurchased = int(random.choice([1]*65 + [2]*20 + [3]*5 + [4]*5 + [5]*3 + [6]*2 + [7]*0)) if self.totalTransactionAmount != 0 else 0
            self.visitsToStore = int(random.gammavariate(2,1)) if self.itemsPurchased == 0 else random.randint(1,4)
            self.gameType = random.choice(['tournament']*5 + ['play for rewards']*55 + ['match with friends']*40)
            self.platform = random.choice(['pc']*5 + ['mobile']*0 + ['nintendo switch']*0 + ['ps4']*40 + ['xbox']*55)
        elif self.simPlayerType == 'afterschool':
            self.numberSessions = int(random.triangular(1,10,3))
            self.datetimepy = self.getNextWeekday( self.datetimepy + datetime.timedelta(days= int(random.choice([1]*9 + [2]*1)) ) )
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = int(random.triangular(1,65,5))
            self.minutesPlayed = random.triangular(5,180,30)
            self.totalTransactionAmount = random.randint(0,100) if self.simPurchaseFreq >= random.random() else 0
            self.itemsPurchased = int(random.choice([1]*58 + [2]*20 + [3]*10 + [4]*5 + [5]*3 + [6]*2 + [7]*2)) if self.totalTransactionAmount != 0 else 0
            self.visitsToStore = int(random.gammavariate(3,1)) if self.itemsPurchased == 0 else random.randint(1,5)
            self.gameType = random.choice(['match with friends']*75 + ['skills game']*10 + ['play for rewards']*10 + ['single match']*5)
            self.platform = random.choice(['pc']*5 + ['mobile']*5 + ['nintendo switch']*15 + ['ps4']*45 + ['xbox']*30)
        elif self.simPlayerType == 'casual':
            self.numberSessions = int(random.triangular(1,8,1))
            self.datetimepy = self.datetimepy + datetime.timedelta(days= int(random.choice([1]*55 + [2]*25 + [3]*10 + [4]*7 + [5]*2)) )
            self.datetime = self.datetimepy.strftime('%Y-%m-%d %H:%M:%S')
            self.points = int(random.triangular(1,82,40))
            self.minutesPlayed = random.triangular(5,90,15)
            self.totalTransactionAmount = random.randint(0,10) if self.simPurchaseFreq >= random.random() else 0
            self.itemsPurchased = int(random.choice([1]*90 + [2]*8 + [3]*2 + [4]*0 + [5]*0 + [6]*0 + [7]*0)) if self.totalTransactionAmount != 0 else 0
            self.visitsToStore = int(random.gammavariate(1,1)) if self.itemsPurchased == 0 else random.randint(1,3)
            self.gameType = random.choice(['single match']*10 + ['play for rewards']*25 + ['skills game']*70)
            self.platform = random.choice(['pc']*0 + ['mobile']*80 + ['nintendo switch']*10 + ['ps4']*5 + ['xbox']*5)
        
        if self.simEventsUntilDisengaged <= 0:
            self.points = random.randint(1,20)
            self.minutesPlayed = random.randint(5,30)
            self.totalTransactionAmount = 0
            self.itemsPurchased = 0
    
    def getEventData(self):
        if (self.simEventsToChurnCount <= self.simEventsToChurnCount) and (self.datetimepy <= datetime.datetime.now()):
            payload = {
                'eventId': self.eventId,
                'userid': self.userid,
                'username': self.username,
                'datetime': self.datetime,
                'numberSessions': self.numberSessions,
                'points': self.points,
                'totalTransactionAmount': self.totalTransactionAmount,
                'itemsPurchased': self.itemsPurchased,
                'visitsToStore': self.visitsToStore,
                'minutesPlayed': self.minutesPlayed,
                'gameType': self.gameType,
                'newFriends': self.newFriends,
                'offensePercentage': self.offensePercent,
                'defensePercentage': self.defensePercent,
                'timeWithBall': self.timeWithBall,
                #'soccerPosition': self.soccerPosition,
                'platform': self.platform,
            }
            return payload
        else:
            if (self.simEventsToChurnCount > self.simEventsToChurnCount):
                print(f'[ INFO ] Simulation complete for {self.username}. Player has churned on {self.datetime}')
            elif (self.datetimepy > datetime.datetime.now()):
                print(f'[ INFO ] Simulation complete for {self.username}. Datetime ({self.datetimepy}) is equal to today.')
            return None


def saveFileToCloudStorage(bucket_name, blob_name, source_file_name):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file_name)
    print(f'[ INFO ] {source_file_name} uploaded to {bucket_name} as {blob_name}')


def saveObjectToCloudStorage(bucket_name, blob_name, data):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data)
    print(f'[ INFO ] In memory data uploaded to {bucket_name} as {blob_name}')


def saveToBigQuery(gcpProjectID, bqDataset, bqTable, rows_to_insert):
    '''
        BigQuery Streaming Insert
        NOTE: Streaming insert cost extra.

        rows_to_insert = [
            {"full_name": "Phred Phlyntstone", "age": 32},
            {"full_name": "Wylma Phlyntstone", "age": 29},
        ]
    '''
    from google.cloud import bigquery
    bigquery_client = bigquery.Client()
    table_id = f'{gcpProjectID}.{bqDataset}.{bqTable}'
    errors = bigquery_client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print(f'New rows have been added.')
    else:
        print(f'[ WARNING ] Encountered errors while inserting rows: {errors}')


def saveToSpanner(instance_id, database_id, table_id, schema, recordList):
    '''
        Examples:
        schema: (SingerId, FirstName, LastName)
        recordList: 
    '''
    from google.cloud import spanner
    
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    
    def insert_singers(transaction):
        row_ct = transaction.execute_update(
            "INSERT Singers (SingerId, FirstName, LastName) VALUES "
            "(12, 'Melissa', 'Garcia'), "
            "(13, 'Russell', 'Morales'), "
            "(14, 'Jacqueline', 'Long'), "
            "(15, 'Dylan', 'Shaw')"
        )
        print("{} record(s) inserted.".format(row_ct))
    
    database.run_in_transaction(insert_singers)
    return None


if __name__ == "__main__":
    
    bucket_name = 'udp-data-assets'
    filename    = 'gameEventsDaily_v2.json'
    bqTableName = 'gameEventsDaily_v2'
    
    playerNamesList = '''020e1d45-85ec-4d51-ab84-e22de8ef6c42|Grace|Nash|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    0242fd56-47bd-49c0-ad96-73538360238e|Harper|Ayers|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    060aaf03-3fe8-4c9e-8a81-99b5e6d533d9|Riley|Shea|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    063b46e1-265f-4800-8cc6-a45c675bd202|Madelyn|Rocha|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    066122d5-6e02-40a7-a0a4-18d84bf5a194|Nora|Davis|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    074c0227-4340-4871-b2c1-b496aaed1a42|Gabriella|Marsh|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    0921ab1c-641d-44f9-bef0-b1c12d121970|Aaliyah|Bernard|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    0de6e2ae-a50c-4234-b811-f398b6bab5a2|Evelyn|Yang|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    0e9be25e-56a3-4bc8-a6ae-11d17f8f026e|Arianna|Whitehead|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    11dac5d6-3628-488a-a74c-807d3f8f231b|Elizabeth|Sanchez|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    12f357d0-90f1-43c0-bab4-8de19acf20c2|Natalie|Ayers|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    14cb15f0-dd0c-426b-9321-1dcffc6671a9|Peyton|Mckee|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    1bf72e53-349b-4dca-b2ec-6b7c2888db2e|Peyton|Whitehead|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    2186e846-2964-4728-9a29-c4c186d8d878|Peyton|Travis|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    2408d0ec-ca2a-4f85-8877-15c18ed2e85f|Skylar|Bautista|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    2715294d-1eb1-45b4-8a5d-8f0aff8bcf8f|Natalie|Nunez|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    27c9c7eb-b792-48b7-90e7-8cd8bccef47d|Samantha|Bean|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    29716d16-9cca-4100-9cef-07345060c397|Layla|Patton|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    2996bb04-8f75-4038-a710-eb4e43803baf|Nora|Kirk|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    2b712c49-87c4-4d45-b3a7-1ee47b86dcd1|Leah|Gordon|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    3148530c-16bb-4ea4-b16a-a77cc83a758b|Zoey|Reese|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    33589078-53e4-4e47-8604-5ec20f85f7af|Claire|Bernard|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    34780070-f4ee-4919-86ee-0b5d1c9f11ca|Lucy|Beard|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    36536553-fe39-4f59-89e7-17db8b4d501f|Evelyn|Shepard|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    3aa0005b-52fe-4dd4-8046-566250037e27|Kaylee|Gordon|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    3c91d436-1641-44f2-9be5-04ab4324d071|Natalie|Bernard|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    3cc34729-0a44-460e-9d8f-95b8171c2fd2|Hannah|Nunez|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    3e8e6ba9-e683-49cf-8494-61c76558be13|Nora|Nash|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    41046327-c026-49ff-9b5a-cd1b99d80ce0|Stella|Bean|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    43482d36-d984-4073-8574-43bfa7e947e3|Sofia|Odom|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    466789f8-d5ad-424d-b915-3d7650dd5385|Sofia|Rocha|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    483f277c-3750-4dfc-9970-41af6740799b|Chloe|Reese|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    4a4c7d23-824a-41a2-9afd-899adb73d3a0|Paisley|Bridges|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    4c385ca7-a2c0-40fe-86ae-21ac4edea7dc|Elizabeth|Rocha|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    4df7541d-774e-43db-860c-7fd1dbbd434c|Abigail|Guerrero|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    557914d8-6e9b-4eae-a5fe-6807ebb958d2|Charlotte|Webb|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    55f5bec8-e661-4a3e-8ad4-e82707e7b5ec|Abigail|Hill|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    5862eea3-698b-4c9e-a064-8419d4129c40|Victoria|Webb|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    5a448572-d9ce-434e-ad4b-6eac0444a6c8|Lily|English|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    5df0a3e8-aae6-48e4-95c8-821f026dc964|Leah|Powell|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    5e089345-c89f-4d24-9d4c-3e7fd1396390|Zoe|Nunez|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    5f6c39e6-1963-4a92-a995-cf135396fd4c|Paisley|Mcknight|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    62a04a3a-ffd9-49e0-8f77-5a514a2d5fac|Aaliyah|Cook|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    665d6073-109d-4743-989a-9f96d34b77c2|Zoe|Bean|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    6af4c233-9ec6-4435-8331-763ec44d4f67|Nora|Yang|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    72a5599b-970c-4455-9d0c-53214dc5dff7|Annabelle|Nunez|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    78b456e6-6cc2-4faa-a561-7fd125f2ac8a|Zoe|Cook|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    78d7d390-0dff-4279-9ef0-a3990575410e|Aubrey|Yang|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    7af2c9f6-38b3-4309-a583-2d401a1b2d27|Arianna|Marsh|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    7b8c8bf9-9526-48eb-972e-8de011a139d0|Stella|Powell|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    7be6d007-368e-4642-9af9-822d419f5da9|Chloe|Guerrero|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    7c6e5253-25a7-4ce9-a556-2b3f8d3e13dd|Amelia|Marsh|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    7c73e167-5b81-4e64-b942-5c4d185cc90b|Nevaeh|Cook|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    7f21f04e-f7b6-45f2-8841-830672334434|Madelyn|Goodwin|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    7f8ee50a-11b1-43ae-86e6-ef72a69f2c59|Mia|Whitehead|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    826a6830-ba71-4765-9e2d-a95cd96bd38e|Gabriella|Gordon|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    8f311e9c-11b0-4c54-b51a-52d5e6216089|Alexis|Goodwin|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    92399412-95df-480e-979e-691e93b3097d|Madelyn|Shea|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    958108a6-0ad4-4e68-841d-82141e2e5380|Camila|Nash|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    96fcdc67-93e9-44cf-84b8-9318ec81792c|Peyton|Yang|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    99e3ad3d-a2a8-4917-8913-ec508ba1ffaf|Madelyn|Fry|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    9af8b796-5912-4152-bd4b-194f1ad3d428|Gabriella|Beard|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    9c33abe2-54d1-41cc-911f-11c59f351a82|Elizabeth|Bonilla|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    9d150157-fbc2-4b56-a568-4d3bdd1bc9a7|Emma|Gay|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    9d8bc771-84ee-4158-8efa-1ce9093cfbfe|Annabelle|Powell|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    a227850c-afc3-43cd-9b34-4b84dbd22552|Camila|Mcknight|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    a2f305e4-3372-431d-976c-f0be4aaad132|Caroline|Gentry|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    a311c020-7484-4cf3-a83e-9c5e5e86609c|Camila|Davis|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    a7de03a7-2f5e-455b-9b29-3db0241c090f|Avery|Hill|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    a9eb6b4c-6330-4f15-893c-ff648b9d67f1|Zoe|Gordon|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    ae2450f7-6ecb-4466-b0a5-9e73ab852473|Olivia|Bridges|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    b0d217d9-3744-4bac-a716-e33f4e0648a3|Zoey|Mcknight|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    b2a3f2e6-4342-47e0-ba6d-234c15684d74|Audrey|Hill|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    b7c7160e-9f67-4bc3-910a-f8e389d9e448|Arianna|Merritt|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    b8c51de4-965c-4922-8018-a9a320eaf941|Nevaeh|Robertson|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c1539142-bb87-43f3-a779-8997a502223f|Harper|Mcknight|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c3ef1e92-aa30-47db-bb33-e1d7e01a1fc1|Audrey|Bernard|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c410d6c9-0929-41f5-a00d-2fc83e64890c|Annabelle|Chavez|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c4dccaf6-6e5d-42f1-b731-b3747fe69023|Samantha|Fry|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c4feeda7-dbab-4931-92cb-facef6499aae|Gabriella|Gentry|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c511dc45-9af5-49e4-aeef-881a9bbeae17|Violet|Woodward|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c79b8487-640f-486e-a236-8f1421450fd3|Arianna|Reese|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c8a91061-a989-4dc5-b342-4e8869b7de70|Penelope|Cook|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    c9ea70af-1534-49c1-bf2b-1ee9b517d85b|Ariana|Webb|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    cbabc721-3ce0-47b0-b5fb-d298fb924953|Riley|Villa|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    cf0f7865-1348-4938-a760-2b851dfe4796|Chloe|Carr|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    d6d968e2-9826-4fa2-9727-085c904686b2|Charlotte|Mckee|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    d96d4c28-f8b4-4342-946e-46bcff884aa8|Gabriella|Weaver|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    dd5f7e21-c566-4905-a040-dd3b384a3b4c|Sadie|Frost|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    de1157fb-a3a7-4a3a-98b7-8cdf07542b47|Emma|Bautista|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    df312cf1-56b9-4db1-a5c9-0a928b488be0|Riley|Burgess|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    df9f7a45-630c-4c18-9f26-3d005b037a0e|Madison|Guerrero|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    e2d4f890-74b7-46e3-a755-1ea813b3ecd0|Chloe|Vega|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    e3ddb1ba-5601-4e28-b29f-ed75d7c38749|Hailey|Robertson|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    e56e6eba-ea49-42bc-b591-d8219f1728c9|Peyton|Weaver|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    e6d1397e-1869-4117-b771-27f981e36dd4|Ava|Carr|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    e7bf5f0a-be3d-4242-a4a1-46ddd1077f99|Caroline|Yang|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    eeb1ac8d-1e32-4a0c-bf41-80502db013ec|Isabella|Chavez|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    f4ed0c9c-d8ba-40fe-a93d-b99b82d54739|Paisley|Whitehead|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA==
    fe848b66-2913-4d0b-9d68-0b174697d549|Gabriella|Lloyd|Female|R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA=='''
    playerNames = [(p.split('|')[0],f"{p.split('|')[1]} {p.split('|')[2]}") for p in playerNamesList.split('\n')]
    
    simulatedPlayerObj = {}
    output = []
    
    for playerID, playerName in playerNames:
        print()
        playerPayload = {}
        if playerName not in simulatedPlayerObj:
            simulatedPlayerObj[playerName] = playerEvent(playerName, playerID)
            playerPayload = simulatedPlayerObj[playerName].getEventData()
        
        #print(f'[ INFO ] ****** {playerName}. playerPayload: {playerPayload}')
        counter = 0
        while playerPayload != None:
            counter += 1
            simulatedPlayerObj[playerName].newEvent()
            playerPayload = simulatedPlayerObj[playerName].getEventData()
            if playerPayload:
                output.append(playerPayload)
    
    print(f'[ INFO ] Total Records: {len(output)}')
    newOutput = sorted(output, key=lambda d: d['datetime'])
    
    newLineDelmitedJSON = ''
    for line in newOutput:
        newLineDelmitedJSON += f'{json.dumps(line)}\n'
    
    saveObjectToCloudStorage(bucket_name=bucket_name, blob_name=filename, data=newLineDelmitedJSON)
