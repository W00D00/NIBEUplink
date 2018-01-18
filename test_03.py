# -*- coding: utf-8 -*-

"""
Nibe Monitor
Channel ID: 291891

https://thingspeak.com/channels/291891/api_keys

Write API Key: MIM5HVUFM30ZEERA
Read API Keys: KQ1IXB2GJXDZTJKL


API Requests

Update a Channel Feed
GET https://api.thingspeak.com/update?api_key=MIM5HVUFM30ZEERA&field1=0

Get a Channel Feed
GET https://api.thingspeak.com/channels/291891/feeds.json?api_key=KQ1IXB2GJXDZTJKL&results=2

Get a Channel Field
GET https://api.thingspeak.com/channels/291891/fields/1.json?api_key=KQ1IXB2GJXDZTJKL&results=2

Get Channel Status Updates
GET https://api.thingspeak.com/channels/291891/status.json?api_key=KQ1IXB2GJXDZTJKL

"""

import requests
import time
from ast import literal_eval

CHANNELID = "291891"
WRITEAPIKEY = "MIM5HVUFM30ZEERA"
READAPIKEY = "KQ1IXB2GJXDZTJKL"

session = requests.session()

def updateChannelFeed(params={}):
    r = session.get('https://api.thingspeak.com/update?api_key={}'.format(WRITEAPIKEY),
                    params = params,
                    )
    return r

def getChannelFeed(params={}):
    """
    {'channel': 
        {'id': 291891, 
        'name': 'Nibe Monitor (Sukoró)', 
        'latitude': '0.0', 
        'longitude': '0.0', 
        'field1': 'outdoor temp. BT1', 
        'field2': 'room temperature BT50', 
        'created_at': '2017-06-22T21:04:37Z', 
        'updated_at': '2017-06-25T19:29:29Z', 
        'last_entry_id': 10}, 
    'feeds': [
        {'created_at': '2017-06-25T19:15:05Z', 
        'entry_id': 9, 
        'field1': '12', 
        'field2': None}, 
        {'created_at': '2017-06-25T19:17:09Z', 
        'entry_id': 10, 
        'field1': None, 
        'field2': None}
    ]}
    """
    r = session.get('https://api.thingspeak.com/channels/{}/feeds.json?api_key={}'.format(CHANNELID, READAPIKEY),
                    params = params,
                    )
#     print(r.text)
    r = literal_eval(r.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
    return r


if __name__ == '__main__':
    while True:
#         updateChannelFeed({'field1': '12'})
        r = getChannelFeed({'results': '2'})
        print('{}: {}'.format(r['channel']['field1'], r['feeds'][-1]['field1']))
        
        time.sleep(10)