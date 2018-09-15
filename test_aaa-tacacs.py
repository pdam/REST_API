import random

import py.test
import pytest

import sys
sys.path.append(".")
import requests
import json

from aaa_tacacs import aaa_tacacs
from pprint  import pprint
import logging
def logAssert(test,msg):
    if not test:
        logging.error(msg)
        assert test,msg
        

username="network-admin"
password="test123"
testTacacs="restTacacs-%d"




def test_FailureAuthorizationcreateTacacs(switch):
        """
           
        """
        logging.info("testing Failed authentication  for createTacacs ")
        response = requests.get("http://%s/vRest/aaa-tacacs"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # sess_author,cmd_acct,name,authen_method,cmd_author,server,priority,secret,timeout,authen,scope,sess_acct,port
    ( 'session-auth', 'cmd_acct', testTacacs%random.randint(0,20000), 'ms-chap', 'cmd_author', '10.20.18.221', 42, 'secret-1451598185', 4, '', 'fabric', '', 72)
        ]

@pytest.mark.parametrize("sess_author,cmd_acct,name,authen_method,cmd_author,server,priority,secret,timeout,authen,scope,sess_acct,port", testdata)                          
def test_POSTcreateTacacs(switch,sess_author,cmd_acct,name,authen_method,cmd_author,server,priority,secret,timeout,authen,scope,sess_acct,port):
    """
       
    """
    c=aaa_tacacs(switch)
    c.cleanUpTatacsConfiguration()
    logging.info("testing POST  for createTacacs ")
    payload ={ 'sess-author' : sess_author, 'cmd-acct' : cmd_acct, 'name' :  name, 'authen-method' : authen_method,  'cmd-author' : cmd_author, 'server' : server, 'secret' : secret , 'timeout' : timeout, 'authen' : authen, 'scope' : scope, 'sess-acct' : sess_acct, 'port' : port}
    response = requests.post("http://%s/vRest/aaa-tacacs"%(switch) , auth=(username , password), data =json.dumps(payload))
    print  response.json()
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashAfter)

    
def test_FailureAuthorizationshowTacacs(switch):
        """
           
        """
        logging.info("testing Failed authentication  for showTacacs ")
        response = requests.get("http://%s/vRest/aaa-tacacs"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # 
        
        ]
@pytest.mark.parametrize("", testdata)
def test_GETshowTacacs(switch):
        """
           
        """
        c=aaa_tacacs(switch)
        logging.info("testing GET  for showTacacs ")
        response = requests.get("http://%s/vRest/aaa-tacacs"%(switch) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        pprint(jsonResponseDat)
        pprint(cliresponseHash)

        

def test_FailureAuthorizationshowTacacsByName(switch):
        """
           
        """
        logging.info("testing Failed authentication  for showTacacsByName ")
        response = requests.get("http://%s/vRest/aaa-tacacs/name"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # 
    ( testTacacs%random.randint(0,20000))
        ]
@pytest.mark.parametrize("tacacs_name", testdata)
def test_GETshowTacacsByName(switch,tacacs_name):
        """
           
        """
        c=aaa_tacacs(switch)
        c.cleanUpTatacsConfiguration()
        c.createTacacsServerForTesting(tacacs_name)
        logging.info("testing GET  for showTacacsByName ")
        response = requests.get("http://%s/vRest/aaa-tacacs/%s"%(switch ,tacacs_name) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        pprint(jsonResponseDat)
        pprint(cliresponseHash)
        c.deleteTacacsServerForTesting(tacacs_name)

        

def test_FailureAuthorizationupdateTacacsByName(switch):
        """
           
        """
        logging.info("testing Failed authentication  for updateTacacsByName ")
        response = requests.get("http://%s/vRest/aaa-tacacs/name"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # sess_author,cmd_acct,authen_method,cmd_author,server,priority,secret,timeout,authen,scope,sess_acct,port
    (  ( testTacacs%random.randint(0,20000)), '','', 'ms-chap', '', '10.20.18.221', 62, 'secret-1451598185', 46, '', 'fabric', '', 17)
        ]
@pytest.mark.parametrize("name,sess_author,cmd_acct,authen_method,cmd_author,server,priority,secret,timeout,authen,scope,sess_acct,port", testdata)
def test_PUTupdateTacacsByName(switch,name,sess_author,cmd_acct,authen_method,cmd_author,server,priority,secret,timeout,authen,scope,sess_acct,port):
    """
       
    """
    c=aaa_tacacs(switch)
    c.cleanUpTatacsConfiguration()
    c.createTacacsServerForTesting(name)
    cliresponseListOfHashBefore =c.show()
    logging.info("testing PUT  for updateTacacsByName ") 
    response = requests.put("http://%s/vRest/aaa-tacacs/%s"%(switch ,name) , auth=(username , password) , data=json.dumps({ 'sess-author' : sess_author, 'cmd-acct' : cmd_acct, 'authen-method' : authen_method, 'cmd-author' : cmd_author, 'server' : server,  'priority' : priority, 'secret' : secret, 'timeout' : timeout, 'authen' : authen, 'scope' : scope, 'sess-acct' : sess_acct, 'port' : port}))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)
    c.deleteTacacsServerForTesting(name)
    
def test_FailureAuthorizationdeleteTacacsByName(switch):
        """
           
        """
        logging.info("testing Failed authentication  for deleteTacacsByName ")
        response = requests.get("http://%s/vRest/aaa-tacacs/name"%switch )
        assert response.status_code == 401
        
        


           
testdata = [ # 
         ( testTacacs%random.randint(0,20000))
        ]

@pytest.mark.parametrize("name", testdata) 
def test_DELETEdeleteTacacsByName(switch,name):
    """
       
    """
    c=aaa_tacacs(switch)
    c.cleanUpTatacsConfiguration()
    c.createTacacsServerForTesting(name)
    logging.info("testing DELETE  for deleteTacacsByName ") 
    response = requests.delete("http://%s/vRest/aaa-tacacs/%s"%(switch ,name) , auth=(username , password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"


    
def test_FailureAuthorizationstatusTacacs(switch):
        """
           
        """
        logging.info("testing Failed authentication  for statusTacacs ")
        response = requests.get("http://%s/vRest/aaa-tacacs/status"%switch )
        assert response.status_code == 401
        
        


