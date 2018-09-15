import sys

import pytest

sys.path.append(".")
import requests
from vnet_manager import vnet_manager
import json

from vnet import vnet
from pprint import pprint
import logging
import random


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg


portList = "40,41,42,43,45"
testVnetmgr = "VnetRest-%d-mgr"
testVnet = "VnetRest-%d"
portsToAdd = "48"
portToRemove = "40"
username = "network-admin"
password = "test123"
iface = "data"
nic = "eth0.2"
testNic = "eth0.%d"
testIPAddress = "172.16.%d.1"
testIPAddressNM = "172.16.%d.1/24"


def test_setup(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()


def test_FailureAuthorizationshowVnetmgrMgrs(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVnetmgrMgrs for url  http://%s/vRest/vnet-managers" % switch)
    response = requests.get("http://%s/vRest/vnet-managers" % switch)
    assert response.status_code == 401


testdata = [
    (
        testVnet % random.randint(0, 20000))
]


@pytest.mark.parametrize("vnetn", testdata)
def test_GETshowVnetmgrMgrs(switch, vnetn):
    """
           
        """
    v = vnet(switch)
    v.createVNetForTesting(vnetn)
    vnet_manager_name = v.getVNetManagerForName(vnetn)
    c = vnet_manager(switch)
    pprint("testing GET  for showVnetmgrMgrs with url  http://%s/vRest/vnet-managers" % (switch))
    response = requests.get("http://%s/vRest/vnet-managers" % (switch), auth=(username, password))
    assert str(response.status_code) == "200"
    jsonResp = json.loads(response.text)["data"]
    cliResp = [x for x in v.show() if x['name'] == vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(jsonResp)
    pprint("=========END  OF JSON  OUTOUT =============")
    cliObjCreated = [x for x in c.show() if str(x['name']) == "%s-mgr"%vnet_manager_name]
    assert cliObjCreated[0]['name'] == "%s-mgr"%vnet_manager_name
    assert cliObjCreated[0]['type'] == "vnet-mgr"
    assert cliObjCreated[0]['vnet'] == vnetn
    assert cliObjCreated[0]['scope'] == "fabric"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    v.deleteVnet(vnetn)


def test_FailureAuthorizationshowVnetmgrMgrByVnmName(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVnetmgrMgrByVnmName ")
    response = requests.get("http://%s/vRest/vnet-managers/%s" % (switch, testVnetmgr % random.randint(0, 20000)))
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000))
]


@pytest.mark.parametrize("vnet_name", testdata)
def test_GETshowVnetmgrMgrByVnmName(switch, vnet_name):
    """
           
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    pprint("testing GET  for showVnetmgrMgrByVnmName with  url  http://%s/vRest/vnet-managers/%s" % (
        switch, vnet_manager_name))
    response = requests.get("http://%s/vRest/vnet-managers/%s" % (switch, "%s-mgr"%vnet_manager_name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    vnetList = [x['name'] for x in mgr.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    vnetListFromREST = [x['name'] for x in json.loads(response.text)["data"]]
    jsonResp = json.loads(response.text)["data"]
    cliResp = [x for x in v.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(jsonResp)
    pprint("=========END  OF JSON  OUTOUT =============")
    assert len(vnetList) == len(vnetListFromREST)
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationupdateVnetmgrMgrByVnmName(switch):
    """
           
    """
    pprint("testing Failed authentication  for updateVnetmgrMgrByVnmName for  url  http://%s/vRest/vnet-managers/%s" % (
        switch, testVnetmgr % random.randint(0, 20000)))
    response = requests.get("http://%s/vRest/vnet-managers/%s" % (switch, testVnetmgr % random.randint(0, 20000)))
    assert response.status_code == 401


testdata = [  # state,gateway
    (testVnet % random.randint(0, 20000), 'enable', testIPAddress % random.randint(2, 200))
]


@pytest.mark.parametrize("vnet_name,state,gateway", testdata)
def test_PUTupdateVnetmgrMgrByVnmName(switch, vnet_name, state, gateway):
    """
       
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    pprint("testing PUT  for updateVnetmgrMgrByVnmName for  url  %s  payload  %s " % (
        "http://%s/vRest/vnet-managers/%s" % (switch, vnet_manager_name), json.dumps({u'state': state})))
    response = requests.put("http://%s/vRest/vnet-managers/%s" % (switch, "%s-mgr"%vnet_manager_name), auth=(username, password),
                            data=json.dumps({u'state': state}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp = [x for x in v.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationaddVnetmgrMgrNicByVnetmgrMgrVnmName(switch):
    """
           
        """
    pprint(
            "testing Failed authentication  for addVnetmgrMgrNicByVnetmgrMgrVnmName http://%s/vRest/vnet-managers/%s/interfaces" % (
                switch, testVnetmgr % random.randint(0, 20000)))
    response = requests.get(
            "http://%s/vRest/vnet-managers/%s/interfaces" % (switch, testVnetmgr % random.randint(0, 20000)))
    assert response.status_code == 401


def test_FailureAuthorizationshowVnetmgrMgrNicsByVnetmgrMgrVnmName(switch):
    """
           
        """
    pprint(
            "testing Failed authentication  for showVnetmgrMgrNicsByVnetmgrMgrVnmName with  url  http://%s/vRest/vnet-managers/%s/interfaces" % (
                switch, testVnetmgr % random.randint(0, 20000)))
    response = requests.get(
            "http://%s/vRest/vnet-managers/%s/interfaces" % (switch, testVnetmgr % random.randint(0, 20000)))
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000))
]


@pytest.mark.parametrize("vnet_name", testdata)
def test_GETshowVnetmgrMgrNicsByVnetmgrMgrVnmName(switch, vnet_name):
    """
           
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    nic = mgr.AddInterface("%s-mgr"%vnet_manager_name, "172.12.3.4/24")
    pprint(nic)
    pprint(
            "testing GET  for showVnetmgrMgrNicsByVnetmgrMgrVnmName for url http://%s/vRest/vnet-managers/%s/interfaces" % (
                switch, "%s-mgr"%vnet_manager_name))
    response = requests.get("http://%s/vRest/vnet-managers/%s/interfaces" % (switch, "%s-mgr"%vnet_manager_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResp = json.loads(response.text)["data"]
    cliResp = [x for x in v.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(jsonResp)
    pprint("=========END  OF JSON  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationshowVnetmgrMgrNicByVnmNameByVnic(switch):
    """
           
        """
    pprint(
            "testing Failed authentication  for showVnetmgrMgrNicByVnmNameByVnic with  url  http://%s/vRest/vnet-managers/vnet-manager-name/interfaces/nic" % switch)
    response = requests.get("http://%s/vRest/vnet-managers/vnet-manager-name/interfaces/nic" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000), testIPAddressNM % random.randint(4, 200))
]


@pytest.mark.parametrize("vnet_name,interface_ip", testdata)
def test_GETshowVnetmgrMgrNicByVnmNameByVnic(switch, vnet_name, interface_ip):
    """
           
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    nic = mgr.AddInterface("%s-mgr"%vnet_manager_name, interface_ip)
    pprint(nic)
    pprint(
            "testing GET  for showVnetmgrMgrNicByVnmNameByVnic for  url  http://%s/vRest/vnet-managers/%s/interfaces/%s" % (
                switch, "%s-mgr"%vnet_manager_name, nic))
    response = requests.get("http://%s/vRest/vnet-managers/%s/interfaces/%s" % (switch, "%s-mgr"%vnet_manager_name, nic),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResp = json.loads(response.text)["data"]
    cliResp = [x for x in mgr.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(jsonResp)
    pprint("=========END  OF JSON  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationupdateVnetmgrMgrNicByVnmNameByVnic(switch):
    """
           
    """
    pprint(
            "testing Failed authentication  for updateVnetmgrMgrNicByVnmNameByVnic for url  http://%s/vRest/vnet-managers/vnet-manager-name/interfaces/nic" % switch)
    response = requests.get("http://%s/vRest/vnet-managers/vnet-manager-name/interfaces/nic" % switch)
    assert response.status_code == 401


testdata = [  # state,gateway
    (testVnet % random.randint(2, 200000), testNic % random.randint(2, 40), testIPAddressNM % random.randint(2, 200),
     random.randint(2, 4090))
]


@pytest.mark.parametrize("vnet_name,nic,ip_address,vlan", testdata)
def test_PUTupdateVnetmgrMgrNicByVnmNameByVnic(switch, vnet_name, nic, ip_address, vlan):
    """
       
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    nic = mgr.AddInterface("%s-mgr"%vnet_manager_name, ip_address)
    pprint(nic)
    pprint("testing PUT  for updateVnetmgrMgrNicByVnmNameByVnic for url  %s  with payload  %s " % (
        "http://%s/vRest/vnet-managers/%s/interfaces/%s" % (switch, "%s-mgr"%vnet_manager_name, nic), json.dumps(
                {'netmask': 24, 'ip': ip_address[:-3], 'exclusive': 'false', 'vlan': vlan,
                 'if': 'data'})))
    response = requests.put("http://%s/vRest/vnet-managers/%s/interfaces/%s" % (switch, "%s-mgr"%vnet_manager_name, nic),
                            auth=(username, password), data=json.dumps(
                {'netmask': 24, 'ip': ip_address[:-3], 'exclusive': 'false', 'vlan': vlan,
                 'if': 'data'}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp = [x for x in mgr.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationremoveVnetmgrMgrNicByVnmNameByVnic(switch):
    """
           
        """
    pprint("testing Failed authentication  for removeVnetmgrMgrNicByVnmNameByVnic ")
    response = requests.get(
            "http://%s/vRest/vnet-managers/%s/interfaces/%s" % (switch, testVnetmgr % random.randint(2, 4090), iface))
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000), testIPAddressNM % random.randint(0, 20))
]


@pytest.mark.parametrize("vnet_name,ip_address", testdata)
def test_DELETEremoveVnetmgrMgrNicByVnmNameByVnic(switch, vnet_name, ip_address):
    """
       
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    nic = mgr.AddInterface("%s-mgr"%vnet_manager_name, ip_address)
    pprint(nic)
    pprint(
            "testing DELETE  for removeVnetmgrMgrNicByVnmNameByVnic for url  http://%s/vRest/vnet-managers/%s/interfaces/%s" % (
                switch, "%s-mgr"%vnet_manager_name, nic))
    response = requests.delete("http://%s/vRest/vnet-managers/%s/interfaces/%s" % (switch, "%s-mgr"%vnet_manager_name, nic),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = mgr.show()
    pprint(cliresponseListOfHashAfter)
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationshowVnetmgrMgrServicesByVnetmgrMgrVnmName(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVnetmgrMgrServicesByVnetmgrMgrVnmName ")
    response = requests.get("http://%s/vRest/vnet-managers/manager/services" % (switch))
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000))
]


@pytest.mark.parametrize("vnet_name", testdata)
def test_GETshowVnetmgrMgrServicesByVnetmgrMgrVnmName(switch, vnet_name):
    """
           
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    nic = mgr.AddInterface("%s-mgr"%vnet_manager_name, "172.16.2.33/24")
    pprint(nic)
    pprint(
            "testing GET  for showVnetmgrMgrServicesByVnetmgrMgrVnmName  for url http://%s/vRest/vnet-managers/%s/services" % (
                switch, "%s-mgr"%vnet_manager_name))
    response = requests.get("http://%s/vRest/vnet-managers/%s/services" % (switch, "%s-mgr"%vnet_manager_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResp = json.loads(response.text)["data"]
    cliResp = [x for x in mgr.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(jsonResp)
    pprint("=========END  OF JSON  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationshowVnetmgrMgrServiceByVnmNameByNic(switch):
    """
           
    """
    pprint(
            "testing Failed authentication  for showVnetmgrMgrServiceByVnmNameByNic with url  http://%s/vRest/vnet-managers/vnet-manager-name/services/if" % switch)
    response = requests.get("http://%s/vRest/vnet-managers/vnet-manager-name/services/if" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000), testIPAddressNM % random.randint(3, 200))
]


@pytest.mark.parametrize("vnet_name,ip_address", testdata)
def test_GETshowVnetmgrMgrServiceByVnmNameByNic(switch, vnet_name, ip_address):
    """
           
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    nic = mgr.AddInterface("%s-mgr"%vnet_manager_name, ip_address)
    pprint(nic)
    pprint(
            "testing GET  for showVnetmgrMgrServiceByVnmNameByNic for url   http://%s/vRest/vnet-managers/%s/services/%s" % (
                switch, "%s-mgr"%vnet_manager_name, nic))
    response = requests.get("http://%s/vRest/vnet-managers/%s/services/%s" % (switch, "%s-mgr"%vnet_manager_name, nic),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResp = json.loads(response.text)["data"]
    cliResp = [x for x in mgr.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(jsonResp)
    pprint("=========END  OF JSON  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationupdateVnetmgrMgrServiceByVnmNameByNic(switch):
    """
           
    """
    pprint(
            "testing Failed authentication  for updateVnetmgrMgrServiceByVnmNameByNic with url  http://%s/vRest/vnet-managers/vnet_manager/services/svc" % switch)
    response = requests.get("http://%s/vRest/vnet-managers/vnet_manager/services/svc" % switch)
    assert response.status_code == 401


testdata = [  # state,gateway
    (testVnet % random.randint(0, 20000), testIPAddressNM % random.randint(2, 200))
]


@pytest.mark.parametrize("vnet_name,ip_address", testdata)
def test_PUTupdateVnetmgrMgrServiceByVnmNameByNic(switch, vnet_name, ip_address):
    """

    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    mgr = vnet_manager(switch)
    nic = mgr.AddInterface("%s-mgr"%vnet_manager_name, ip_address)
    pprint(nic)
    pprint("testing PUT  for updateVnetmgrMgrServiceByVnmNameByNic  with url %s  payload  %s" % (
        "http://%s/vRest/vnet-managers/%s/services/%s" % (switch, "%s-mgr"%vnet_manager_name, nic), json.dumps(
                {'ssh': 'false', 'web': 'false', 'icmp': 'false', 'ntp': 'false', 'web-ssl': 'false',
                 'web-ssl-port': '8448', 'web-port': '80'})))
    response = requests.put("http://%s/vRest/vnet-managers/%s/services/%s" % (switch, "%s-mgr"%vnet_manager_name, nic),
                            auth=(username, password), data=json.dumps(
                {'ssh': 'false', 'web': 'false', 'icmp': 'false', 'ntp': 'false', 'web-ssl': 'false',
                 'web-ssl-port': '8448', 'web-port': '80'}))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp = [x for x in mgr.show() if x['name'] == "%s-mgr"%vnet_manager_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationmigrateVnetmgrMgr(switch):
    """
           
    """
    pprint(
            "testing Failed authentication  for migrateVnetmgrMgr with url  http://%s/vRest/vnet-managers/migrate" % switch)
    response = requests.get("http://%s/vRest/vnet-managers/migrate" % switch)
    assert response.status_code == 401


testdata = [
    (testVnet % random.randint(0, 200000), '', 9517372)
]


@pytest.mark.parametrize(
        "vnet_name,storage_pool,location",
        testdata)
def test_POSTmigrateVnetmgrMgr(switch, vnet_name, storage_pool, location):
    """
       
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    v.getVNetIdForName(vnet_name)
    vnet_manager_name = v.getVNetManagerForName(vnet_name)
    pprint("testing POST  for migrateVnetmgrMgr  with url  %s  payload  %s " % (
        "http://%s/vRest/vnet-managers/migrate" % (switch),
        json.dumps({u'name': "%s-mgr"%vnet_manager_name, 'location': location})))
    response = requests.post("http://%s/vRest/vnet-managers/migrate" % (switch), auth=(username, password),
                             data=json.dumps({u'name': "%s-mgr"%vnet_manager_name, 'location': location}))
    pprint(response.json())
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp = [x for x in v.show() if x['name'] == vnet_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    v.deleteVnet(vnet_name)


def test_cleanup(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()
