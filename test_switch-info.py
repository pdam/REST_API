import sys

import pytest
sys.path.append(".")
import requests
import json
from switch_info import switch_info
from pprint  import pprint
import logging

def logAssert(test,msg):
    if not test:
        logging.error(msg)
        assert test,msg
        

username="network-admin"
password="test123"



def test_FailureAuthorizationshowHwInfo(switch):
        """
           
        """
        pprint("testing Failed authentication  for showHwInfo with  url http://%s/vRest/switch-info"%switch)
        response = requests.get("http://%s/vRest/switch-info"%switch )
        assert response.status_code == 401
        
        



           
def test_GETshowHwInfo(switch):
        """
           
        """
        c=switch_info(switch)
        pprint("testing GET  for showHwInfo with url http://%s/vRest/switch-info"%(switch))
        response = requests.get("http://%s/vRest/switch-info"%(switch) , auth=(username , password))
        pprint("=========JSON  OUTOUT =============")
        pprint(response.json())
        pprint("=========END  OF  JSON  OUTOUT =============")
        pprint("=========CLI  OUTOUT =============")
        pprint(c.show()[0])
        pprint("=========END  OF  CLI  OUTOUT =============")
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()[0]
        jsonResponseDat=json.loads(response.text)["data"][0]
        assert cliresponseHash['chassis-serial'] ==  jsonResponseDat['chassis-serial']
        if cliresponseHash.has_key('cpu1-type'):
            assert cliresponseHash['cpu1-type']   ==  jsonResponseDat['cpu1-type']
        if cliresponseHash.has_key('cpu2-type'):
            assert cliresponseHash['cpu2-type']==  jsonResponseDat['cpu2-type']
        if cliresponseHash.has_key('fan1-status'):
            assert cliresponseHash['fan1-status']==  jsonResponseDat['fan1-status']
        if cliresponseHash.has_key('fan2-status'):
            assert cliresponseHash['fan2-status']==  jsonResponseDat['fan2-status']
        if cliresponseHash.has_key('fan3-status'):
            assert cliresponseHash['fan3-status']==  jsonResponseDat['fan3-status']
        if cliresponseHash.has_key('fan4-status'):
            assert cliresponseHash['fan4-status']==  jsonResponseDat['fan4-status']
        if cliresponseHash.has_key('gandalf-version'):
            assert cliresponseHash['gandalf-version'][2:] ==  jsonResponseDat['gandalf-version'][10:]
        if cliresponseHash.has_key('model'):
            assert cliresponseHash['model']==  jsonResponseDat['model']
        if cliresponseHash.has_key('polaris-device'):
            assert cliresponseHash['polaris-device']==  jsonResponseDat['polaris-device']
        if cliresponseHash.has_key('ps1-status'):
            assert cliresponseHash['ps1-status']==  jsonResponseDat['ps1-status']
        if cliresponseHash.has_key('ps2-status'):
            assert cliresponseHash['ps2-status']==  jsonResponseDat['ps2-status']
        if cliresponseHash.has_key('switch-device'):
           assert cliresponseHash['switch-device']==  jsonResponseDat['switch-device']





