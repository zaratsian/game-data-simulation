
####################################################
#
#   Game Event Simulator (Basic Simulation)
#
#   This simulator will randomly generate events,
#   at randomized intervals.
#
'''
USAGE:
python3 gaming-events-simulator-basic.py --outputFilename gamingEvents.json --outputFormat json --numEvent 1000000
python3 gaming-events-simulator-basic.py --outputFilename gamingEvents.csv --outputFormat csv --numEvent 1000000
'''
####################################################

import sys,os
import datetime, time
import random
import json
import argparse

####################################################
# Config
####################################################

game_types =['Creative']*5 + \
            ['Deathmatch']*1 + \
            ['Capture The Flag']*3 + \
            ['Tournament']*3 + \
            ['Complete This Stage']*5

game_maps = ['Tropical']*3 + \
            ['Artic']*3 + \
            ['Sandbox']*4 + \
            ['Planetscape']*1 + \
            ['Solarium']*1 + \
            ['Rural']*6 + \
            ['Arcadia']*1 + \
            ['Warfare']*5 + \
            ['Battlegrounds']*1

weapons =   ['Electro']*3 + \
            ['Hagar']*1 + \
            ['Shotgun']*5 + \
            ['Mine Layer']*1 + \
            ['Crylink']*1 + \
            ['Mortar']*1 + \
            ['Blaster']*3 + \
            ['Machine Gun']*4 + \
            ['Devastator']*1 + \
            ['Vortex']*1

usernames = ['ScaryPumpkin']*1 + \
            ['Scrapper']*16 + \
            ['Shooter']*20 + \
            ['SnakeEye']*10 + \
            ['SunVolt']*15 + \
            ['Swerve']*5 + \
            ['SwiftFox']*10

actions =   ['killed']*10 + \
            ['madeKill']*8 + \
            ['purchasedItem']*10 + \
            ['pointsCollected']*15 + \
            ['pointsLost']*9 + \
            ['unlockLevel']*10 + \
            ['violation']*1

####################################################
# Functions
####################################################

def simulate_payload(format=json, enable_sleep=True, sleep_duration=2, header=None):
    '''
    
    format:     json or csv as the output format.
    
    '''
    if enable_sleep:
        time.sleep(random.random()*sleep_duration)
    
    payload = {
        'uid':          int(random.random()*10000000),
        'datetime':     datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        'gameID':       random.randint(1000,1050),
        'gameType':     random.choice(game_types),
        'gameMap':      random.choice(game_maps),
        'player':       random.choice(usernames),
        'action':       random.choice(actions),
        'x_coord':      random.randint(1,100),
        'y_coord':      random.randint(1,100),
        'z_coord':      random.randint(1,100)
    }
    
    if format.lower() == 'csv':
        header  = ','.join( [str(v) for v in payload.keys()] )
        payload = ','.join( [str(v) for v in payload.values()] )
    
    return header, payload

####################################################
# Main
####################################################

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--outputFilename', required=True, type=str, help='Name of output file')
    parser.add_argument('--outputFormat',   required=True, type=str, help='Output file format (csv or json)')
    parser.add_argument('--numEvent',       required=True, type=int, help='Number of events to simulate')
    
    args = parser.parse_args()
    output_filename = args.outputFilename
    fileFormat      = (args.outputFormat).lower()
    
    f = open(output_filename, 'w')
    
    if fileFormat == 'json':
        for eventNum in range(args.numEvent):
            header, payload = simulate_payload(format="json", enable_sleep=False)
            f.write(json.dumps(payload)+'\n')
    
    elif fileFormat == 'csv':
        # First event
        header, payload = simulate_payload(format="csv", enable_sleep=False)
        f.write(header+'\n')
        f.write(payload+'\n')
        
        # All other event
        for eventNum in range(args.numEvent):
            header, payload = simulate_payload(format="csv", enable_sleep=False)
            f.write(payload+'\n')
    
    f.close()
    print(f'[ INFO ] Simulation complete. Output file is at {os.getcwd()}/{output_filename}')
