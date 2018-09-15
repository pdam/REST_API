
import py.test
import pytest

import sys
sys.path.append(".")
import requests
import json

from admin_sftp import admin_sftp
from pprint  import pprint
import logging

def logAssert(test,msg):
    if not test:
        logging.error(msg)
        assert test,msg
        
        

username="network-admin"
password="test123"



def test_FailureAuthorizationupdateAdminSftp(switch):
        """
           
        """
        logging.info("testing Failed authentication  for updateAdminSftp ")
        response = requests.get("http://%s/vRest/admin-sftp"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # sftp_password,enable
               ('test123', 'true')
        ]
@pytest.mark.parametrize("sftp_password,enable", testdata)
def test_PUTupdateAdminSftp(switch,sftp_password,enable):
    """
       
    """
    c=admin_sftp(switch)
    logging.info("testing PUT  for updateAdminSftp ") 
    response = requests.put("http://%s/vRest/admin-sftp"%(switch) , auth=(username , password) , data=json.dumps({ 'sftp-password' : sftp_password, 'enable' :enable}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    val = c.show()[0]['enable']
    valHash ={ 'yes' :  'true' , 'no' : 'false'}
    assert valHash[val] == enable


    
def test_FailureAuthorizationshowAdminSftp(switch):
        """
           
        """
        logging.info("testing Failed authentication  for showAdminSftp ")
        response = requests.get("http://%s/vRest/admin-sftp"%switch )
        assert response.status_code == 401
        
        



           
testdata = [ # 
        
        ]
@pytest.mark.parametrize("", testdata)
def test_GETshowAdminSftp(switch):
        """
           
        """
        c=admin_sftp(switch)
        logging.info("testing GET  for showAdminSftp ")
        response = requests.get("http://%s/vRest/admin-sftp"%(switch) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success" 
        cliVal = c.show()[0]['enable']
        jsonResponseDat=json.loads(response.text)["data"][0]
        valHash ={ 'yes' :  'True' , 'no' : 'False'}
        assert valHash[cliVal] == str(jsonResponseDat['enable'])


        
