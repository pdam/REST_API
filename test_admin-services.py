
import py.test
import pytest

import sys
sys.path.append(".")
import requests
import json

from admin_service import admin_service
from pprint  import pprint
import logging

def logAssert(test,msg):
    if not test:
        logging.error(msg)
        assert test,msg
        
        

username="network-admin"
password="test123"



def test_FailureAuthorizationshowAdminServices(switch):
        """
           
        """
        logging.info("testing Failed authentication  for showAdminServices ")
        response = requests.get("http://%s/vRest/admin-services"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # 
        
        ]
@pytest.mark.parametrize("", testdata)
def test_GETshowAdminServices(switch):
        """
           
        """
        c=admin_service(switch)
        logging.info("testing GET  for showAdminServices ")
        response = requests.get("http://%s/vRest/admin-services"%(switch) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        pprint(jsonResponseDat)
        pprint(cliresponseHash)

        

def test_FailureAuthorizationshowAdminServiceByNic(switch):
        """
           
        """
        logging.info("testing Failed authentication  for showAdminServiceByNic ")
        response = requests.get("http://%s/vRest/admin-services/{if}"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # 
    ( 'data')
        ]
@pytest.mark.parametrize("iface", testdata)
def test_GETshowAdminServiceByNic(switch,iface):
        """
           
        """
        c=admin_service(switch)
        logging.info("testing GET  for showAdminServiceByNic ")
        response = requests.get("http://%s/vRest/admin-services/%s"%(switch ,iface) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        pprint(jsonResponseDat)
        pprint(cliresponseHash)

        

def test_FailureAuthorizationupdateAdminServiceByNic(switch):
        """
           
        """
        logging.info("testing Failed authentication  for updateAdminServiceByNic ")
        response = requests.get("http://%s/vRest/admin-services/{if}"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ #iface , web,web_ssl,snmp,web_port,web_ssl_port,nfs,ssh,scope,icmp,net_api
               ('data',True, True, True, '80', '443', '', '22', 'fabric', '', 'true')
        ]
@pytest.mark.parametrize("iface,web,web_ssl,snmp,web_port,web_ssl_port,nfs,ssh,scope,icmp,net_api", testdata)
def test_PUTupdateAdminServiceByNic(switch,iface,web,web_ssl,snmp,web_port,web_ssl_port,nfs,ssh,scope,icmp,net_api):
    """
       
    """
    c=admin_service(switch)
    cliresponseListOfHashBefore =c.show()
    logging.info("testing PUT  for updateAdminServiceByNic ")
    payload={  'snmp' :   snmp,   'ssh' : ssh, 'icmp' : icmp}
    response = requests.put("http://%s/vRest/admin-services/%s"%(switch ,iface) , auth=(username , password) , data=json.dumps(payload))
    print response.json()
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)

