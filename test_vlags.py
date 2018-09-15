import random
import sys

import pytest

sys.path.append(".")
import requests
import json

from vlag import vlag
from pprint import pprint
import logging


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg


username = "network-admin"
password = "test123"
testVlag = "restVlag-%d"


def test_setup(switch):
    v = vlag(switch)
    v.cleanupAllVlags()


def test_FailureAuthorizationcreateVlag(switch):
    """
           
        """
    pprint("testing Failed authentication  for createVlag ")
    response = requests.get("http://%s/vRest/vlags" % switch)
    assert response.status_code == 401


testdata = [  # failover_move_L2,name,lacp_mode,peer_switch,mode,lacp_timeout,port,peer_port
    (testVlag % random.randint(0, 200000), 'slow', 'active-standby', 16, 'active-standby', 'slow', 34, 34)
]


@pytest.mark.parametrize("name,failover_move_L2,lacp_mode,peer_switch,mode,lacp_timeout,port,peer_port",
                         testdata)
def test_POSTcreateVlag(switch, name, failover_move_L2, lacp_mode, peer_switch, mode, lacp_timeout, port, peer_port):
    """
       
    """
    c = vlag(switch)
    pprint("testing POST  for createVlag with  url %s  and payload %s  " % (
        "http://%s/vRest/vlags" % (switch), json.dumps({
            "name": name,
            "mode": mode,
            "port": port,
            "lacp-mode": "active",
            "lacp-timeout": "slow",
            "peer-port": peer_port,
            "failover-move-L2": "false"
        })))
    response = requests.post("http://%s/vRest/vlags" % (switch), auth=(username, password), data=json.dumps({
        "name": name,
        "mode": mode,
        "port": port,
        "lacp-mode": "active",
        "lacp-timeout": "slow",
        "peer-port": peer_port,
        "failover-move-L2": "false"
    }))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.show() if x['name'] == name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVLagByName(name)


def test_FailureAuthorizationshowVlags(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVlags ")
    response = requests.get("http://%s/vRest/vlags" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVlag % random.randint(0, 200000), 34, 34)
]


@pytest.mark.parametrize("name,port,peer_port", testdata)
def test_GETshowVlags(switch, name, port, peer_port):
    """
           
        """
    c = vlag(switch)
    c.createVlagForTesting(name, port, peer_port)
    pprint("testing GET  for showVlags with url   http://%s/vRest/vlags" % (switch))
    response = requests.get("http://%s/vRest/vlags" % (switch), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVLagByName(name)


def test_FailureAuthorizationshowVlagByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVlagByName with url http://%s/vRest/vlags/name" % switch)
    response = requests.get("http://%s/vRest/vlags/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVlag % random.randint(0, 20000), 34, 34)
]


@pytest.mark.parametrize("name,port,peer_port", testdata)
def test_GETshowVlagByName(switch, name, port, peer_port):
    """
           
        """
    c = vlag(switch)
    c.createVlagForTesting(name, port, peer_port)
    cliresponseHash = [x for x in c.show() if x['name'] == name]
    pprint(cliresponseHash)
    pprint("testing GET  for showVlagByName with  http://%s/vRest/vlags/%s" % (switch, name))
    response = requests.get("http://%s/vRest/vlags/%s" % (switch, name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    c.deleteVLagByName(name)


def test_FailureAuthorizationupdateVlagByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for updateVlagByName with url http://%s/vRest/vlags/name" % switch)
    response = requests.get("http://%s/vRest/vlags/name" % switch)
    assert response.status_code == 401


testdata = [  # failover_move_L2,lacp_timeout
    (testVlag % random.randint(0, 200000), 35, 35, 'false', 'slow')
]


@pytest.mark.parametrize("name,port,peer_port,failover_move_L2,lacp_timeout", testdata)
def test_PUTupdateVlagByName(switch, name, port, peer_port, failover_move_L2, lacp_timeout):
    """
       
    """
    c = vlag(switch)
    c.createVlagForTesting(name, 34, 34)
    cliresponseListOfHashBefore = [x for x in c.show() if x['name'] == name]
    pprint(cliresponseListOfHashBefore)
    pprint("testing PUT  for updateVlagByName with url %s  payload  %s " % ("http://%s/vRest/vlags/%s" % (switch, name),
                                                                            json.dumps({
                                                                                'failover-move-L2': failover_move_L2,
                                                                                'lacp-timeout': lacp_timeout})))
    response = requests.put("http://%s/vRest/vlags/%s" % (switch, name), auth=(username, password),
                            data=json.dumps({'failover-move-L2': failover_move_L2, 'lacp-timeout': lacp_timeout}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)
    c.deleteVLagByName(name)


def test_FailureAuthorizationdeleteVlagByName(switch):
    """
           
        """
    pprint("testing Failed authentication  for deleteVlagByName http://%s/vRest/vlags/name" % switch)
    response = requests.get("http://%s/vRest/vlags/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVlag % random.randint(0, 200000), 34, 34)
]


@pytest.mark.parametrize("name,port,peer_port", testdata)
def test_DELETEdeleteVlagByName(switch, name, port, peer_port):
    """
       
    """
    c = vlag(switch)
    c.createVlagForTesting(name, port, peer_port)
    cliresponseListOfHashBefore = [x for x in c.show() if x['name'] == name]
    pprint(cliresponseListOfHashBefore)
    pprint("testing DELETE  for deleteVlagByName with url   http://%s/vRest/vlags/%s" % (switch, name))
    response = requests.delete("http://%s/vRest/vlags/%s" % (switch, name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliHash = [x for x in c.show() if x['name'] == name]
    assert len(cliHash) == 0


def test_teardown(switch):
    v = vlag(switch)
    v.cleanupAllVlags()

