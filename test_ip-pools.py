import random

import py.test
import pytest

import sys

sys.path.append(".")
import requests
import json
from ip_pool import ip_pool
from vnet import vnet
from vlan import vlan
from pprint import pprint
import logging


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg


username = "network-admin"
password = "test123"
vlanId = random.randint(2, 4000)
randSubNet=random.randint(2,252)
testVnet = "restVNet-%d" % (random.randint(0, 20000))
testIPPool = "restPool-%d" % (random.randint(0, 20000))
testVlan = "restVlan-%d" % (vlanId)
start_ip='172.16.%d.1'%randSubNet
end_ip='172.16.%d.254'%randSubNet


def test_setup(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()
    ip_poolobj = ip_pool(switch)
    ip_poolobj.cleanAll()

def test_FailureAuthorizationcreateIpPool(switch):
    """
           
        """
    pprint("testing Failed authentication  for createIpPool with  url http://%s/vRest/ip-pools" % switch )
    response = requests.get("http://%s/vRest/ip-pools" % switch)
    assert response.status_code == 401


testdata = [  # name,vnet,start_ip,end_ip,netmask
    (testIPPool, testVnet,"172.16.23.10","172.16.23.1" , 24 , "Start ip 172.16.23.10 is larger than end ip 172.16.23.1"),
    (testIPPool, testVnet,"172.16.23.1","172.16.23.100" , 33 ,"Start ip 172.16.23.1 is not a usable address")

]


@pytest.mark.parametrize("name,vnet_name,start_ip,end_ip,netmask,message", testdata)
def test_POSTcreateIpPoolErrorMessages(switch, name, vnet_name, start_ip, end_ip, netmask,message):
    """

    """

    ippoolobj = ip_pool(switch)
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_id= v.getVNetIdForName(vnet_name)
    payload = { 'name' : str(testIPPool), 'vnet-id' : str(vnet_id), 'start-ip' : str(start_ip), 'end-ip' : str(end_ip), 'netmask' : netmask}
    pprint("testing POST  for createIpPool with  url  %s and payload  %s  "%("http://%s/vRest/ip-pools" % (switch),payload ))
    response = requests.post("http://%s/vRest/ip-pools" % (switch), auth=(username, password), data=json.dumps(payload))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    assert message  in json.loads(response.text)["result"]["result"][0]["message"]
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0
    v.deleteVnet(vnet_name)




testdata = [  # name,vnet,start_ip,end_ip,netmask
    (testIPPool, testVnet,start_ip,end_ip , 24)
]


@pytest.mark.parametrize("name,vnet_name,start_ip,end_ip,netmask", testdata)
def test_POSTcreateIpPool(switch, name, vnet_name, start_ip, end_ip, netmask):
    """
       
    """

    ippoolobj = ip_pool(switch)
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_id= v.getVNetIdForName(vnet_name)
    v1 = vlan(switch)
    v1.create( vlanId, "fabric", "30,31")
    payload = { 'name' : str(testIPPool), 'vnet-id' : str(vnet_id), 'start-ip' : str(start_ip), 'end-ip' : str(end_ip), 'netmask' : netmask}
    pprint("testing POST  for createIpPool with  url  %s and payload  %s  "%("http://%s/vRest/ip-pools" % (switch),payload ))
    response = requests.post("http://%s/vRest/ip-pools" % (switch), auth=(username, password), data=json.dumps(payload))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in ippoolobj.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliCreated = [x for x in ippoolobj.show() if x['name'] == str(name)]
    assert cliCreated[0]['vnet'] == str(testVnet)
    assert cliCreated[0]['start-ip'] == str(start_ip)
    assert cliCreated[0]['end-ip'] == str(end_ip)


def test_FailureAuthorizationshowIpPools(switch):
    """
           
        """
    pprint("testing Failed authentication  for showIpPools ")
    response = requests.get("http://%s/vRest/ip-pools" % switch)
    assert response.status_code == 401


def test_GETshowIpPools(switch):
    """
           
        """
    ippoolobj = ip_pool(switch)
    pprint("testing GET  for showIpPools  for url  http://%s/vRest/ip-pools/%s" % (switch, testIPPool))
    response = requests.get("http://%s/vRest/ip-pools" % (switch), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint(ippoolobj.show())
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    ippoolList = [x['name'] for x in ippoolobj.show()]
    jsonResponseDat = json.loads(response.text)["data"]
    ippoolListFromREST = [x['name'] for x in jsonResponseDat]
    pprint(ippoolListFromREST)
    pprint(ippoolList)
    assert len(ippoolList) == len(ippoolListFromREST)


def test_FailureAuthorizationshowIpPoolByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for showIpPoolByName with url  http://%s/vRest/ip-pools/%s" % (switch, testIPPool))
    response = requests.get("http://%s/vRest/ip-pools/%s" % (switch, testIPPool))
    assert response.status_code == 401


testdata = [  #
    (testIPPool)
]


@pytest.mark.parametrize("name", testdata)
def test_GETshowIpPoolByName(switch,name):
    """
           
        """
    ippoolobj = ip_pool(switch)
    ippoolobj.createDefaultIPPoolForTesting(name)
    pprint("testing GET  for showIpPoolByName ")
    response = requests.get("http://%s/vRest/ip-pools/%s" % (switch, name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in ippoolobj.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    vnetCLI = [(x['start-ip'], x['end-ip']) for x in ippoolobj.show() if x['name'] == str(name)][0]
    vnetREST = [(x['start-ip'], x['end-ip']) for x in json.loads(response.text)["data"]][0]
    assert vnetCLI == vnetREST


def test_FailureAuthorizationupdateIpPoolByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for updateIpPoolByName with  url  http://%s/vRest/ip-pools/%s" % (switch, testIPPool))
    response = requests.get("http://%s/vRest/ip-pools/%s" % (switch, testIPPool))
    assert response.status_code == 401


testdata = [  # name,vnet,start_ip,end_ip,netmask
    (testIPPool, testVnet, start_ip, end_ip, 24)
]


@pytest.mark.parametrize("name,vnet,mod_start_ip,mod_end_ip,netmask", testdata)
def test_PUTcreateIpPool(switch,name, vnet, mod_start_ip, mod_end_ip, netmask):
    """

    """
    from vnet import vnet
    ippoolobj = ip_pool(switch)
    v = vnet(switch)
    v.getVNetIdForName(testVnet)
    pprint("testing POST  for createIpPool with url %s  payload  %s" %("http://%s/vRest/ip-pools/%s" % (switch, testIPPool) ,json.dumps(
                                    {'start-ip': mod_start_ip, 'end-ip': mod_end_ip, 'netmask': netmask}) ))
    response = requests.put("http://%s/vRest/ip-pools/%s" % (switch, testIPPool), auth=(username, password),
                            data=json.dumps(
                                    {'start-ip': mod_start_ip, 'end-ip': mod_end_ip, 'netmask': netmask}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in ippoolobj.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliCreated = [x for x in ippoolobj.show() if x['name'] == str(testIPPool)]
    assert cliCreated[0]['vnet'] == str(testVnet)
    assert cliCreated[0]['start-ip'] == str(mod_start_ip)
    assert cliCreated[0]['end-ip'] == str(mod_end_ip)


def test_FailureAuthorizationdeleteIpPoolByName(switch):
    """
           
    """
    pprint("testing Failed authentication  for deleteIpPoolByName with url http://%s/vRest/ip-pools/%s" % (switch, testIPPool))
    response = requests.get("http://%s/vRest/ip-pools/%s" % (switch, testIPPool))
    assert response.status_code == 401


testdata = [  #
    (testIPPool)
]


@pytest.mark.parametrize("name", testdata)
def test_DELETEdeleteIpPoolByName(switch,name):
    """
       
    """
    ippoolobj = ip_pool(switch)
    ippoolobj.createDefaultIPPoolForTesting(name)
    pprint("testing DELETE  for deleteIpPoolByName ")
    response = requests.delete("http://%s/vRest/ip-pools/%s" % (switch, name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in ippoolobj.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert (len([x for x in ippoolobj.show() if x['name'] == str(testIPPool)])) == 0





def test_teardown(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()
    ip_poolobj = ip_pool(switch)
    ip_poolobj.cleanAll()
