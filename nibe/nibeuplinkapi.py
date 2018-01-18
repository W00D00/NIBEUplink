# -*- coding: utf-8 -*-

import logging
import requests
import json
from ast import literal_eval


# create logger
logger = logging.getLogger("nibeuplinkapi")
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class RequestError(Exception) :
    """
    """
    def __init__(self, code) :
        super(RequestError, self).__init__()
        self.code = code


class InvalidResponseError(Exception) :
    """
    """
    pass


def token_refresher(func) :
    """
    """
    def wrapper(*args, **kwargs) :
        while True :
            try :
                return func(*args, **kwargs)
            except RequestError as e :
                if e.code == 401 :
                    args[0]._refreshToken()
                else :
                    raise e
    return wrapper


class NIBEUplinkAPI():
    """
    API documentation: https://api.nibeuplink.com/docs/v1
    
    """
    def __init__(self, client_id, client_secret) :
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.session()
        self.access_token = None
        self.refresh_token = None
        
        self.api_base_url = 'https://api.nibeuplink.com'
        self.refresh_token_url = 'oauth/token'
        
        self.__loadToken()

    @token_refresher
    def __callApi(self, funcUrl, params = {}) :
        """
        Decorator is used to handle the errors.
        """
        r = self.session.get('{}/{}'.format(self.api_base_url, funcUrl), 
                             headers = {'Authorization' : 'Bearer %s' % self.access_token}, 
                             params = params
                             )
        if r.status_code != 200 :
            raise RequestError(r.status_code)
        return r

    def _refreshToken(self) :
        """
        """
        logger.info('Refreshing token ...')
        r = self.session.post('{}/{}'.format(self.api_base_url, 
                                             self.refresh_token_url
                                             ),
                              {'grant_type' : 'refresh_token', 
                               'refresh_token' : self.refresh_token, 
                               'client_id' : self.client_id, 
                               'client_secret' : self.client_secret
                               }
                              )
        if r.status_code != 200 :
            raise RequestError(r.status_code)
        data = json.loads(r.text)
        if 'access_token' not in data or 'refresh_token' not in data :
            raise InvalidResponseError
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.__saveToken()

    def __loadToken(self) :
        """
        """
        with open('nibe/token.txt', 'r') as f:
            self.access_token = f.readline().strip()
            self.refresh_token = f.readline().strip()
        logger.info('Token is loaded from file.')

    def __saveToken(self) :
        """
        """
        with open('nibe/token.txt', 'w') as f:
            f.write('{}\n{}\n'.format(self.access_token, self.refresh_token))
        logger.info('Token is saved into file.')
        
    def __replaceVars2PythonFormat(self, respText):
        res = respText.replace('true', 'True').replace('false', 'False').replace('null', 'None')
        return res
        
    def __convert2PythonFormat(self, respText):
        res = literal_eval(self.__replaceVars2PythonFormat(respText))
        return res
        
        
    def getSoftwareInfo(self, serialNumber):
        """
        Get information about the current software release for a serial number.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-software_serialNumber
        """
        r = self.__callApi('api/v1/software', {'serialNumber' : serialNumber})
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Software info: {}'.format(res))
        return res
        
    def getSystemUnits(self, systemId):
        """
        Get all system units ("units") connected to system. A unit is a single entity in a system, i.e. a master, a slave or an outdoor unit. 
        In case of a system without the ability for slaves or outdoor units this function will return only one unit, the master.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-units
        """
        r = self.__callApi('api/v1/systems/{systemId}/units'.format(systemId=systemId))
        res = self.__convert2PythonFormat(r.text)
        logger.debug('System units: {}pcs - {}'.format(len(res), res))
        return res
        
    def getSystemInfo(self, systemId):
        """
        Get the information about a single connected system.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId
        """
        r = self.__callApi('api/v1/systems/{systemId}'.format(systemId=systemId))
        res = self.__convert2PythonFormat(r.text)
        logger.debug('System info: {}'.format(res))
        return res
        
    def getSystemSoftwareInfo(self, systemId):
        """
        Get information about the currently installed software version and whether and upgrade is available.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-software
        """
        r = self.__callApi('api/v1/systems/{systemId}/software'.format(systemId=systemId))
        res = self.__convert2PythonFormat(r.text)
        logger.debug('System software info: {}'.format(res))
        return res
        
    def getProductConfig(self, systemId):
        """
        Get the configuration of the system, i.e. whether it can produce hot water, heating and so on.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-config
        """
        r = self.__callApi('api/v1/systems/{systemId}/config'.format(systemId=systemId))
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Product config: {}'.format(res))
        return res
        
    def getCurrentSystemStatus(self, systemId):
        """
        Get the current system status. This function returns the overall system status.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-status-system
        """
        r = self.__callApi('api/v1/systems/{systemId}/status/system'.format(systemId=systemId))
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Current system status: {}'.format(res))
        return res
        
    def getCurrentSystemUnitStatus(self, systemId, systemUnitId):
        """
        Get the current system unit status. This function returns the status of the compressors and pumps of the system unit specified.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-status-systemUnit-systemUnitId
        """
        r = self.__callApi('api/v1/systems/{systemId}/status/systemUnit/{systemUnitId}'.format(systemId=systemId, systemUnitId=systemUnitId))
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Current system unit status: {}'.format(res))
        return res

    def getNotifications(self, systemId) :
        """
        Get notifications registered on system. Use the filtering and the built-in paging to specify which notifications to get.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-notifications_type_active_page_itemsPerPage
        """
        r = self.__callApi('api/v1/systems/{systemId}/notifications'.format(systemId=systemId))
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Notifications: {}'.format(res))
        return res

    def getParameters(self, systemId, paramId) :
        """
        Get parameter info and their value.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-parameters_parameterIds[0]_parameterIds[1]
        """
        r = self.__callApi('api/v1/systems/{systemId}/parameters'.format(systemId=systemId), {'parameterIds' : paramId})
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Parameters: {}'.format(res))
        return res
        
    def getCategories(self, systemId, systemUnitId, parameters=False):
        """
        Get the available categories for service info data on system.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-serviceinfo-categories_systemUnitId_parameters
        """
        r = self.__callApi('api/v1/systems/{systemId}/serviceinfo/categories'.format(systemId=systemId), {'systemUnitId' : systemUnitId, 'parameters': parameters})
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Categories: {}'.format(res))
        return res
        
    def getCategoryParameters(self, systemId, categoryId, systemUnitId):
        """
        Get all parameters available in a specific service info category on system.
        Categories: https://api.nibeuplink.com/docs/v1/ResourceModel?modelName=Categories
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-serviceinfo-categories-categoryId_systemUnitId
        """
        r = self.__callApi('api/v1/systems/{systemId}/serviceinfo/categories/{categoryId}'.format(systemId=systemId, categoryId=categoryId), {'systemUnitId' : systemUnitId})
        res = self.__convert2PythonFormat(r.text)
        logger.debug('Category parameters: {}'.format(res))
        return res
        
    def getSystems(self) :
        """
        List the user's connected systems. The results are paged, please use the URI parameters to specify paging options.
        Further description details: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems_page_itemsPerPage
        """
        r = self.__callApi('api/v1/systems')
        data = json.loads(r.text)
        if 'objects' not in data :
            raise InvalidResponseError
        logger.debug('Systems: {}'.format(data))
        return data['objects']
