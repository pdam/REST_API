import sys

import pytest

from vlan import vlan

sys.path.append(".")
import requests
import json

from vrg import vrg
from pprint import pprint
from ParserUtils import hyphen_range, randintWithExclude
import logging
import random


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg


username = "network-admin"
password = "test123"

portList = "40,41,42,43,45"
testVrg = "vrgRest-%d"
portsToAdd = "48"
portToRemove = "40"


def  test_setup(switch):
    v = vrg(switch)
    v.deleteAllVrgs()


def test_FailureAuthorizationcreateVrg(switch):
    """
           
        """
    pprint("testing Failed authentication  for createVrg  with  url  http://%s/vRest/vrgs" % switch)
    response = requests.get("http://%s/vRest/vrgs" % switch)
    assert response.status_code == 401


testdata = [  # vlans,ports
    (testVrg % random.randint(0, 20000), random.randint(2, 4090), portList)
]


@pytest.mark.parametrize("vrg_name,vlanid,ports", testdata)
def test_POSTcreateVrg(switch, vrg_name, vlanid, ports):
    """
       
    """
    from vlan import vlan
    v1 = vlan(switch)
    v1.create(vlanid, "fabric", portList)
    c = vrg(switch)
    pprint("testing POST  for createVrg with url %s and  payload  %s "%("http://%s/vRest/vrgs" % (switch) , json.dumps(
            {'name': vrg_name, 'scope': 'fabric', 'vlans': str(vlanid), 'ports': portList})))
    response = requests.post("http://%s/vRest/vrgs" % (switch), auth=(username, password), data=json.dumps(
            {'name': vrg_name, 'scope': 'fabric', 'vlans': str(vlanid), 'ports': portList}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == str(vrg_name)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert str(response.status_code) == "201"
    cliObjCreated = [x for x in c.show() if x['name'] == vrg_name]
    assert cliObjCreated[0]['name'] == vrg_name
    assert cliObjCreated[0]['vlans'] == str(vlanid)
    assert list(hyphen_range(cliObjCreated[0]['ports'])) == map(int, portList.split(","))
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"


def test_FailureAuthorizationshowVrgs(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVrgs  with url   http://%s/vRest/vrgs" % switch)
    response = requests.get("http://%s/vRest/vrgs" % switch)
    assert response.status_code == 401


def test_GETshowVrgs(switch):
    """
           
        """
    c = vrg(switch)
    vrgn = testVrg % random.randint(0, 20000)
    c.createVrgForTesting(vrgn)
    pprint("testing GET  for showVrgs http://%s/vRest/vrgs" % (switch))
    response = requests.get("http://%s/vRest/vrgs" % (switch), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == str(vrgn)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    vlanList = [x['name'] for x in c.show()]
    jsonResponseDat = json.loads(response.text)["data"]
    vlanListFromREST = [x['name'] for x in jsonResponseDat]
    pprint(vlanListFromREST)
    pprint(vlanList)
    assert len(vlanList) == len(vlanListFromREST)


def test_FailureAuthorizationshowVrgByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVrgByName ")
    response = requests.get("http://%s/vRest/vrgs/%s" % (switch, testVrg % random.randint(0, 20000)))
    assert response.status_code == 401


testdata = [  #
    (testVrg % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_GETshowVrgByName(switch, name):
    """
           
        """
    c = vrg(switch)
    c.createVrgForTesting(name)
    pprint("testing GET  for showVrgByName with url http://%s/vRest/vrgs/%s" % (switch, name))
    response = requests.get("http://%s/vRest/vrgs/%s" % (switch, name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == str(name)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    descCLI = [x['name'] for x in c.show() if x['name'] == str(name)][0]
    descREST = [x['name'] for x in json.loads(response.text)["data"]][0]
    assert descCLI == descREST


def test_FailureAuthorizationupdateVrgByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for updateVrgByName ")
    response = requests.get("http://%s/vRest/vrgs/%s" % (switch, testVrg % random.randint(0, 20000)))
    assert response.status_code == 401


testdata = [  # restricted_resources,data_bw_min,data_bw_max,numflows, vlans,ports
    (testVrg % random.randint(0, 20000),random.randint(2, 4090), random.randint(2, 40))
]


@pytest.mark.parametrize("name,vlans,ports", testdata)
def test_PUTupdateVrgByName(switch, name,vlans, ports):
    """
       
    """
    c = vrg(switch)
    c.createVrgForTesting(name)
    v1 = vlan(switch)
    v1.create(vlans, "fabric", ports)
    pprint("test_PUTupdateVrgByName   with  url  %s   and  payload %s"%("http://%s/vRest/vrgs/%s" % (switch, name)  , json.dumps({'vlans': str(vlans), 'ports': str(ports)})))

    response = requests.put("http://%s/vRest/vrgs/%s" % (switch, name), auth=(username, password),
                            data=json.dumps({'vlans': str(vlans), 'ports': str(ports)}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == str(name)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    vlansAfter = [x['vlans'] for x in c.show() if x['name'] == str(name)][0]
    portsAfter = [x['ports'] for x in c.show() if x['name'] == str(name)][0]
    assert str(vlans) == vlansAfter
    assert str(ports) == portsAfter


def test_FailureAuthorizationdeleteVrgByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for deleteVrgByName with url http://%s/vRest/vrgs/name" % switch)
    response = requests.get("http://%s/vRest/vrgs/name" % switch)
    assert response.status_code == 401


def test_FailureAuthorizationshowVrgVrgClientsByVrgName(switch):
    """
           
    """
    vrg_name=testVrg % random.randint(0, 20000)
    pprint("testing Failed authentication  for showVrgVrgClientsByVrgName http://%s/vRest/vrgs/%s/clients" % (switch, vrg_name))
    response = requests.get("http://%s/vRest/vrgs/%s/clients" % (switch, vrg_name))
    assert response.status_code == 401


testdata = [  #
    (testVrg % random.randint(0, 20000))
]


@pytest.mark.parametrize("vrg_name", testdata)
def test_GETshowVrgVrgClientsByVrgName(switch, vrg_name):
    """
           
        """
    c = vrg(switch)
    c.createVrgForTesting(vrg_name)
    pprint("testing GET  for showVrgVrgClientsByVrgName http://%s/vRest/vrgs/%s/clients" % (switch, vrg_name))
    response = requests.get("http://%s/vRest/vrgs/%s/clients" % (switch, vrg_name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == str(vrg_name)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"


def test_FailureAuthorizationaddVrgPortByVrgName(switch):
    """
           
    """
    vrg_name=testVrg % random.randint(0, 20000)
    pprint("testing Failed authentication  for addVrgPortByVrgName http://%s/vRest/vrgs/%s/ports" % (switch,vrg_name))
    response = requests.get("http://%s/vRest/vrgs/%s/ports" % (switch,vrg_name))
    assert response.status_code == 401


testdata = [  # vlans,ports
    (testVrg % random.randint(0, 20000), random.randint(2, 4090), portsToAdd)
]


@pytest.mark.parametrize("vrg_name,vlans,portsToAdd", testdata)
def test_POSTaddVrgPortByVrgName(switch, vrg_name, vlans, portsToAdd):
    """
       
    """
    c = vrg(switch)
    c.createVrgForTesting(vrg_name)
    portsInUse = []
    [portsInUse.append(x['ports']) for x in c.show() if x['ports'] != u'none']
    puse = ','.join(portsInUse)
    pListUse = list(hyphen_range(puse))
    portsToAdd = randintWithExclude(0, 100, pListUse)
    pprint(portsToAdd)
    lPortsBefore = [hyphen_range(x['ports']) for x in c.show() if x['name'] == str(vrg_name)]
    pprint("testing POST  for addVrgPortByVrgName with url  %s  and payload  %s"%("http://%s/vRest/vrgs/%s/ports" % (switch, vrg_name) , json.dumps({'ports' : str(portsToAdd)})))
    response = requests.post("http://%s/vRest/vrgs/%s/ports" % (switch, vrg_name), auth=(username, password),data=json.dumps({'ports' : str(portsToAdd)}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == str(vrg_name)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    lPortsAfter = [x['ports'] for x in c.show() if x['name'] == str(vrg_name)][0]
    assert lPortsAfter ==  str(portsToAdd)

def test_FailureAuthorizationremoveVrgPortByNameByPmap(switch):
    """
           
    """
    vrg_name=testVrg % random.randint(0, 20000)
    pprint("testing Failed authentication  for removeVrgPortByNameByPmap with  http://%s/vRest/vrgs/%s/ports/%s" % (switch, vrg_name, portList))
    response = requests.get("http://%s/vRest/vrgs/%s/ports/%s" % (switch, vrg_name, portList))
    assert response.status_code == 401


testdata = [  #
    (testVrg % random.randint(0, 20000), portToRemove)
]


@pytest.mark.parametrize("vrg_name,ports", testdata)
def test_DELETEremoveVrgPortByNameByPmap(switch, vrg_name, ports):
    """
       
    """
    v = vrg(switch)
    v.createVrgForTesting(vrg_name)
    pprint("testing DELETE  for removeVrgPortByNameByPmap with  url http://%s/vRest/vrgs/%s/ports/%s" % (switch, vrg_name, ports))
    response = requests.delete("http://%s/vRest/vrgs/%s/ports/%s" % (switch, vrg_name, ports),
                               auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in v.show() if x['name'] == str(vrg_name)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    portsForVrg = [x['ports'] for x in v.show() if x['name'] == str(vrg_name)]
    assert ports not in portsForVrg


testdata = [  #
    (testVrg % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_DELETEdeleteVrgByName(switch, name):
    """

    """
    c = vrg(switch)
    c.createVrgForTesting(name)
    pprint("testing DELETE  for deleteVrgByName with url http://%s/vRest/vrgs/%s" % (switch, name))
    response = requests.delete("http://%s/vRest/vrgs/%s" % (switch, name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == str(name)])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert (len([x for x in c.show() if x['name'] == str(name)])) == 0


def  test_teardown(switch):
    v = vrg(switch)
    v.deleteAllVrgs()