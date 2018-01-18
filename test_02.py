
"""

Zoli

"""

import requests
import json

# otthon
CLIENT_ID = 'efdcdbb91d704610a2f035b7ce6b2c36'
CLIENT_SECRET = 'oeHCGqTYZELWZ3cVkLCX3vreVcpNuTV6SuP4f5oOYxY='

class RequestError(Exception) :
    def __init__(self, code) :
        super(RequestError, self).__init__()
        self.code = code

class InvalidResponseError(Exception) :
    pass

def token_refresher(func) :
    def wrapper(*args, **kwargs) :
        while True :
            try :
                return func(*args, **kwargs)
            except RequestError as e :
                if e.code == 401 :
                    args[0].__refreshToken()
                else :
                    raise e
    return wrapper

class Nibe :
    def __init__(self, client_id, client_secret, url = 'https://api.nibeuplink.com') :
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_base_url = url
        self.session = requests.session()
        self.access_token = None
        self.refresh_token = None
        self.__loadToken()

    def systems(self) :
        r = self.__callApi('systems')
        data = json.loads(r.text)
        if 'objects' not in data :
            raise InvalidResponseError
        return data['objects']

    def units(self, systemId) :
        r = self.__callApi('systems/%d/units' % systemId)
        print(r.text)

    def config(self, systemId) :
        r = self.__callApi('systems/%d/config' % systemId)
        print(r.text)

    def notifications(self, systemId) :
        r = self.__callApi('systems/%d/notifications' % systemId)
        print(r.text)

    def parameter(self, systemId, paramId) :
        r = self.__callApi('systems/%d/parameters' % systemId, {'parameterIds' : paramId})
        print(r.text)

    @token_refresher
    def __callApi(self, func, params = {}) :
        r = self.session.get('%s/api/v1/%s' % (self.api_base_url, func), headers = {'Authorization' : 'Bearer %s' % self.access_token}, params = params)
        if r.status_code != 200 :
            raise RequestError(r.status_code)
        return r

    def __refreshToken(self) :
        print('refreshing token ...')
        r = self.session.post('%s/oauth/token' % self.api_base_url, {'grant_type' : 'refresh_token', 'refresh_token' : self.refresh_token, 'client_id' : self.client_id, 'client_secret' : self.client_secret})
        if r.status_code != 200 :
            raise RequestError(r.status_code)
        data = json.loads(r.text)
        if 'access_token' not in data or 'refresh_token' not in data :
            raise InvalidResponseError
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.__saveToken()

    def __loadToken(self) :
        with open('nibeuplink/token.txt', 'r') as f:
            self.access_token = f.readline().strip()
            self.refresh_token = f.readline().strip()

    def __saveToken(self) :
        with open('nibeuplinkapi/token.txt', 'w') as f:
            f.write('%s\n%s\n' % (self.access_token, self.refresh_token))

n = Nibe(CLIENT_ID, CLIENT_SECRET)
systemId = n.systems()[0]['systemId']
print('systemId', systemId)
n.parameter(systemId, '43009')
n.units(systemId)
n.notifications(systemId)
