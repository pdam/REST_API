
import py.test
import pytest

import sys
sys.path.append(".")
import requests
import json

from switch_status import switch_status
from pprint  import pprint
import logging

def logAssert(test,msg):
    if not test:
        logging.error(msg)
        assert test,msg
        
        

username="network-admin"
password="test123"



def test_FailureAuthorizationshowHwStatuses(switch):
        """
           
        """
        pprint("testing Failed authentication  for showHwStatuses with url  http://%s/vRest/switch-statuses"%switch )
        response = requests.get("http://%s/vRest/switch-statuses"%switch )
        assert response.status_code == 401
        
        



           
def test_GETshowHwStatuses(switch):
        """
           
        """
        c=switch_status(switch)
        pprint("testing GET  for showHwStatuses  with url  http://%s/vRest/switch-statuses"%(switch) )
        response = requests.get("http://%s/vRest/switch-statuses"%(switch) , auth=(username , password))
        pprint("=========JSON  OUTOUT =============")
        pprint(response.json())
        pprint("=========END  OF  JSON  OUTOUT =============")
        pprint("=========CLI  OUTOUT =============")
        pprint(c.show())
        pprint("=========END  OF  CLI  OUTOUT =============")
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        paramsCheckedForValues =[ 'Switch Temp' , 'CPU1 Temp', 'CPU2 Temp', 'System Temp' ,'Peripheral Temp', 'PCH Temp' , 'fan-1' , 'fan-2' , 'fan-3', 'fan-4']
        paramsCheckedForState =[ 'VTT','CPU1 Vcore','CPU2 Vcore' ,  'switch-3.3v' ,
                         'switch-1.1v' , 'switch-2.5v', 'switch-5.0v' ,'switch-1.2v' ,'switch-1.8v' , 'switch-vcore' , 'switch-0.95v', 'VDIMM AB' ,'VDIMM CD','VDIMM EF','VDIMM GH' , '+1.1 V' , '+1.5 V','+3.3 V' , '+3.3VSB'
                         '5V' ,'+5VSB', '12V', 'VBAT']
        pprint(cliresponseHash)
        for param in paramsCheckedForValues :
            jsonParams ,cliParams=None ,None
            try:
                jsonParams =[ str(x['value']) for x in  jsonResponseDat if x['name'] == param ][0]
                cliParams =[  x['value'] for x in  cliresponseHash if  x['name']== param] [0]
                assert jsonParams == cliParams
            except:
                print "Parameter mismatch :%s JSON  :%s   CLI  : %s "%(param , jsonParams ,cliParams)

        for param in paramsCheckedForState :
            jsonParams ,cliParams=None ,None
            try:
                jsonParams =[ x['state'] for x in  jsonResponseDat if x['name'] == param ][0]
                cliParams =[  x['state'] for x in  cliresponseHash if  x['name']== param] [0]
                assert jsonParams == cliParams
            except:
                print "Parameter mismatch :%s JSON  :%s   CLI  : %s "%(param , jsonParams ,cliParams)
