import sys
from datetime import datetime
import pytest

sys.path.append(".")
import requests
import json
import random
from vlan import vlan
from ParserUtils import hyphen_range
from pprint import pprint
import logging


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg


username = "network-admin"
password = "test123"
descVlan = "desc-%d"
portList = "20,21,22,23,24,25.26.27.28.29,30"
portsToDelete = "20,21,22"
portsToAdd = "30,31,32"


def test_setup(switch):
    v = vlan(switch)
    v.cleanupVlans()


def test_FailureAuthorizationcreateVlan(switch):
    """
           
        """
    pprint("testing Failed authentication  for createVlan with http://%s/vRest/vlans" % switch)
    response = requests.get("http://%s/vRest/vlans" % switch)
    assert response.status_code == 401


testdata = [
    (90000, "local", "20,21,22,23,24,25", "Value 90000 out of range for field ident."),
    (23, "", "20,21,22,23,24,25", "Invalid value for scope."),
    (23, "fabric", "9999",
     "The value 9999 is invalid. Value should be a comma delimited list of ports or port ranges such as 22,33,40-42,45. Port value should be between 0 and 255."),
]


@pytest.mark.parametrize("id,scope,ports,message", testdata)
def test_POSTcreateVlanErrorMessages(switch, id, scope, ports, message):
    """
       
    """
    c = vlan(switch)
    description = descVlan % id
    pprint("testing POST  for createVlan with  url %s  payload  %s" % ("http://%s/vRest/vlans" % (switch), json.dumps(
            {'description': description, 'id': id, 'scope': scope, 'ports': ports})))
    response = requests.post("http://%s/vRest/vlans" % (switch), auth=(username, password),
                             data=json.dumps({'description': description, 'id': id, 'scope': scope, 'ports': ports}))
    pprint("==========JSON Response for  Error==========")
    pprint(response.json())
    pprint("====================")
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0


testdata = [  # id,scope,ports
    (random.randint(4, 4000), "local", "20,21,22,23,24,25")
]


@pytest.mark.parametrize("id,scope,ports", testdata)
def test_POSTcreateVlan(switch, id, scope, ports):
    """

    """
    c = vlan(switch)
    description = descVlan % id
    pprint("testing POST  for createVlan with url %s payload  %s  " % ("http://%s/vRest/vlans" % (switch), json.dumps(
            {'description': description, 'id': id, 'scope': scope, 'ports': ports})))
    response = requests.post("http://%s/vRest/vlans" % (switch), auth=(username, password),
                             data=json.dumps({'description': description, 'id': id, 'scope': scope, 'ports': ports}))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliCreated = [x for x in c.show() if x[u'id'] == str(id)]
    assert cliCreated[0]['id'] == str(id)
    assert cliCreated[0]['description'] == str(description)


def test_FailureAuthorizationshowVlans(switch):
    """
           
    """
    pprint("testing Failed authentication  for showVlans with url http://%s/vRest/vlans" % switch)
    response = requests.get("http://%s/vRest/vlans" % switch)
    assert response.status_code == 401


def test_GETshowVlans(switch):
    """
           
    """
    c = vlan(switch)
    c.createVlanForTesting(random.randint(4, 4000))
    pprint("testing GET  for showVlans with url   http://%s/vRest/vlans" % (switch))
    response = requests.get("http://%s/vRest/vlans" % (switch), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    vlanList = [x['id'] for x in c.show()]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint("=========JSON Output================")
    pprint(jsonResponseDat)
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint(c.show())
    pprint("=========================")
    vlanListFromREST = [x['id'] for x in jsonResponseDat]
    pprint(vlanListFromREST)
    pprint(vlanList)
    pprint("=========DIFF================")
    assert len(vlanList) == len(vlanListFromREST)


def test_FailureAuthorizationshowVlanByIdent(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVlanByIdent with url  http://%s/vRest/vlans/{id}" % switch)
    response = requests.get("http://%s/vRest/vlans/id" % switch)
    assert response.status_code == 401


testdata = [  #
    (random.randint(4, 4000))
]


@pytest.mark.parametrize("id", testdata)
def test_GETshowVlanByIdent(switch, id):
    """
           
    """
    c = vlan(switch)
    c.createVlanForTesting(id)
    pprint("testing GET  for showVlanByIdent with url  http://%s/vRest/vlans/id/%s" % (switch, id))
    response = requests.get("http://%s/vRest/vlans/id/%s" % (switch, id), auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResponseDat = json.loads(response.text)["data"]
    pprint("=========JSON Output================")
    pprint(jsonResponseDat)
    pprint("=========================")
    pprint("=========CLI Output================")
    pprint([x for x in c.show() if x['id'] == id])
    pprint("=========================")
    descCLI = [x['description'] for x in c.show() if x['id'] == str(id)][0]
    descREST = [x['description'] for x in json.loads(response.text)["data"]][0]
    assert descCLI == descREST


testdata = [
    (-100, "Value -100 out of range for field ident."),
    (6000, "value 6000 for id out of range. id must be between 0 and 4095.")
]


@pytest.mark.parametrize("id,message", testdata)
def test_GETshowVlanByIdentErrorMessages(switch, id, message):
    """

    """
    c = vlan(switch)
    response = requests.get("http://%s/vRest/vlans/id/%s" % (switch, id), auth=(username, password))
    pprint("==========JSON Response for  Error==========")
    pprint(response.json())
    pprint("====================")
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0


def test_FailureAuthorizationupdateVlanByIdent(switch):
    """
           
        """
    pprint("testing Failed authentication  for updateVlanByIdent ")
    response = requests.get("http://%s/vRest/vlans/{id}" % switch)
    assert response.status_code == 401


testdata = [  # description
    (random.randint(4, 4000), u'automation-%d' % random.randint(3,100000) )
]


@pytest.mark.parametrize("id,description", testdata)
def test_PUTupdateVlanByIdent(switch, id, description):
    """
       
    """
    c = vlan(switch)
    c.createVlanForTesting(id)
    descriptionBefore = [x['description'] for x in c.show() if x['id'] == str(id)]
    pprint("testing PUT  for updateVlanByIdent  with url %s payload %s " % (
        "http://%s/vRest/vlans/%s" % (switch, id), json.dumps({u'description': description})))
    response = requests.put("http://%s/vRest/vlans/id=%s,vnet-id=api.null" % (switch, id), auth=(username, password),
                            data=json.dumps({u'description': description}))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    descriptionAfter = [x['description'] for x in c.show() if x['id'] == str(id)][0]
    assert description == descriptionAfter


testdata = [  # description
    (23, "", "Illegal value for description. Legal values are: letters, numbers, _, ., :, spaces, and -"),
    (23, "xxxxxxxxx" * 100, "description cannot exceed 59 characters")
]


@pytest.mark.parametrize("id,description,message", testdata)
def test_PUTupdateVlanByIdentErrorMessages(switch, id, description, message):
    """

    """
    response = requests.put("http://%s/vRest/vlans/id=%s,vnet-id=api.null" % (switch, id), auth=(username, password),
                            data=json.dumps({u'description': description}))
    pprint("==========JSON Response for  Error==========")
    pprint(response.json())
    pprint("====================")
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0


def test_FailureAuthorizationdeleteVlanByIdent(switch):
    """
           
        """
    pprint("testing Failed authentication  for deleteVlanByIdent ")
    response = requests.get("http://%s/vRest/vlans/{id}" % switch)
    assert response.status_code == 401


testdata = [  #
    (random.randint(4, 4000))
]


def test_FailureAuthorizationaddVlanVlanPortByVlanIdent(switch):
    """
           
    """
    pprint("testing Failed authentication  for addVlanVlanPortByVlanIdent ")
    response = requests.get("http://%s/vRest/vlans/%d/ports" % (switch, random.randint(4, 4000)))
    assert response.status_code == 401


testdata = [  # scope,portsToAdd,id
    ('local', portsToAdd, random.randint(4, 4000))
]


@pytest.mark.parametrize("scope,portsToAdd,vlan_id", testdata)
def test_POSTaddVlanVlanPortByVlanIdent(switch, scope, portsToAdd, vlan_id):
    """
       
    """
    c = vlan(switch)
    description = descVlan % vlan_id
    c.createVlanForTestingWithPorts(vlan_id, portsToAdd)
    lPortsBefore = [hyphen_range(x['ports']) for x in c.show() if x['id'] == str(id)]
    pprint("testing POST  for addVlanVlanPortByVlanIdent with url  %s  payload  %s  " % (
        "http://%s/vRest/vlans/id=%s,vnet-id=api.null/ports" % (switch, vlan_id), json.dumps({u'ports': portsToAdd})))
    response = requests.post("http://%s/vRest/vlans/id=%s,vnet-id=api.null/ports" % (switch, vlan_id), auth=(username, password),
                             data=json.dumps({u'ports': portsToAdd}))
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    lPortsAfter = [hyphen_range(x['ports']) for x in c.show() if x['id'] == str(id)]
    pprint(lPortsAfter)
    pprint(lPortsBefore)


testdata = [  # scope,portsToAdd,id
    ('local', "", 100, "Ports added")
]


@pytest.mark.parametrize("scope,portsToAdd,vlan_id,message", testdata)
def test_POSTaddVlanVlanPortByVlanIdentErrorMessages(switch, scope, portsToAdd, vlan_id, message):
    """

    """
    c = vlan(switch)
    description = descVlan % vlan_id
    c.createVlanForTestingWithPorts(vlan_id, portsToAdd)
    lPortsBefore = [hyphen_range(x['ports']) for x in c.show() if x['id'] == str(id)]
    pprint("testing POST  for addVlanVlanPortByVlanIdent url  %s  payload  %s   " % (
        "http://%s/vRest/vlans/id=%s,vnet-id=api.null/ports" % (switch, vlan_id), json.dumps({u'ports': portsToAdd})))
    response = requests.post("http://%s/vRest/vlans/id=%s,vnet-id=api.null/ports" % (switch, vlan_id), auth=(username, password),
                             data=json.dumps({u'ports': portsToAdd}))
    pprint("==========JSON Response for  Error==========")
    pprint(response.json())
    pprint("====================")
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message


def test_FailureAuthorizationremoveVlanVlanPortByIdentByPmap(switch):
    """
           
        """
    pprint("testing Failed authentication  for removeVlanVlanPortByIdentByPmap ")
    response = requests.get("http://%s/vRest/vlans/{vlan-id}/ports/{ports}" % switch)
    assert response.status_code == 401


testdata = [
    (10, -98,
     "The value -98 is invalid. Value should be a comma delimited list of ports or port ranges such as 22,33,40-42,45. Port value should be between 0 and 255."),
    (10, 2000,
     "The value 2000 is invalid. Value should be a comma delimited list of ports or port ranges such as 22,33,40-42,45. Port value should be between 0 and 255.")
]


@pytest.mark.parametrize("id,ports,message", testdata)
def test_DELETEremoveVlanVlanPortByIdentByPmapErrorMessages(switch, id, ports, message):
    """

    """
    c = vlan(switch)
    c.createVlanForTesting(id)
    response = requests.delete("http://%s/vRest/vlans/id=%s,vnet-id=api.null/ports/%s" % (switch, id, ports),
                               auth=(username, password))
    pprint("==========JSON Response for  Error==========")
    pprint(response.json())
    pprint("====================")
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0


testdata = [  #
    (random.randint(4, 4000), portsToDelete)
]


@pytest.mark.parametrize("vlan_id,ports", testdata)
def test_DELETEremoveVlanVlanPortByIdentByPmap(switch, vlan_id, ports):
    """
       
    """
    v = vlan(switch)
    v.createVlanForTestingWithPorts(vlan_id, ports)
    pprint("testing DELETE  for removeVlanVlanPortByIdentByPmap with url http://%s/vRest/vlans/id=%s,vnet-id=api.null/ports/%s" % (
        switch, vlan_id, ports))
    response = requests.delete("http://%s/vRest/vlans/id=%s,vnet-id=api.null/ports/%s" % (switch, vlan_id, ports),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    portsForVlan = [x['ports'] for x in v.show() if x['id'] == str(id)]
    assert ports not in portsForVlan


testdata = [
    (random.randint(4, 4000))
]


@pytest.mark.parametrize("id", testdata)
def test_DELETEdeleteVlanByIdent(switch, id):
    """

    """
    c = vlan(switch)
    c.createVlanForTesting(id)
    pprint("testing DELETE  for deleteVlanByIdent with url  http://%s/vRest/vlans/id/%d" % (switch, id))
    response = requests.delete("http://%s/vRest/vlans/id/%d" % (switch, id), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert (len([x for x in c.show() if x['id'] == str(id)])) == 0


testdata = [
    (-100, "Value -100 out of range for field ident."),
    (6000, "value 6000 for id out of range. id must be between 0 and 4095.")
]


@pytest.mark.parametrize("id,message", testdata)
def test_DELETEdeleteVlanByIdentErrorMessages(switch, id, message):
    """

    """
    response = requests.delete("http://%s/vRest/vlans/id/%d" % (switch, id), auth=(username, password))
    pprint("==========JSON Response for  Error==========")
    pprint(response.json())
    pprint("====================")
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0
