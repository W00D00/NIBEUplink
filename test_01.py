# -*- coding: utf-8 -*-

import logging
import requests
import json
import re

from nibe import config

logger = logging.getLogger()

class NibeUplink(object):
    def __init__(self, username, password, systemid):
        self.auth_data = {
            "email": username,
            "password": password,
            "systemid": systemid,
            }
        
        # https://www.nibeuplink.com/LogIn?ReturnUrl=%2fSystem%2f29276%2fStatus%2fOverview
#        self.nibeuplinkurl = "https://api.nibeuplink.com/"
        self.nibeuplinkurl = "https://www.nibeuplink.com/LogIn"
        
        self.authenticated = False
        self.session = requests.Session()
        
    def login(self):
        auth_result = self.session.post(self.nibeuplinkurl, self.auth_data)
        if auth_result.status_code == 200:
            self.authenticated = True
            logger.info("Succesfully authenticated.")
            return True
        else:
            logger.error("Failed to authenticate with status code: %d, content: %s", 
                         auth_result.status_code,
                         auth_result.content,
                         )
            return False

    def normalize_value(self, value):
        try:
            return float(re.sub('^([-\d.]+)(Hz|h|%|\u00B0C|DM|cent/kWh)?$', r'\1\2', value, flags = re.UNICODE))
        except ValueError:
            pass

        return value

    def getValues(self, *args):
        if not self.authenticated:
            if not self.login():
                raise Exception("Unable to get Nibe uplink values. Authentication failed")
            
        variable_query_result = self.session.post('https://www.nibeuplink.com/PrivateAPI/Values', {
            "hpid": self.auth_data['systemid'],
            "variables": args
            })
        
        decoded = {}
        
        try:
            data = json.loads(variable_query_result.content)
        except ValueError as e:
            logger.exception("Failed to decode JSON object: %s. Request status code: %d", variable_query_result.content, 
                             variable_query_result.status_code)
            # try to reauth
            self.authenticated = False
        
            return None, None
        
        if 'IsOffline' in data and 'Values' in data:
            online = not data['IsOffline']
            values = data['Values']
            for value in values:
                if 'VariableId' in value and 'CurrentValue' in value:
                    v = value['CurrentValue']
                    v = self.normalize_value(v)
                    decoded[value['VariableId']] = v

            logger.info("Fetched: %s", str(decoded))
            return online, decoded

        return None, None
    
    def setValue(self):
        # https://www.nibeuplink.com/System/29276/Manage/1.1.2/Boxed
        # 48785:24
        r = self.session.post('https://www.nibeuplink.com/System/29276/Manage/1.1.2/Boxed', {"48785": "25"})
        print(r)


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
    nibe = NibeUplink(**config)
    
    r = nibe.login()
    print(r)
    #print(nibe.getValues([40067]))
    print(nibe.setValue())
    
