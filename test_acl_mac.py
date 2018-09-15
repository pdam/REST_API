import py.test
import pytest
import random
import sys

sys.path.append(".")
import requests
import json

from acl_mac import acl_mac
from pprint import pprint
import logging


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg


from ParserUtils import generateRandomMac


username = "network-admin"
password = "test123"
testAclMAC = "restAclMac-%d"
subnet = random.randint(2, 200)
dst_mac_mask = "ff:00:ff:00:ff:00"
src_mac_mask = "00:ff:00:ff:00:ff"

def test_FailureAuthorizationcreateMacAcl(switch):
    """
           
    """
    pprint("testing Failed authentication  for createMacAcl with url http://%s/vRest/acl-macs" % switch)
    response = requests.get("http://%s/vRest/acl-macs" % switch)
    assert response.status_code == 401


testdata = [  # src_mac_mask,name,vlan,src_port,dst_mac_mask,src_mac,dst_port,action,scope,dst_mac,port
    (src_mac_mask, testAclMAC % random.randint(0, 20000),   0, dst_mac_mask , generateRandomMac(), 'permit',  generateRandomMac())
]


@pytest.mark.parametrize(
        "src_mac_mask,name,vlan,dst_mac_mask,src_mac,action,dst_mac", testdata)
def test_POSTcreateMacAcl(switch,src_mac_mask, name,  vlan, dst_mac_mask, src_mac, action,
                          dst_mac):
    """

    """
    c = acl_mac(switch)
    payload = json.dumps({'src-mac-mask': src_mac_mask, 'name': name,  'vlan': vlan,
               'dst-mac-mask': dst_mac_mask, 'src-mac': src_mac,  'action': 'permit',
               'scope': 'fabric', 'dst-mac': dst_mac})
    pprint("testing POST  for createMacAcl for url  %s  with  payload  %s"%( "http://%s/vRest/acl-macs" % (switch), payload ) )
    response = requests.post("http://%s/vRest/acl-macs" % (switch), auth=(username, password), data=payload)
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp= [ x  for x  in  c.show() if  x['name'] == name ]
    pprint("=========JSON Output================")
    pprint(response.json())
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint(cliResp)
    pprint("=========================")


def test_FailureAuthorizationshowMacAcls(switch):
    """
           
        """
    pprint("testing Failed authentication  for showMacAcls for url  http://%s/vRest/acl-macs" % switch)
    response = requests.get("http://%s/vRest/acl-macs" % switch)
    assert response.status_code == 401


def test_GETshowMacAcls(switch):
    """
           
        """
    c = acl_mac(switch)
    pprint("testing GET  for showMacAcls with url http://%s/vRest/acl-macs" % (switch))
    response = requests.get("http://%s/vRest/acl-macs" % (switch), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint("=========JSON Output================")
    pprint(jsonResponseDat)
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint(cliresponseHash)
    pprint("=========================")
    assert len(cliresponseHash) == len(jsonResponseDat)

def test_FailureAuthorizationshowMacAclByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for showMacAclByName with url  http://%s/vRest/acl-macs/name/name" % switch)
    response = requests.get("http://%s/vRest/acl-macs/name/name1" % switch)
    assert response.status_code == 401


testdata = [
    (testAclMAC % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_GETshowMacAclByName(switch,name):
    """
           
        """
    c = acl_mac(switch)
    c.create(name,generateRandomMac(),generateRandomMac())
    pprint("testing GET  for showMacAclByName with url http://%s/vRest/acl-macs/name/%s" % (switch, name))
    response = requests.get("http://%s/vRest/acl-macs/name/%s" % (switch, name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp= [ x  for x  in  c.show() if  x['name'] == name ]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint("=========JSON Output================")
    pprint(jsonResponseDat)
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint(cliResp)
    pprint("=========================")


def test_FailureAuthorizationupdateMacAclByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for updateMacAclByName for  url http://%s/vRest/acl-macs/name/%s" % (switch, testAclMAC % random.randint(0, 20000)))
    response = requests.get("http://%s/vRest/acl-macs/name/%s" % (switch, testAclMAC % random.randint(0, 20000)))
    assert response.status_code == 401


testdata = [  # acl_name ,src_mac_mask,vlan,test_src_mac,dst_mac_mask,action,test_dst_mac
     (testAclMAC % random.randint(0, 20000), src_mac_mask,   0, generateRandomMac(), dst_mac_mask, 'deny',  generateRandomMac())
]


@pytest.mark.parametrize("mac_acl_name,src_mac_mask,vlan,dst_mac_mask,src_mac,action,dst_mac",
                         testdata)
def test_PUTupdateMacAclByName(switch,mac_acl_name, src_mac_mask, vlan, dst_mac_mask, src_mac, action,dst_mac
                               ):
    """
       
    """
    c = acl_mac(switch)
    c.create(mac_acl_name , generateRandomMac() , generateRandomMac())
    actionBefore = [ x['action']  for  x in  c.show()  if   x['name'] ==str(mac_acl_name)]

    payload = json.dumps({
                'action': action
               })
    pprint("testing PUT  for updateMacAclByName with url %s payload %s "%("http://%s/vRest/acl-macs/name/%s" % (switch, mac_acl_name) , payload))
    response = requests.put("http://%s/vRest/acl-macs/name/%s" % (switch, mac_acl_name), auth=(username, password),
                            data=payload)
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    actionAfter = [ x['action']  for  x in  c.show()  if   x['name'] ==str(mac_acl_name)][0]
    assert action ==  actionAfter
    cliResp= [ x  for x  in  c.show() if  x['name'] == mac_acl_name ]
    jsonResponseDat = json.loads(response.text)
    pprint("=========JSON Output================")
    pprint(jsonResponseDat)
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint(cliResp)
    pprint("=========================")




def test_GETshowMacAclByIdent(switch):
    """
           
    """
    c = acl_mac(switch)
    acl_mac_name=testAclMAC % random.randint(0, 20000)
    c.create(acl_mac_name,generateRandomMac(),generateRandomMac())
    testAclMACId = c.getAclId(acl_mac_name)
    pprint("testing GET  for showMacAclByIdent with url  http://%s/vRest/acl-macs/id/%s" % (switch, testAclMACId))
    response = requests.get("http://%s/vRest/acl-macs/id/%s" % (switch, testAclMACId), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp= [ x  for x  in  c.show() if  x['id'] == testAclMACId ]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint("=========JSON Output================")
    pprint(jsonResponseDat)
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint(cliResp)
    pprint("=========================")


def test_FailureAuthorizationupdateMacAclByIdent(switch):
    """
           
        """
    pprint("testing Failed authentication  for updateMacAclByIdent for url  http://%s/vRest/acl-macs/id/7" % switch)
    response = requests.get("http://%s/vRest/acl-macs/id/7" % switch)
    assert response.status_code == 401


testdata = [  # src_mac_mask,name,proto,vlan,src_port,dst_mac_mask,src_mac,dst_port,action,scope,dst_mac,port
    (src_mac_mask, testAclMAC % random.randint(0, 20000),   0, generateRandomMac(), dst_mac_mask, 'deny',  generateRandomMac() ,40)
]


@pytest.mark.parametrize("src_mac_mask,name,vlan,dst_mac_mask,src_mac,action,dst_mac,port",
                         testdata)
def test_PUTupdateMacAclByIdent(switch,src_mac_mask, name,vlan, dst_mac_mask, src_mac, action,
                                dst_mac, port):
    """
       
    """
    c = acl_mac(switch)
    c.create(name , src_mac , dst_mac)
    actionBefore = [ x['action']  for  x in  c.show()  if   x['name'] ==str(name)]
    testAclMACId = c.getAclId(name)
    pprint(testAclMACId)

    response = requests.put("http://%s/vRest/acl-macs/id/%s" % (switch, testAclMACId), auth=(username, password),
                            data=json.dumps({
                                              'action': action}))
    pprint("testing PUT  for updateMacAclByIdent with url %s  payload  %s"%("http://%s/vRest/acl-macs/id/%s" % (switch, testAclMACId),  json.dumps({
                                              'action': action})))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    actionAfter = [ x['action']  for  x in  c.show()  if   x['name'] ==str(name)][0]
    assert action ==  actionAfter
    cliResp= [ x  for x  in  c.show() if  x['id'] == testAclMACId ]
    jsonResponseDat = json.loads(response.text)
    pprint("=========JSON Output================")
    pprint(jsonResponseDat)
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint(cliResp)
    pprint("=========================")



def test_FailureAuthorizationdeleteMacAclByIdent(switch):
    """
           
        """
    pprint("testing Failed authentication  for deleteMacAclByIdent with url  http://%s/vRest/acl-macs/id/7" % switch )
    response = requests.get("http://%s/vRest/acl-macs/id/7" % switch)
    assert response.status_code == 401


def test_FailureAuthorizationdeleteMacAclByName(switch):
    """

        """
    pprint("testing Failed authentication  for deleteMacAclByName http://%s/vRest/acl-macs/name/%s" % (switch, testAclMAC % random.randint(0, 20000)))
    response = requests.get("http://%s/vRest/acl-macs/name/%s" % (switch, testAclMAC % random.randint(0, 20000)))
    assert response.status_code == 401


testdata = [  #
    (testAclMAC % random.randint(0, 20000))
]


@pytest.mark.parametrize("acl_name", testdata)
def test_DELETEdeleteMacAclByName(switch,acl_name):
    """

    """
    c=acl_mac(switch)
    c.create(acl_name,generateRandomMac(),generateRandomMac())
    pprint("testing DELETE  for deleteMacAclByName for  http://%s/vRest/acl-macs/name/%s" % (switch, acl_name))
    response = requests.delete("http://%s/vRest/acl-macs/name/%s" % (switch, acl_name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    id = c.getAclId(acl_name)
    assert  id == None



def test_FailureAuthorizationshowMacAclByIdent(switch):
    """

    """
    pprint("testing Failed authentication  for showMacAclByIdent with url  http://%s/vRest/acl-macs/id/7" % switch)
    response = requests.get("http://%s/vRest/acl-macs/id/7" % switch)
    assert response.status_code == 401


testdata = [  #
    (testAclMAC % random.randint(0, 20000))
]


@pytest.mark.parametrize("acl_name", testdata)
def test_DELETEdeleteMacAclByIdent(switch,acl_name):
    """
       
    """
    c=acl_mac(switch)
    c.create(acl_name,generateRandomMac(),generateRandomMac())
    mac_aclid=c.getAclId(acl_name)
    pprint(mac_aclid)
    pprint("testing DELETE  for deleteMacAclByIdent for http://%s/vRest/acl-macs/id/%s" % (switch, mac_aclid))
    response = requests.delete("http://%s/vRest/acl-macs/id/%s" % (switch, mac_aclid), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    id = c.getAclId(acl_name)
    assert  id == None


def test_teardown(switch):
    v = acl_mac(switch)
    v.deleteAll()
