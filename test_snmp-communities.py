
import py.test
import pytest

import sys
sys.path.append(".")
import requests
import json

from snmp_community import snmp_community
from pprint  import pprint
import logging

def logAssert(test,msg):
    if not test:
        logging.error(msg)
        assert test,msg
        
        

username="network-admin"
password="test123"



def test_FailureAuthorizationcreateAdminSnmpCommunity(switch):
        """
           
        """
        logging.info("testing Failed authentication  for createAdminSnmpCommunity ")
        response = requests.get("http://%s/vRest/snmp-communities"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # community_string,community_type
               ('rest123', 'read-only')
        ]

@pytest.mark.parametrize("community_string,community_type", testdata)                          
def test_POSTcreateAdminSnmpCommunity(switch,community_string,community_type):
    """
       
    """
    c=snmp_community(switch)
    cliresponseListOfHashBefore =c.show()
    payload={
  "community-string": community_string,
  "community-type": community_type
    }
    pprint(payload)
    response = requests.delete("http://%s/vRest/snmp-communities/%s"%(switch ,community_string) , auth=(username , password))
    logging.info("testing POST  for createAdminSnmpCommunity ")
    response = requests.post("http://%s/vRest/snmp-communities"%(switch) , auth=(username , password), data=json.dumps(payload))
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)

    
    
def test_FailureAuthorizationshowAdminSnmpCommunities(switch):
        """
           
        """
        logging.info("testing Failed authentication  for showAdminSnmpCommunities ")
        response = requests.get("http://%s/vRest/snmp-communities"%switch )
        assert response.status_code == 401
        
        



           

def test_GETshowAdminSnmpCommunities(switch):
        """
           
        """
        c=snmp_community(switch)
        logging.info("testing GET  for showAdminSnmpCommunities ")
        response = requests.get("http://%s/vRest/snmp-communities"%(switch) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        pprint(jsonResponseDat)
        pprint(cliresponseHash)

        

def test_FailureAuthorizationshowAdminSnmpCommunityByCommunityString(switch):
        """
           
        """
        logging.info("testing Failed authentication  for showAdminSnmpCommunityByCommunityString ")
        response = requests.get("http://%s/vRest/snmp-communities/{community-string}"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # 
    ('rest123')
        ]
@pytest.mark.parametrize("community_string", testdata)
def test_GETshowAdminSnmpCommunityByCommunityString(switch,community_string):
        """
           
        """
        c=snmp_community(switch)
        logging.info("testing GET  for showAdminSnmpCommunityByCommunityString ")
        response = requests.get("http://%s/vRest/snmp-communities/%s"%(switch ,community_string) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        pprint(jsonResponseDat)
        pprint(cliresponseHash)

        

def test_FailureAuthorizationupdateAdminSnmpCommunityByCommunityString(switch):
        """
           
        """
        logging.info("testing Failed authentication  for updateAdminSnmpCommunityByCommunityString ")
        response = requests.get("http://%s/vRest/snmp-communities/{community-string}"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # community_type
    ( 'rest123' , 'read-only')
        ]
@pytest.mark.parametrize("community_string,community_type", testdata)
def test_PUTupdateAdminSnmpCommunityByCommunityString(switch,community_string,community_type):
    """
       
    """
    c=snmp_community(switch)
    cliresponseListOfHashBefore =c.show()
    logging.info("testing PUT  for updateAdminSnmpCommunityByCommunityString ") 
    response = requests.put("http://%s/vRest/snmp-communities/%s"%(switch ,community_string) , auth=(username , password) , data=json.dumps({ 'community-type' : community_type}))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)

    
def test_FailureAuthorizationdeleteAdminSnmpCommunityByCommunityString(switch):
        """
           
        """
        logging.info("testing Failed authentication  for deleteAdminSnmpCommunityByCommunityString ")
        response = requests.get("http://%s/vRest/snmp-communities/{community-string}"%switch )
        assert response.status_code == 401
        
        


           
testdata = [ # 
    ('rest123')
        ]

@pytest.mark.parametrize("community_string", testdata) 
def test_DELETEdeleteAdminSnmpCommunityByCommunityString(switch,community_string):
    """
       
    """
    c=snmp_community(switch)
    cliresponseListOfHashBefore =c.show()
    payload={
  "community-string": community_string,
  "community-type": "read-only"
    }
    pprint(payload)
    logging.info("testing POST  for createAdminSnmpCommunity ")
    response = requests.post("http://%s/vRest/snmp-communities"%(switch) , auth=(username , password), data=json.dumps(payload))
    logging.info("testing DELETE  for deleteAdminSnmpCommunityByCommunityString ") 
    response = requests.delete("http://%s/vRest/snmp-communities/%s"%(switch ,community_string) , auth=(username , password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)
