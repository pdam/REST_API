import random
import sys

import pytest

from fabric_node import fabric_node
from vnet import vnet

sys.path.append(".")
import requests
import json

from vrouter import vrouter
from pprint import pprint

from vlan import vlan
username = "network-admin"
password = "test123"
testVRouter = "restVrouter-%d"
testVNet = "restVNet-%d"
testNetwork = "172.16.23.%d"
testNetworkGatewayIp = "172.16.23.1"
testGatewayIp = "172.16.%d.1"
testGroupIp = "224.0.%d.1"
testSourceIp = "172.16.%d.1"
testBGPIp = "192.168.%d.1"
testNeighBourIP = "209.75.%d.3"
testInterface = "eth0.%d"
testInterfaceIP = "172.16.%d.1"
testVRouterIP = "172.16.%d.1"
testPrefixname = "testPrefix-%d"
testPrefixIP = "172.16.%d.12"
testPrefixNetwork = "172.16.%d.1"
testRPAdddress = "172.16.%d.1"
testIGMPGRoupName = "restIGMPGroup-%d"
testMulticastIP = "224.0.%d.23"


def test_setup(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()


def test_FailureAuthorizationcreateVrouter(switch):
    """

        """
    pprint("testing Failed authentication  for createVrouter with url  http://%s/vRest/vrouters" % switch)
    response = requests.get("http://%s/vRest/vrouters" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVNet % random.randint(0, 20), 'hardware', testVRouter % random.randint(2, 200000))
]


@pytest.mark.parametrize("vnet_name,router_type,vrouter_name", testdata)
def test_POSTcreateVrouter(switch, vnet_name, router_type, vrouter_name):
    """

    """
    c = vrouter(switch)
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)

    payload = {
        "name": vrouter_name,
        "vnet": vnet_name,
        "router-type": router_type

    }
    pprint("testing POST  for createVrouter with  url %s  and  payload  %s  " % (
        "http://%s/vRest/vrouters" % (switch), payload))
    response = requests.post("http://%s/vRest/vrouters" % (switch), auth=(username, password), data=json.dumps(payload))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == vrouter_name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouters(switch):
    """

        """
    pprint("testing Failed authentication  for showVrouters ")
    response = requests.get("http://%s/vRest/vrouters" % switch)
    assert response.status_code == 401


def test_GETshowVrouters(switch):
    """

        """
    c = vrouter(switch)
    vrouter_name, vnet_name = testVRouter % random.randint(0, 20000), testVNet % random.randint(0, 20000)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    pprint("testing GET  for showVrouters ")
    response = requests.get("http://%s/vRest/vrouters" % (switch), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResponseDat = json.loads(response.text)["data"]
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in c.show() if x['name'] == vrouter_name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterByVnmName(switch):
    """

    """
    pprint("testing Failed authentication  for showVrouterByVnmName with url  http://%s/vRest/vrouters/name" % switch)
    response = requests.get("http://%s/vRest/vrouters/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("name,vnet_name", testdata)
def test_GETshowVrouterByVnmName(switch, name, vnet_name):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(name, vnet_name)
    pprint("testing GET  for showVrouterByVnmName  with url  http://%s/vRest/vrouters/%s" % (switch, name))
    response = requests.get("http://%s/vRest/vrouters/%s" % (switch, name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationupdateVrouterByVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for updateVrouterByVnmName with  url  http://%s/vRest/vrouters/name" % switch)
    response = requests.get("http://%s/vRest/vrouters/name" % switch)
    assert response.status_code == 401


testdata = [  # max_prefix_len,min_prefix_len,prefix,netmask,action,any
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000), 'enable', 10, 'pim-sparse',
     testVRouterIP % random.randint(3, 200))
]


@pytest.mark.parametrize("name,vnet_name, state,bgp_as,proto_multi,router_id", testdata)
def test_PUTupdateVrouterByVnmName(switch, name, vnet_name, state, bgp_as, proto_multi, router_id):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(name, vnet_name)
    cliresponseListOfHashBefore = c.show()
    payload = {
        "state": state,
        "bgp-as": bgp_as,
        "proto-multi": proto_multi,
        "router-id": router_id
    }
    response = requests.put("http://%s/vRest/vrouters/%s" % (switch, name), auth=(username, password),
                            data=json.dumps(payload))
    pprint("testing PUT  for updateVrouterByVnmName with  url %s   payload  %s " % (
        "http://%s/vRest/vrouters/%s" % (switch, name), payload))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationdeleteVrouterByVnmName(switch):
    """

        """
    pprint("testing Failed authentication  for deleteVrouterByVnmName with url  http://%s/vRest/vrouters/name" % switch)
    response = requests.get("http://%s/vRest/vrouters/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("name,vnet_name", testdata)
def test_DELETEdeleteVrouterByVnmName(switch, name, vnet_name):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(name, vnet_name)
    pprint("testing DELETE  for deleteVrouterByVnmName with url http://%s/vRest/vrouters/%s" % (switch, name))
    response = requests.delete("http://%s/vRest/vrouters/%s" % (switch, name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp = [x for x in c.show() if x['name'] == name]
    assert len(cliResp) == 0
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationaddVrouterStaticRouteByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterStaticRouteByVrouterVnmName with  url  http://%s/vRest/vrouters/vrouter-name/static-routes" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/static-routes" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouterIP % random.randint(3, 200),
     testGatewayIp % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,gateway_ip,router_ip", testdata)
def test_POSTaddVrouterStaticRouteByVrouterVnmName(switch, vrouter_name, vnet_name, gateway_ip, router_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    cliresponseListOfHashBefore = c.show()
    payload = {
        "netmask": 24,
        "network": router_ip,
        "distance": 10,
        "gateway-ip": gateway_ip
    }
    pprint("testing POST  for addVrouterStaticRouteByVrouterVnmName with url  %s and  payload  %s" % (
        "http://%s/vRest/vrouters/%s/static-routes" % (switch, vrouter_name), payload))
    response = requests.post("http://%s/vRest/vrouters/%s/static-routes" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps(payload))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterStaticRoutesByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterStaticRoutesByVrouterVnmName with  url http://%s/vRest/vrouters/vrouter-name/static-routes" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/static-routes" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouterIP % random.randint(3, 200), 24, testGatewayIp % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,network,netmask,gateway_ip", testdata)
def test_GETshowVrouterStaticRoutesByVrouterVnmName(switch, vrouter_name, vnet_name, network, netmask, gateway_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addStaticRoute(vrouter_name, network, netmask, gateway_ip)
    pprint(
            "testing GET  for showVrouterStaticRoutesByVrouterVnmName with  url http://%s/vRest/vrouters/%s/static-routes" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/static-routes" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showStaticRoutes()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterStaticRoutesByVnmNameUniqueKeyAll(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterStaticRoutesByVnmNameUniqueKeyAll with url http://%s/vRest/vrouters/vrouter-name/static-routes/network=network,netmask=netmask,gateway-ip=gateway-ip" % switch)
    response = requests.get(
            "http://%s/vRest/vrouters/vrouter-name/static-routes/network=network,netmask=netmask,gateway-ip=gateway-ip,interface=api.null" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouterIP % random.randint(3, 200), 24,
     testGatewayIp % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,network,netmask,gateway_ip", testdata)
def test_GETshowVrouterStaticRoutesByVnmNameUniqueKeyAll(switch, vrouter_name, vnet_name, network, netmask, gateway_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addStaticRoute(vrouter_name, network, netmask, gateway_ip)
    url = "http://%s/vRest/vrouters/%s/static-routes/network=%s,netmask=%s,gateway-ip=%s,interface=api.null" % (
        switch, vrouter_name, network, netmask, gateway_ip)
    pprint("testing GET  for showVrouterStaticRoutesByVnmNameUniqueKeyAll with url  %s" % url)
    response = requests.get(url, auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showStaticRoutes()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationremoveVrouterStaticRouteByVnmNameUniqueKeyAll(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterStaticRouteByVnmNameUniqueKeyAll for  url  http://%s/vRest/vrouters/vrouter-name/static-routes/network=network,netmask=netmask,gateway-ip=gateway-ip" % switch)
    response = requests.get(
            "http://%s/vRest/vrouters/vrouter-name/static-routes/network=network,netmask=netmask,gateway-ip=gateway-ip,interface=api.null" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200),
        24,
        testNetworkGatewayIp)
]


@pytest.mark.parametrize("vrouter_name,vnet_name,network,netmask,gateway_ip", testdata)
def test_DELETEremoveVrouterStaticRouteByVnmNameUniqueKeyAll(switch, vrouter_name, vnet_name, network, netmask,
                                                             gateway_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addStaticRoute(vrouter_name, network, netmask, gateway_ip)
    pprint(
            "testing DELETE  for removeVrouterStaticRouteByVnmNameUniqueKeyAll with url http://%s/vRest/vrouters/%s/static-routes/network=%s,netmask=%s,gateway-ip=%s,interface=api.null" % (
                switch, vrouter_name, "%s.%s" % (".".join(network.split(".")[0:3]), "0"), netmask, gateway_ip))
    response = requests.delete(
            "http://%s/vRest/vrouters/%s/static-routes/network=%s,netmask=%s,gateway-ip=%s,interface=api.null" % (
                switch, vrouter_name, "%s.%s" % (".".join(network.split(".")[0:3]), "0"), netmask, gateway_ip),
            auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showStaticRoutes() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    assert len(cliresponseListOfHashAfter) == 0
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterIpRoutesByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterIpRoutesByVrouterVnmName with url http://%s/vRest/vrouters/vrouter-name/routes" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/routes" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterIpRoutesByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addInterfaceToAVRouter(vrouter_name,"172.16.12.23")
    ##Add  a   static route
    response = requests.post("http://%s/vRest/vrouters/%s/routes" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({ "network" :  "1.2.3.4" , "netmask" : 24 ,  "gateway-ip" :  "172.16.12.1"})
                             )
    ## Check route
    pprint("testing GET  for showVrouterIpRoutesByVrouterVnmName with url http://%s/vRest/vrouters/%s/routes" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/routes" % (switch, vrouter_name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterIpRouteByVnmNameByNetwork(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterIpRouteByVnmNameByNetwork with url http://%s/vRest/vrouters/vrouter-name/routes/network" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/routes/network" % switch)
    assert response.status_code == 401


def test_FailureAuthorizationshowVrouterIpMroutesByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterIpMroutesByVrouterVnmName with url http://%s/vRest/vrouters/vrouter-name/multicast-routes" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/multicast-routes" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testMulticastIP % random.randint(3, 200), testMulticastIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,multicast_ip,multicast_ip2", testdata)
def test_GETshowVrouterIpMroutesByVrouterVnmName(switch, vrouter_name, vnet_name, multicast_ip, multicast_ip2):
    """

        """
    c = vrouter(switch)
    c.createVRouterForOSPFTesting(vrouter_name, vnet_name)
    pprint(
            "testing GET  for showVrouterIpMroutesByVrouterVnmName with url  http://%s/vRest/vrouters/%s/multicast-routes" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/multicast-routes" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showRoutesMultiCast()
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterIpMrouteByVnmNameBySource(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterIpMrouteByVnmNameBySource   with url   http://%s/vRest/vrouters/vrouter-name/multicast-routes/source" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/multicast-routes/source" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testSourceIp % random.randint(3, 200))
]


def test_FailureAuthorizationshowVrouterBgpNeighborsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterBgpNeighborsByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/bgp-neighbors" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/bgp-neighbors" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000), random.randint(4, 4000),
     testBGPIp % random.randint(3, 200),
     testNeighBourIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name1,vnet_name1,vrouter_name2,vnet_name2,vlan,vrouter_ip,neighbor", testdata)
def test_POSTresetVrouterBgpNeighborByVrouterVnmName(switch, vrouter_name1, vnet_name1, vrouter_name2, vnet_name2, vlan,
                                                     vrouter_ip, neighbor):
    """

    """
    f = fabric_node(switch)
    lSwitches = [x['name']  for x  in f.getFabricSwitches() ]
    switch1,switch2 = lSwitches

    c = vrouter(switch1)
    c.createVRouterForTestingWithBGPServiceNeighbour(vrouter_name1, vnet_name1, "50.1.1.2", vlan, "50.1.1.0",True)
    c = vrouter(switch2)
    c.createVRouterForTestingWithBGPServiceNeighbour(vrouter_name2, vnet_name2, "50.1.1.3", vlan, "50.1.1.0",False)

    pprint("testing POST  for resetVrouterBgpNeighborByVrouterVnmName with url  %s and payload %s" % (
        "http://%s/vRest/vrouters/%s/bgp-neighbors/reset" % (switch, vrouter_name1),
        json.dumps({'neighbour': "50.1.1.0"})))
    response = requests.post("http://%s/vRest/vrouters/%s/bgp-neighbors/reset" % (switch, vrouter_name1),
                             auth=(username, password), data=json.dumps({'neighbor': "50.1.1.0"}))
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name1)
    c.deleteVnetAssociatedWithVrouter(vnet_name2)


def test_FailureAuthorizationshowVrouterBgpNeighborByVnmNameByNeighbor(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterBgpNeighborByVnmNameByNeighbor  with url  http://%s/vRest/vrouters/vrouter-name/bgp-neighbors/neighbor" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/bgp-neighbors/neighbor" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000), random.randint(4, 4000),
     testBGPIp % random.randint(3, 200),
     testNeighBourIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name1,vnet_name1,vrouter_name2,vnet_name2,vlan,vrouter_ip,neighbor", testdata)
def test_GETshowVrouterBgpNeighborByVnmNameByNeighbor(switch, vrouter_name1, vnet_name1, vrouter_name2, vnet_name2,
                                                      vlan, vrouter_ip, neighbor):
    """

    """
    f = fabric_node(switch)
    lSwitches = [x['name']  for x  in f.getFabricSwitches() ]
    switch1,switch2 = lSwitches
    c = vrouter(switch1)
    c.createVRouterForTestingWithBGPServiceNeighbour(vrouter_name1, vnet_name1, "50.1.1.2", 100, "50.1.1.0",True)
    c = vrouter(switch2)
    c.createVRouterForTestingWithBGPServiceNeighbour(vrouter_name2, vnet_name2, "50.1.1.3", 100, "50.1.1.0",False)
    pprint(
            "testing GET  for showVrouterBgpNeighborByVnmNameByNeighbor with url  http://%s/vRest/vrouters/%s/bgp-neighbors/%s" % (
                switch, vrouter_name1, "50.1.1.0"))
    response = requests.get("http://%s/vRest/vrouters/%s/bgp-neighbors/%s" % (switch, vrouter_name1, "50.1.1.0"),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showVRouterBGP() if
                       x['vrouter-name'] == vrouter_name1 or x['vrouter-name'] == vrouter_name2]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name1)
    c.deleteVnetAssociatedWithVrouter(vnet_name2)
    c.close()


def test_FailureAuthorizationaddVrouterOspfByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterOspfByVrouterVnmName with url   http://%s/vRest/vrouters/vrouter-name/ospfs" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospfs" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouterIP % random.randint(0, 20))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_POSTaddVrouterOspfByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTestingWithID(vrouter_name, vnet_name, interface_ip)
    pprint("testing POST  for addVrouterOspfByVrouterVnmName  with url %s  and payload  %s " % (
        "http://%s/vRest/vrouters/%s/ospfs" % (switch, vrouter_name), json.dumps({
            "netmask": 24,
            "network": interface_ip,
            "ospf-area": 0
        })))
    response = requests.post("http://%s/vRest/vrouters/%s/ospfs" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({
                                 "netmask": 24,
                                 "network": interface_ip,
                                 "ospf-area": 0
                             }))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterOspfsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspfsByVrouterVnmName with url http://%s/vRest/vrouters/vrouter-name/ospfs" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospfs" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterOspfsByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createVRouterForOSPFTesting(vrouter_name, vnet_name)
    cliHash = [x for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name]
    pprint(cliHash)
    pprint("testing GET  for showVrouterOspfsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/ospfs" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/ospfs" % (switch, vrouter_name), auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterOspfByVnmNameByNetwork(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspfByVnmNameByNetwork with url   http://%s/vRest/vrouters/vrouter-name/ospfs/network" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospfs/network" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterOspfByVnmNameByNetwork(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createVRouterForOSPFTesting(vrouter_name, vnet_name)
    network = [x['network'] for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name][0]
    pprint(network)
    pprint("testing GET  for showVrouterOspfByVnmNameByNetwork with url   http://%s/vRest/vrouters/%s/ospfs/%s" % (
        switch, vrouter_name, network))
    response = requests.get("http://%s/vRest/vrouters/%s/ospfs/%s" % (switch, vrouter_name, network),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name][0]

    jsonResponseDat = json.loads(response.text)["data"]
    pprint("========================JSON =====================")
    pprint(jsonResponseDat)
    pprint("========================CLI =====================")
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationremoveVrouterOspfByVnmNameByNetwork(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterOspfByVnmNameByNetwork with url  http://%s/vRest/vrouters/vrouter-name/ospfs/network" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospfs/network" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_DELETEremoveVrouterOspfByVnmNameByNetwork(switch, vrouter_name, vnet_name):
    """

    """
    c = vrouter(switch)
    c.createVRouterForOSPFTesting(vrouter_name, vnet_name)
    network = [x['network'] for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name][0]
    pprint(network)
    pprint("testing DELETE  for removeVrouterOspfByVnmNameByNetwork with url  http://%s/vRest/vrouters/%s/ospfs/%s" % (
        switch, vrouter_name, network))
    response = requests.delete("http://%s/vRest/vrouters/%s/ospfs/%s" % (switch, vrouter_name, network),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name]
    assert len(cliresponseListOfHashAfter) == 0
    c.close()


def test_FailureAuthorizationaddVrouterOspf6ByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterOspf6ByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/ospf6s" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf6s" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testVRouterIP % random.randint(2, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_POSTaddVrouterOspf6ByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic=c.addInterfaceToAVRouter(vrouter_name,interface_ip)
    pprint("testing POST  for addVrouterOspf6ByVrouterVnmName with url %s  payload  %s" % (
        "http://%s/vRest/vrouters/%s/ospf6s" % (switch, vrouter_name), json.dumps({
            "nic": nic,
            "ospf6-area": "0"
        })))
    response = requests.post("http://%s/vRest/vrouters/%s/ospf6s" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({
                                 "nic": nic,
                                 "ospf6-area": "0"
                             }))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showOSPF6Routers()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterOspf6sByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspf6sByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/ospf6s" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf6s" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterOspf6sByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name,"172.16.23.44")
    response = requests.post("http://%s/vRest/vrouters/%s/ospf6s" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({
                                 "nic": nic,
                                 "ospf6-area": "0"
                             }))
    pprint(response.json())
    pprint("testing GET  for showVrouterOspf6sByVrouterVnmName with url  http://%s/vRest/vrouters/%s/ospf6s" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/ospf6s" % (switch, vrouter_name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showOSPF6Routers()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterOspf6ByVnmNameByVnic(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspf6ByVnmNameByVnic with url  http://%s/vRest/vrouters/vrouter-name/ospf6s/nic" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf6s/nic" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterOspf6ByVnmNameByVnic(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic=c.addInterfaceToAVRouter(vrouter_name,"172.16.22.33")
    response = requests.post("http://%s/vRest/vrouters/%s/ospf6s" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({
                                 "nic": nic,
                                 "ospf6-area": "0"
                             }))
    pprint(response.json())
    pprint("testing GET  for showVrouterOspf6ByVnmNameByVnic with url http://%s/vRest/vrouters/%s/ospf6s/%s" % (
        switch, vrouter_name, nic))
    response = requests.get("http://%s/vRest/vrouters/%s/ospf6s/%s" % (switch, vrouter_name, nic),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationremoveVrouterOspf6ByVnmNameByVnic(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterOspf6ByVnmNameByVnic with url  http://%s/vRest/vrouters/vrouter-name/ospf6s/nic" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf6s/nic" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_DELETEremoveVrouterOspf6ByVnmNameByVnic(switch, vrouter_name, vnet_name):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic=c.addInterfaceToAVRouter(vrouter_name,"172.16.22.33")
    response = requests.post("http://%s/vRest/vrouters/%s/ospf6s" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({
                                 "nic": nic,
                                 "ospf6-area": "0"
                             }))
    pprint(response.json())
    pprint("testing DELETE  for removeVrouterOspf6ByVnmNameByVnic  with url  http://%s/vRest/vrouters/%s/ospf6s/%s" % (
        switch, vrouter_name, nic))
    response = requests.delete("http://%s/vRest/vrouters/%s/ospf6s/%s" % (switch, vrouter_name, nic),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showOSPF6Routers()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationaddVrouterOspfAreaByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterOspfAreaByVrouterVnmName for  url  http://%s/vRest/vrouters/vrouter-name/ospf-areas" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf-areas" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_POSTaddVrouterOspfAreaByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

    """
    c = vrouter(switch)
    c.createVRouterForOSPFTesting(vrouter_name, vnet_name)
    pprint("testing POST  for addVrouterOspfAreaByVrouterVnmName with url  %s  payload  %s" % (
        "http://%s/vRest/vrouters/%s/ospf-areas" % (switch, vrouter_name), json.dumps({
            "area": 1000,
            "stub-type": "nssa"
        })))
    response = requests.post("http://%s/vRest/vrouters/%s/ospf-areas" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps({
            "area": 1000,
            "stub-type": "nssa"
        }))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showOSPFRouters()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterOspfAreasByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspfAreasByVrouterVnmName with url  http://%s/vRest/vrouters/{vrouter-name}/ospf-areas" % switch)
    response = requests.get("http://%s/vRest/vrouters/{vrouter-name}/ospf-areas" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterOspfAreasByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createVRouterForOSPFTesting(vrouter_name, vnet_name)
    response = requests.post("http://%s/vRest/vrouters/%s/ospf-areas" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps({
            "area": 1000,
            "stub-type": "nssa"
        }))
    pprint(response.json())
    assert str(response.status_code) == "201"
    pprint("testing GET  for showVrouterOspfAreasByVrouterVnmName with  url  http://%s/vRest/vrouters/%s/ospf-areas" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/ospf-areas" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterOspfAreaByVnmNameByArea(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspfAreaByVnmNameByArea with url  http://%s/vRest/vrouters/{vrouter-name}/ospf-areas/{area}" % switch)
    response = requests.get("http://%s/vRest/vrouters/{vrouter-name}/ospf-areas/{area}" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000), 10, "stub")
]


@pytest.mark.parametrize("vrouter_name,vnet_name,area,stub_type", testdata)
def test_GETshowVrouterOspfAreaByVnmNameByArea(switch, vrouter_name, vnet_name, area, stub_type):
    """

    """
    c = vrouter(switch)
    c.createOSPFAreaForVrouter(vrouter_name, vnet_name, area, stub_type)
    cliHash = [x for x in c.showOSPFAreaForVRouters() if x['vrouter-name'] == vrouter_name]
    pprint(cliHash)
    pprint("testing GET  for showVrouterOspfAreaByVnmNameByArea with url  http://%s/vRest/vrouters/%s/ospf-areas/%s" % (
        switch, vrouter_name, area))
    response = requests.get("http://%s/vRest/vrouters/%s/ospf-areas/%s" % (switch, vrouter_name, area),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showOSPFAreaForVRouters() if x['vrouter-name'] == vrouter_name]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationupdateVrouterOspfAreaByVnmNameByArea(switch):
    """

        """
    pprint(
            "testing Failed authentication  for updateVrouterOspfAreaByVnmNameByArea with url  http://%s/vRest/vrouters/vrouter-name/ospf-areas/area" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf-areas/area" % switch)
    assert response.status_code == 401


testdata = [  # max_prefix_len,min_prefix_len,prefix,netmask,action,any
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000), 10, 'prefix_list_in',
     'prefix_list_out', 'stub')
]


@pytest.mark.parametrize("vrouter_name,vnet_name,area,prefix_list_in,prefix_list_out,stub_type", testdata)
def test_PUTupdateVrouterOspfAreaByVnmNameByArea(switch, vrouter_name, vnet_name, area, prefix_list_in, prefix_list_out,
                                                 stub_type):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name,vnet_name)
    c.createOSPFAreaForVrouter(vrouter_name, vnet_name, area, stub_type)
    cliHash = [x for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name]
    pprint("testing PUT  for updateVrouterOspfAreaByVnmNameByArea with  url  %s  payload  %s" % (
        "http://%s/vRest/vrouters/%s/ospf-areas/%s" % (switch, vrouter_name, area), json.dumps(
                {
                    "stub-type": stub_type
                })))
    response = requests.put("http://%s/vRest/vrouters/%s/ospf-areas/%s" % (switch, vrouter_name, area),
                            auth=(username, password), data=json.dumps(
                {
                    "stub-type": stub_type
                }))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showOSPFRouters() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationremoveVrouterOspfAreaByVnmNameByArea(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterOspfAreaByVnmNameByArea with url  http://%s/vRest/vrouters/vrouter-name/ospf-areas/area" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf-areas/area" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000), random.randint(3, 20), "stub")
]


@pytest.mark.parametrize("vrouter_name,vnet_name,area,stub_type", testdata)
def test_DELETEremoveVrouterOspfAreaByVnmNameByArea(switch, vrouter_name, vnet_name, area, stub_type):
    """

    """
    c = vrouter(switch)
    c.createOSPFAreaForVrouter(vrouter_name, vnet_name, area, stub_type)
    cliHash = [x for x in c.showOSPFAreaForVRouters() if x['vrouter-name'] == vrouter_name]
    pprint(cliHash)
    pprint(
            "testing DELETE  for removeVrouterOspfAreaByVnmNameByArea with  url  http://%s/vRest/vrouters/%s/ospf-areas/%s" % (
                switch, vrouter_name, area))
    response = requests.delete("http://%s/vRest/vrouters/%s/ospf-areas/%s" % (switch, vrouter_name, area),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showOSPFAreaForVRouters() if x['vrouter-name'] == vrouter_name]
    assert len(cliresponseListOfHashAfter) == 0
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationaddVrouterRipByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterRipByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/rips" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/rips" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouterIP % random.randint(0, 20))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,network", testdata)
def test_POSTaddVrouterRipByVrouterVnmName(switch, vrouter_name, vnet_name, network):
    """

    """
    c = vrouter(switch)
    c.createVRouterForRipTesting(vrouter_name, vnet_name, network)
    pprint("testing POST  for addVrouterRipByVrouterVnmName  with url  %s  payload  %s " % (
        "http://%s/vRest/vrouters/%s/rips" % (switch, vrouter_name), json.dumps({
            "netmask": 0,
            "network": network
        })))
    response = requests.post("http://%s/vRest/vrouters/%s/rips" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({
                                 "netmask": 0,
                                 "network": network
                             }))
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showRipVRouters()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterRipsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterRipsByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/rips" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/rips" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouterIP % random.randint(0, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,network", testdata)
def test_GETshowVrouterRipsByVrouterVnmName(switch, vrouter_name, vnet_name, network):
    """

        """
    c = vrouter(switch)
    c.createVRouterForRipTesting(vrouter_name, vnet_name, network)
    pprint("testing GET  for showVrouterRipsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/rips" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/rips" % (switch, vrouter_name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showRipVRouters()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterRipByVnmNameByNetwork(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterRipByVnmNameByNetwork with url  http://%s/vRest/vrouters/vrouter-name/rips/{network}" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/rips/{network}" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,network", testdata)
def test_GETshowVrouterRipByVnmNameByNetwork(switch, vrouter_name, vnet_name, network):
    """

        """
    c = vrouter(switch)
    c.createVRouterForRipTesting(vrouter_name, vnet_name, network)
    pprint("testing GET  for showVrouterRipByVnmNameByNetwork with url http://%s/vRest/vrouters/%s/rips/%s" % (
        switch, vrouter_name, "%s.%s" % (".".join(network.split(".")[0:3]), "0")))
    response = requests.get("http://%s/vRest/vrouters/%s/rips/%s" % (
        switch, vrouter_name, "%s.%s" % (".".join(network.split(".")[0:3]), "0")), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationremoveVrouterRipByVnmNameByNetwork(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterRipByVnmNameByNetwork  with url  http://%s/vRest/vrouters/vrouter-name/rips/network" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/rips/network" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,network", testdata)
def test_DELETEremoveVrouterRipByVnmNameByNetwork(switch, vrouter_name, vnet_name, network):
    """

    """
    c = vrouter(switch)
    c.createVRouterForRipTesting(vrouter_name, vnet_name, network)
    cliRespHash = [x for x in c.showRIPRouters() if x['vrouter-name'] == vrouter_name]
    pprint(cliRespHash)
    pprint("testing DELETE  for removeVrouterRipByVnmNameByNetwork with url  http://%s/vRest/vrouters/%s/rips/%s" % (
        switch, vrouter_name, "%s.%s" % (".".join(network.split(".")[0:3]), "0")))
    response = requests.delete("http://%s/vRest/vrouters/%s/rips/%s" % (
        switch, vrouter_name, "%s.%s" % (".".join(network.split(".")[0:3]), "0")),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showRIPRouters() if x['vrouter-name'] == vrouter_name]
    assert len(cliresponseListOfHashAfter) == 0
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterRipRoutesByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterRipRoutesByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/rip-routes" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/rip-routes" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testVRouterIP % random.randint(3, 200))
]

@pytest.mark.parametrize("vrouter_name,vnet_name,network", testdata)
def test_GETshowVrouterRibRoutes(switch, vrouter_name, vnet_name, network):
    """

        """
    c = vrouter(switch)
    c.createVRouterForRipTesting(vrouter_name, vnet_name, network)
    pprint("testing GET  for showVrouterRipRoutesByVrouterVnmName with url  http://%s/vRest/vrouter-rib-routes" % (
        switch))
    response = requests.get("http://%s/vRest/vrouter-rib-routes" % (switch),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()





def test_FailureAuthorizationshowVrouterRipRoutesByVnmNameByNetwork(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterRipRoutesByVnmNameByNetwork with url  http://%s/vRest/vrouters/vrouter-name/rip-routes/{network}" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/rip-routes/{network}" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200))
]


def test_FailureAuthorizationshowVrouterOspfNeighborsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspfNeighborsByVrouterVnmName with url http://%s/vRest/vrouters/vrouter-name/ospf-neighbors" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf-neighbors" % switch)
    assert response.status_code == 401



def test_GETshowVrouterOspfNeighborsByVrouterVnmName(switch):
    """

        """

    f = fabric_node(switch)
    switch1 ,switch2 = [x['name'] for  x  in  f.getFabricSwitches() ]
    vrouter_name1,vnet_name1,vrouter_name2,vnet_name2="vrouter_name1","vnet_name1","vrouter_name2","vnet_name2"
    c = vrouter(switch1)
    c.createVRouterForTestingWithOSPFServiceNeighbour(vrouter_name1,vnet_name1,"50.1.1.2", "50.1.1.0",100,0,True)
    c = vrouter(switch2)
    c.createVRouterForTestingWithOSPFServiceNeighbour(vrouter_name2,vnet_name2,"50.1.1.3", "50.1.1.0",100,0,False)
    pprint(
            "testing GET  for showVrouterOspfNeighborsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/ospf-neighbors" % (
                switch, vrouter_name1))
    response = requests.get("http://%s/vRest/vrouters/%s/ospf-neighbors" % (switch, vrouter_name1),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showOSPFRouters()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name1)
    c.deleteVnetAssociatedWithVrouter(vnet_name2)
    c.close()


def test_FailureAuthorizationshowVrouterOspf6NeighborsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterOspf6NeighborsByVrouterVnmName with   url  http://%s/vRest/vrouters/vrouter-name/ospf6-neighbors" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/ospf6-neighbors" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterOspf6NeighborsByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

        """
    f = fabric_node(switch)
    switch1 ,switch2 = [x['name'] for  x  in  f.getFabricSwitches() ]
    vrouter_name1,vnet_name1,vrouter_name2,vnet_name2="vrouter_name1","vnet_name1","vrouter_name2","vnet_name2"
    c = vrouter(switch1)
    c.createVRouterForTestingWithOSPF6ServiceNeighbour(vrouter_name1,vnet_name1,"50.1.1.2", "50.1.1.0",100,True)
    c = vrouter(switch2)
    c.createVRouterForTestingWithOSPF6ServiceNeighbour(vrouter_name2,vnet_name2,"50.1.1.3", "50.1.1.0",100,False)
    pprint(
            "testing GET  for showVrouterOspf6NeighborsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/ospf6-neighbors" % (
                switch, vrouter_name1))
    response = requests.get("http://%s/vRest/vrouters/%s/ospf6-neighbors" % (switch, vrouter_name1),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name1)
    c.deleteVnetAssociatedWithVrouter(vnet_name2)
    c.close()


def test_FailureAuthorizationshowVrouterPimInterfacesByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPimInterfacesByVrouterVnmName with url http://%s/vRest/vrouters/vrouter-name/pim-interfaces" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-interfaces" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testRPAdddress % random.randint(3, 200), testVRouterIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,rp_address,ip_address", testdata)
def test_GETshowVrouterPimInterfacesByVrouterVnmName(switch, vrouter_name, vnet_name, rp_address, ip_address):
    """

    """
    c = vrouter(switch)
    c.createVRouterForPIMSSMTesting(vrouter_name, vnet_name, rp_address)
    c.addInterfaceToAVRouterWithPIM(vrouter_name, ip_address)
    pprint(
            "testing GET  for showVrouterPimInterfacesByVrouterVnmName with url http://%s/vRest/vrouters/%s/pim-interfaces" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/pim-interfaces" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterMulticastKernelCachesByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterMulticastKernelCachesByVrouterVnmName withh url  http://%s/vRest/vrouters/vrouter-name/multicast-routes" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/multicast-routes" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterMulticastKernelCachesByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    pprint(
            "testing GET  for showVrouterMulticastKernelCachesByVrouterVnmName with url  http://%s/vRest/vrouters/%s/multicast-routes" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/multicast-routes" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterMulticastIgmpGroupsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterMulticastIgmpGroupsByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/multicast-igmp-groups" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/multicast-igmp-groups" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


def test_FailureAuthorizationshowVrouterPimJoinsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPimJoinsByVrouterVnmName with url   http://%s/vRest/vrouters/vrouter-name/pim-joins" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-joins" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),testInterfaceIP% random.randint(3, 200),
     testRPAdddress % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,ip_address,rp_address", testdata)
def test_GETshowVrouterPimJoinsByVrouterVnmName(switch, vrouter_name, vnet_name,ip_address, rp_address):
    """

        """
    c = vrouter(switch)
    c.createVRouterForPIMTesting(vrouter_name, vnet_name, rp_address)
    c.addInterfaceToAVRouterWithPIM(vrouter_name, ip_address)
    pprint("testing GET  for showVrouterPimJoinsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/pim-joins" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/pim-joins" % (switch, vrouter_name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterPimNeighborsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPimNeighborsByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/pim-neighbors" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-neighbors" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testRPAdddress % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,rp_address", testdata)
def test_GETshowVrouterPimNeighborsByVrouterVnmName(switch, vrouter_name, vnet_name, rp_address):
    """

        """
    c = vrouter(switch)
    c.createVRouterForPIMTesting(vrouter_name, vnet_name, rp_address)
    pprint(
            "testing GET  for showVrouterPimNeighborsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/pim-neighbors" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/pim-neighbors" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationaddVrouterPimRpByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterPimRpByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/pim-rps" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-rps" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testRPAdddress % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,rp_address", testdata)
def test_POSTaddVrouterPimRpByVrouterVnmName(switch, vrouter_name, vnet_name, rp_address):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTestingWithPIMSupport(vrouter_name, vnet_name)
    pprint(c.showPIMVRouters())
    pprint("testing POST  for addVrouterPimRpByVrouterVnmName with  url  %s   payload %s " % (
        "http://%s/vRest/vrouters/%s/pim-rps" % (switch, vrouter_name), json.dumps({
            "netmask": 4,
            "group": "224.0.0.0",
            "rp-address": rp_address
        })))
    response = requests.post("http://%s/vRest/vrouters/%s/pim-rps" % (switch, vrouter_name), auth=(username, password),
                             data=json.dumps({
                                 "netmask": 4,
                                 "group": "224.0.0.0",
                                 "rp-address": rp_address
                             }))
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showPIMVRouters()
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    pprint(cliresponseListOfHashAfter)
    c.close()


def test_FailureAuthorizationshowVrouterPimRpsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPimRpsByVrouterVnmName with url http://%s/vRest/vrouters/vrouter-name/pim-rps" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-rps" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testRPAdddress % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,rp_address", testdata)
def test_GETshowVrouterPimRpsByVrouterVnmName(switch, vrouter_name, vnet_name, rp_address):
    """

        """
    c = vrouter(switch)
    c.createVRouterForPIMTesting(vrouter_name, vnet_name, rp_address)
    pprint("testing GET  for showVrouterPimRpsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/pim-rps" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/pim-rps" % (switch, vrouter_name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showPIMVRouters()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterPimRpByVnmNameByAddress(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPimRpByVnmNameByAddress http://%s/vRest/vrouters/vrouter-name/pim-rps/rp-address/{rp-address}" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-rps/rp-address=1.2.3.4" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testRPAdddress % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,rp_address", testdata)
def test_GETshowVrouterPimRpByVnmNameByAddress(switch, vrouter_name, vnet_name, rp_address):
    """

        """
    c = vrouter(switch)
    c.createVRouterForPIMTesting(vrouter_name, vnet_name, rp_address)
    cliHash = [x for x in c.showPIMVRouters() if x['vrouter-name'] == vrouter_name]
    pprint(
            "testing GET  for showVrouterPimRpByVnmNameByAddress with url http://%s/vRest/vrouters/%s/pim-rps/rp-address=%s,group=api.null,netmask=api.null" % (
                switch, vrouter_name, rp_address))
    response = requests.get("http://%s/vRest/vrouters/%s/pim-rps/rp-address=%s,group=api.null,netmask=api.null" % (switch, vrouter_name, rp_address),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationremoveVrouterPimRpByVnmNameByAddress(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterPimRpByVnmNameByAddress with url  http://%s/vRest/vrouters/vrouter-name/pim-rps/rp-address/172.12.3.4" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-rps/rp-address=172.12.3.4,group=api.null,netmask=api.null" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testRPAdddress % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,rp_address", testdata)
def test_DELETEremoveVrouterPimRpByVnmNameByAddress(switch, vrouter_name, vnet_name, rp_address):
    """

    """
    c = vrouter(switch)
    c.createVRouterForPIMTesting(vrouter_name, vnet_name, rp_address)
    cliHash = [x for x in c.showPIMVRouters() if x['vrouter-name'] == vrouter_name]
    pprint(cliHash)
    pprint(
            "testing DELETE  for removeVrouterPimRpByVnmNameByAddress with url  http://%s/vRest/vrouters/%s/pim-rps/rp-address=%s,group=api.null,netmask=api.null" % (
                switch, vrouter_name, rp_address))
    response = requests.delete("http://%s/vRest/vrouters/%s/pim-rps/rp-address=%s,group=api.null,netmask=api.null" % (switch, vrouter_name, rp_address),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showPIMVRouters() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterPimRpByVnmNameByGroup(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPimRpByVnmNameByGroup with url   http://%s/vRest/vrouters/vrouter-name/pim-rps/group/group" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-rps/rp-address=null,group=grp,netmask=api.null" % switch)
    assert response.status_code == 401


def test_FailureAuthorizationremoveVrouterPimRpByVnmNameByGroup(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterPimRpByVnmNameByGroup with url   http://%s/vRest/vrouters/vrouter-name/pim-rps/group/224.0.0.0" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/pim-rps/rp-address=api.null,netmask=api.null,group=224.0.0.0" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testRPAdddress % random.randint(3, 200), testRPAdddress % random.randint(3, 200), "224.0.0.0")
]


def test_FailureAuthorizationaddVrouterIgmpStaticJoinByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterIgmpStaticJoinByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/igmp-static-joins" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/igmp-static-joins" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), testIGMPGRoupName % random.randint(0, 200000),
     testGroupIp % random.randint(3, 200), testSourceIp % random.randint(3, 200))

]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip,igmp_group_name,group_ip,source_ip", testdata)
def test_POSTaddVrouterIgmpStaticJoinByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip, igmp_group_name,
                                                      group_ip, source_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name, interface_ip)
    pprint("testing POST  for addVrouterIgmpStaticJoinByVrouterVnmName with url  %s  and  payload  %s" % (
        "http://%s/vRest/vrouters/%s/igmp-static-joins" % (switch, vrouter_name), json.dumps(
                {'interface': nic, 'group-ip': group_ip, 'source-ip': source_ip, 'name': igmp_group_name})))
    response = requests.post("http://%s/vRest/vrouters/%s/igmp-static-joins" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps(
                {'interface': nic, 'group-ip': group_ip, 'source-ip': source_ip, 'name': igmp_group_name}))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showIGMPStaticGroupJoins()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterIgmpStaticJoinsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterIgmpStaticJoinsByVrouterVnmName by url http://%s/vRest/vrouters/vrouter-name/igmp-static-joins" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/igmp-static-joins" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), testIGMPGRoupName % random.randint(0, 200000),
     testGroupIp % random.randint(3, 200), testSourceIp % random.randint(3, 200))

]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip , igmp_group_name , group_ip , source_ip", testdata)
def test_GETshowVrouterIgmpStaticJoinsByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip, igmp_group_name,
                                                       group_ip, source_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic=c.addInterfaceToAVRouter(vrouter_name,interface_ip)
    ##Add igmp static  join
    response = requests.post("http://%s/vRest/vrouters/%s/igmp-static-joins" % (switch, vrouter_name),
                            auth=(username, password) , data=json.dumps({
                              "name": igmp_group_name,
                              "group-ip": group_ip,
                              "source-ip": source_ip,
                              "interface": nic
                        }))
    pprint(
            "testing GET  for showVrouterIgmpStaticJoinsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/igmp-static-joins" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/igmp-static-joins" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationshowVrouterIgmpStaticJoinByVnmNameByName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterIgmpStaticJoinByVnmNameByName with url  http://%s/vRest/vrouters/vrouter-name/igmp-static-joins/name" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/igmp-static-joins/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), testIGMPGRoupName % random.randint(0, 200000),
     testGroupIp % random.randint(3, 200), testSourceIp % random.randint(3, 200))

]


@pytest.mark.parametrize("vrouter_name,vnet_name, interface_ip , igmp_group_name , group_ip , source_ip", testdata)
def test_GETshowVrouterIgmpStaticJoinByVnmNameByName(switch, vrouter_name, vnet_name, interface_ip, igmp_group_name,
                                                     group_ip, source_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTestingIGMPStaticJoin(vrouter_name, vnet_name, interface_ip, igmp_group_name, group_ip,
                                             source_ip)
    cliHash = [x for x in c.showIGMPStaticGroupJoins() if x['vrouter-name'] == vrouter_name]
    pprint(cliHash)
    pprint(
            "testing GET  for showVrouterIgmpStaticJoinByVnmNameByName with url   http://%s/vRest/vrouters/%s/igmp-static-joins/%s" % (
                switch, vrouter_name, igmp_group_name))
    response = requests.get(
            "http://%s/vRest/vrouters/%s/igmp-static-joins/%s" % (switch, vrouter_name, igmp_group_name),
            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showIGMPStaticGroupJoins() if x['vrouter-name'] == vrouter_name]
    jsonResponseDat = [x for x in json.loads(response.text)["data"] if x['name'] == igmp_group_name]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationremoveVrouterIgmpStaticJoinByVnmNameByName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterIgmpStaticJoinByVnmNameByName with url  http://%s/vRest/vrouters/vrouter-name/igmp-static-joins/name" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/igmp-static-joins/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), testIGMPGRoupName % random.randint(0, 200000),
     testGroupIp % random.randint(3, 200), testSourceIp % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name, interface_ip , igmp_group_name , group_ip , source_ip", testdata)
def test_DELETEremoveVrouterIgmpStaticJoinByVnmNameByName(switch, vrouter_name, vnet_name, interface_ip,
                                                          igmp_group_name, group_ip, source_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTestingIGMPStaticJoin(vrouter_name, vnet_name, interface_ip, igmp_group_name, group_ip,
                                             source_ip)
    cliHash = [x for x in c.showIGMPStaticGroupJoins() if x['vrouter-name'] == vrouter_name]
    pprint(cliHash)
    pprint(
            "testing DELETE  for removeVrouterIgmpStaticJoinByVnmNameByName with url  http://%s/vRest/vrouters/%s/igmp-static-joins/%s" % (
                switch, vrouter_name, igmp_group_name))
    response = requests.delete(
            "http://%s/vRest/vrouters/%s/igmp-static-joins/%s" % (switch, vrouter_name, igmp_group_name),
            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showIGMPStaticGroupJoins()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)
    c.close()


def test_FailureAuthorizationaddVrouterNicByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterNicByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/interfaces" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interfaces" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_POSTaddVrouterNicByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    v=vlan(switch)
    v.createVlanForTesting(100)
    pprint("testing POST  for addVrouterNicByVrouterVnmName with url  %s  payload  %s " % (
        "http://%s/vRest/vrouters/%s/interfaces" % (switch, vrouter_name), json.dumps(
                {
                    "netmask": 24,
                    "ip": interface_ip,
                    "exclusive": "false",
                    "vlan" : 100
                })))
    response = requests.post("http://%s/vRest/vrouters/%s/interfaces" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps(
                {
                    "netmask": 24,
                    "ip": interface_ip,
                    "exclusive": "false",
                    "vlan" : 100
                }))
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showVRouterInterfaces() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterNicsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterNicsByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/interfaces" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interfaces" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_GETshowVrouterNicsByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name, interface_ip)
    pprint("testing GET  for showVrouterNicsByVrouterVnmName with url  http://%s/vRest/vrouters/%s/interfaces" % (
        switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/interfaces" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showVRouterInterfaces() if x['vrouter-name'] == vrouter_name]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterNicByVnmNameByVnic(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterNicByVnmNameByVnic http://%s/vRest/vrouters/vrouter-name/interfaces/nic" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interfaces/nic" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_GETshowVrouterNicByVnmNameByVnic(switch, vrouter_name, vnet_name, interface_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name, interface_ip)
    pprint("testing GET  for showVrouterNicByVnmNameByVnic with  url http://%s/vRest/vrouters/%s/interfaces/%s" % (
        switch, vrouter_name, nic))
    response = requests.get("http://%s/vRest/vrouters/%s/interfaces/%s" % (switch, vrouter_name, nic),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showVRouterInterfaces() if x['vrouter-name'] == vrouter_name]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationupdateVrouterNicByVnmNameByVnic(switch):
    """

        """
    pprint(
            "testing Failed authentication  for updateVrouterNicByVnmNameByVnic with url  http://%s/vRest/vrouters/vrouter-name/interfaces/nic" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interfaces/nic" % switch)
    assert response.status_code == 401


testdata = [  # max_prefix_len,min_prefix_len,prefix,netmask,action,any
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200),
        10, 4, 'prefix-1451598241', 24,
        'permit', 'false', random.randint(7, 2000))
]


@pytest.mark.parametrize(
        "vrouter_name,vnet_name,networkip,max_prefix_len,min_prefix_len,prefix,netmask,action,any,sequence", testdata)
def test_PUTupdateVrouterNicByVnmNameByVnic(switch, vrouter_name, vnet_name, networkip, max_prefix_len, min_prefix_len,
                                            prefix, netmask,
                                            action, any, sequence):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name, networkip)
    pprint("testing PUT  for updateVrouterNicByVnmNameByVnic with url  %s  payload  %s " % (
        "http://%s/vRest/vrouters/%s/interfaces/%s" % (switch, vrouter_name, nic), json.dumps(
                {
                    "mtu": 1500
                })))
    response = requests.put("http://%s/vRest/vrouters/%s/interfaces/%s" % (switch, vrouter_name, nic),
                            auth=(username, password), data=json.dumps(
                {
                    "mtu": 1500
                }))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showVRouterInterfaces()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationremoveVrouterNicByVnmNameByVnic(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterNicByVnmNameByVnic with url   http://%s/vRest/vrouters/vrouter-name/interfaces/nic" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interfaces/nic" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_DELETEremoveVrouterNicByVnmNameByVnic(switch, vrouter_name, vnet_name, interface_ip):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name, interface_ip)
    pprint("testing DELETE  for removeVrouterNicByVnmNameByVnic with url http://%s/vRest/vrouters/%s/interfaces/%s" % (
        switch, vrouter_name, nic))
    response = requests.delete("http://%s/vRest/vrouters/%s/interfaces/%s" % (switch, vrouter_name, nic),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showVRouterInterfaces() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationaddVrouterNicConfigByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterNicConfigByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/interface-configs" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interface-configs" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), testGroupIp % random.randint(3, 200),
     testSourceIp % random.randint(3, 200),
     testInterface)
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface,group_ip,source_ip,name", testdata)
def test_POSTaddVrouterNicConfigByVrouterVnmName(switch, vrouter_name, vnet_name, interface, group_ip, source_ip, name):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name, interface)
    pprint("testing POST  for addVrouterNicConfigByVrouterVnmName with url  %s   payload %s" % (
        "http://%s/vRest/vrouters/%s/interface-configs" % (switch, vrouter_name), json.dumps(
                {
                    "nic": nic,
                    "ospf-hello-interval": 2,
                    "ospf-dead-interval": 20,
                    "ospf-priority": 10,
                    "ospf-cost": 20,
                    "ospf-passive-if": "false",
                    "bfd-multiplier": 7
                })))

    response = requests.post("http://%s/vRest/vrouters/%s/interface-configs" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps(
                {
                    "nic": nic,
                    "ospf-hello-interval": 2,
                    "ospf-dead-interval": 20,
                    "ospf-priority": 10,
                    "ospf-cost": 20,
                    "ospf-passive-if": "false",
                    "bfd-multiplier": 7
                }))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showVRouterInterfacesConfigs() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterNicConfigsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterNicConfigsByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/interface-configs" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interface-configs" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_GETshowVrouterNicConfigsByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic = c.addInterfaceToAVRouter(vrouter_name, interface_ip)
    response = requests.post("http://%s/vRest/vrouters/%s/interface-configs" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps(
                {
                    "nic": nic,
                    "ospf-hello-interval": 2,
                    "ospf-dead-interval": 20,
                    "ospf-priority": 10,
                    "ospf-cost": 20,
                    "ospf-passive-if": "false",
                    "bfd-multiplier": 7
                }))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    pprint(
            "testing GET  for showVrouterNicConfigsByVrouterVnmName with url http://%s/vRest/vrouters/%s/interface-configs" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/interface-configs" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterNicConfigByVnmNameByVnic(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterNicConfigByVnmNameByVnic with   url http://%s/vRest/vrouters/vrouter-name/interface-configs/nic" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interface-configs/nic" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_GETshowVrouterNicConfigByVnmNameByVnic(switch, vrouter_name, vnet_name, interface_ip):
    """

        """
    c = vrouter(switch)
    nic = c.createAVrouterWithInterfaceConfigSupport(vrouter_name, vnet_name, interface_ip)
    cliHash = [x for x in c.showVRouterInterfacesConfigs() if x['vrouter-name'] == vrouter_name]
    pprint(
            "testing GET  for showVrouterNicConfigByVnmNameByVnic with url  http://%s/vRest/vrouters/%s/interface-configs/%s" % (
                switch, vrouter_name, nic))
    response = requests.get("http://%s/vRest/vrouters/%s/interface-configs/%s" % (switch, vrouter_name, nic),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationupdateVrouterNicConfigByVnmNameByVnic(switch):
    """

        """
    pprint("testing Failed authentication  for updateVrouterNicConfigByVnmNameByVnic ")
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interface-configs/nic" % switch)
    assert response.status_code == 401


testdata = [
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_PUTupdateVrouterNicConfigByVnmNameByVnic(switch, vrouter_name, vnet_name, interface_ip):
    """

    """
    c = vrouter(switch)
    nic = c.createAVrouterWithInterfaceConfigSupport(vrouter_name, vnet_name, interface_ip)
    cliHash = [x for x in c.showVRouterInterfacesConfigs() if x['vrouter-name'] == vrouter_name]
    pprint("testing PUT  for updateVrouterNicConfigByVnmNameByVnic with url %s  and  payload  %s" % (
        "http://%s/vRest/vrouters/%s/interface-configs/%s" % (switch, vrouter_name, nic), json.dumps(
                {
                    "ospf-hello-interval": 2,
                    "ospf-dead-interval": 20,
                    "ospf-priority": 10,
                    "ospf-cost": 20,
                    "ospf-passive-if": "false",
                    "bfd-multiplier": 7
                })))
    response = requests.put("http://%s/vRest/vrouters/%s/interface-configs/%s" % (switch, vrouter_name, nic),
                            auth=(username, password), data=json.dumps(
                {
                    "ospf-hello-interval": 2,
                    "ospf-dead-interval": 20,
                    "ospf-priority": 10,
                    "ospf-cost": 20,
                    "ospf-passive-if": "false",
                    "bfd-multiplier": 7
                }))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showVRouterInterfacesConfigs() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationremoveVrouterNicConfigByVnmNameByVnic(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterNicConfigByVnmNameByVnic  for  http://%s/vRest/vrouters/vrouter-name/interface-configs/nic" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/interface-configs/nic" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip", testdata)
def test_DELETEremoveVrouterNicConfigByVnmNameByVnic(switch, vrouter_name, vnet_name, interface_ip):
    """

    """
    c = vrouter(switch)
    nic = c.createAVrouterWithInterfaceConfigSupport(vrouter_name, vnet_name, interface_ip)
    cliHash = [x for x in c.showVRouterInterfacesConfigs() if x['vrouter-name'] == vrouter_name]
    pprint(
            "testing DELETE  for removeVrouterNicConfigByVnmNameByVnic for url  http://%s/vRest/vrouters/%s/interface-configs/%s" % (
                switch, vrouter_name, nic))
    response = requests.delete("http://%s/vRest/vrouters/%s/interface-configs/%s" % (switch, vrouter_name, nic),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showVRouterInterfaces()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationaddVrouterLoopbackByVrouterVnmName(switch):
    """

    """
    pprint(
            "testing Failed authentication  for addVrouterLoopbackByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/loopback-interfaces" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/loopback-interfaces" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip,index", testdata)
def test_POSTaddVrouterLoopbackByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip, index):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    pprint("testing POST  for addVrouterLoopbackByVrouterVnmName   with url  %s  and   payload  %s  " % (
        "http://%s/vRest/vrouters/%s/loopback-interfaces" % (switch, vrouter_name), json.dumps(
                {
                    "index": index,
                    "ip": interface_ip
                })))
    response = requests.post("http://%s/vRest/vrouters/%s/loopback-interfaces" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps(
                {
                    "index": index,
                    "ip": interface_ip
                }))
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showLoopbackInterfaces() if x['vrouter-name'] == vrouter_name]
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterLoopbacksByVrouterVnmName(switch):
    """

        """
    pprint("testing Failed authentication  for showVrouterLoopbacksByVrouterVnmName ")
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/loopback-interfaces" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), random.randint(4, 250))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip,index", testdata)
def test_GETshowVrouterLoopbacksByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip, index):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.AddLoopBackInterfaces(vrouter_name, interface_ip, index)
    pprint(
            "testing GET  for showVrouterLoopbacksByVrouterVnmName with url http://%s/vRest/vrouters/%s/loopback-interfaces" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/loopback-interfaces" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showLoopbackInterfaces() if x['vrouter-name'] == vrouter_name]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterLoopbackByVnmNameByIndex(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterLoopbackByVnmNameByIndex with url  http://%s/vRest/vrouters/vrouter-name/loopback-interfaces/index" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/loopback-interfaces/index" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip,index", testdata)
def test_GETshowVrouterLoopbackByVnmNameByIndex(switch, vrouter_name, vnet_name, interface_ip, index):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.AddLoopBackInterfaces(vrouter_name, interface_ip, index)
    pprint(
            "testing GET  for showVrouterLoopbackByVnmNameByIndex with url  http://%s/vRest/vrouters/%s/loopback-interfaces/%s" % (
                switch, vrouter_name, index))
    response = requests.get("http://%s/vRest/vrouters/%s/loopback-interfaces/%s" % (switch, vrouter_name, index),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showLoopbackInterfaces() if
                       x['vrouter-name'] == vrouter_name and x['index'] == str(index)]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationremoveVrouterLoopbackByVnmNameByIndex(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterLoopbackByVnmNameByIndex with url  http://%s/vRest/vrouters/vrouter-name/loopback-interfaces/index" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/loopback-interfaces/index" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip,index", testdata)
def test_DELETEremoveVrouterLoopbackByVnmNameByIndex(switch, vrouter_name, vnet_name, interface_ip, index):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.AddLoopBackInterfaces(vrouter_name, interface_ip, index)
    pprint(
            "testing DELETE  for removeVrouterLoopbackByVnmNameByIndex with url  http://%s/vRest/vrouters/%s/loopback-interfaces/%s" % (
                switch, vrouter_name, index))
    response = requests.delete("http://%s/vRest/vrouters/%s/loopback-interfaces/%s" % (switch, vrouter_name, index),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.showLoopbackInterfaces() if x['vrouter-name'] == vrouter_name]
    assert len(cliresponseListOfHashAfter) == 0
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationaddVrouterPacketRelayByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for addVrouterPacketRelayByVrouterVnmName with url   http://%s/vRest/vrouters/vrouter-name/packet-relays" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/packet-relays" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), testInterfaceIP % random.randint(3, 200))
]


def test_FailureAuthorizationshowVrouterPacketRelaysByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPacketRelaysByVrouterVnmName with url  http://%s/vRest/vrouters/vrouter-name/packet-relays" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/packet-relays" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testInterfaceIP % random.randint(3, 200), testInterfaceIP % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,interface_ip,forward_ip", testdata)
def test_GETshowVrouterPacketRelaysByVrouterVnmName(switch, vrouter_name, vnet_name, interface_ip, forward_ip):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    nic=c.addInterfaceToAVRouter(vrouter_name,interface_ip)
    ## Add  a  packet relay
    response = requests.post("http://%s/vRest/vrouters/%s/packet-relays" % (switch, vrouter_name),
                            auth=(username, password) , data= json.dumps({
                      "nic": nic,
                      "forward-ip": forward_ip,
                      "forward-proto": "dhcp"
            }))
    pprint(
            "testing GET  for showVrouterPacketRelaysByVrouterVnmName with url  http://%s/vRest/vrouters/%s/packet-relays" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/packet-relays" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = [x for x in c.showPacketRelays() if x['vrouter-name'] == vrouter_name]
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationremoveVrouterPacketRelayByVnmNameUniqueKeyAll(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterPacketRelayByVnmNameUniqueKeyAll with url  http://%s/vRest/vrouters/vrouter-name/packet-relays/forward-proto=forward-proto,forward-ip=forward-ip,nic=nic" % switch)
    response = requests.get(
            "http://%s/vRest/vrouters/vrouter-name/packet-relays/forward-proto=forward-proto,forward-ip=forward-ip,nic=nic" % switch)
    assert response.status_code == 401


testdata = [  # interface,group_ip,source_ip,name
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testPrefixname % random.randint(0, 200000), "permit", testPrefixNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,prefix_name,action,prefix_network", testdata)
def test_POSTaddVrouterPrefixListByVrouterVnmName(switch, vrouter_name, vnet_name, prefix_name, action, prefix_network):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    pprint("testing POST  for addVrouterPrefixListByVrouterVnmName   with url  %s and   payload  %s" % (
        "http://%s/vRest/vrouters/%s/prefix-lists" % (switch, vrouter_name), json.dumps({
            "netmask": 24,
            "name": prefix_name,
            "action": action,
            "prefix": prefix_network
        })))
    response = requests.post("http://%s/vRest/vrouters/%s/prefix-lists" % (switch, vrouter_name),
                             auth=(username, password), data=json.dumps({
            "netmask": 24,
            "name": prefix_name,
            "action": action,
            "prefix": prefix_network
        }))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showPrefixList()
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterPrefixListsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPrefixListsByVrouterVnmName for url  http://%s/vRest/vrouters/vrouter-name/prefix-lists" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/prefix-lists" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testPrefixname % random.randint(0, 200000), "permit", testPrefixNetwork % random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,prefix_name,action,prefix_network", testdata)
def test_GETshowVrouterPrefixListsByVrouterVnmName(switch, vrouter_name, vnet_name, prefix_name, action,
                                                   prefix_network):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addPrefixList(vrouter_name, prefix_name, action, prefix_network)
    pprint(
            "testing GET  for showVrouterPrefixListsByVrouterVnmName for url  http://%s/vRest/vrouters/%s/prefix-lists" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/prefix-lists" % (switch, vrouter_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showPrefixList()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationshowVrouterPrefixListsByVnmNameUniqueKeyAll(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterPrefixListsByVnmNameUniqueKeyAll for url   http://%s/vRest/vrouters/vrouter-name/prefix-lists/name=name,seq=seq" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/prefix-lists/name=name,seq=seq" % switch)
    assert response.status_code == 401


testdata = [  #
    (
        testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
        testPrefixname % random.randint(0, 20000), "permit", testPrefixNetwork % random.randint(3, 200),
        random.randint(3, 20000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name,prefix_name, action, prefix_network,seq", testdata)
def test_GETshowVrouterPrefixListsByVnmNameUniqueKeyAll(switch, vrouter_name, vnet_name, prefix_name, action,
                                                        prefix_network, seq):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addPrefixList(vrouter_name, prefix_name, action, prefix_network, seq)
    pprint(
            "testing GET  for showVrouterPrefixListsByVnmNameUniqueKeyAll  for url  http://%s/vRest/vrouters/%s/prefix-lists/name=%s,seq=%s" % (
                switch, vrouter_name, prefix_name, seq))
    response = requests.get(
            "http://%s/vRest/vrouters/%s/prefix-lists/name=%s,seq=%s" % (switch, vrouter_name, prefix_name, seq),
            auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.showPrefixList()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationupdateVrouterPrefixListByVnmNameUniqueKeyAll(switch):
    """

    """
    pprint(
            "testing Failed authentication  for updateVrouterPrefixListByVnmNameUniqueKeyAll for   url  http://%s/vRest/vrouters/vrouter-name/prefix-lists/name=name,seq=seq" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/prefix-lists/name=name,seq=seq" % switch)
    assert response.status_code == 401


testdata = [
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testPrefixname % random.randint(3, 200), testPrefixNetwork % random.randint(3, 200), random.randint(3, 200), 10, 3,
     testPrefixIP % random.randint(3, 200), 24, 'permit', 'false')
]


@pytest.mark.parametrize(
        "vrouter_name,vnet_name,prefix_name,prefix_network,seq,max_prefix_len,min_prefix_len,prefix,netmask,action,any",
        testdata)
def test_PUTupdateVrouterPrefixListByVnmNameUniqueKeyAll(switch, vrouter_name, vnet_name, prefix_name, prefix_network,
                                                         seq, max_prefix_len,
                                                         min_prefix_len, prefix, netmask, action, any):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addPrefixList(vrouter_name, prefix_name, action, prefix_network, seq)
    cliresponseListOfHashBefore = c.showPrefixList()
    pprint("testing PUT  for updateVrouterPrefixListByVnmNameUniqueKeyAll for   url  %s   payload  %s  " % (
        "http://%s/vRest/vrouters/%s/prefix-lists/name=%s,seq=%s" % (switch, vrouter_name, prefix_name, seq),
        json.dumps(
                {'prefix': prefix,
                 'netmask': netmask, 'action': action})))
    response = requests.put(
            "http://%s/vRest/vrouters/%s/prefix-lists/name=%s,seq=%s" % (switch, vrouter_name, prefix_name, seq),
            auth=(username, password), data=json.dumps(
                    {'prefix': prefix,
                     'netmask': netmask, 'action': action}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showPrefixList()
    pprint(cliresponseListOfHashBefore)
    pprint(cliresponseListOfHashAfter)
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_FailureAuthorizationremoveVrouterPrefixListByVnmNameUniqueKeyAll(switch):
    """

        """
    pprint(
            "testing Failed authentication  for removeVrouterPrefixListByVnmNameUniqueKeyAll for  url  http://%s/vRest/vrouters/vrouter-name/prefix-lists/name,seq=seq" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/prefix-lists/name,seq=seq" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000),
     testPrefixname % random.randint(3, 200), testPrefixNetwork % random.randint(3, 200), random.randint(3, 200))
]


@pytest.mark.parametrize("vrouter_name,vnet_name, prefix_name,prefix_network,seq", testdata)
def test_DELETEremoveVrouterPrefixListByVnmNameUniqueKeyAll(switch, vrouter_name, vnet_name, prefix_name,
                                                            prefix_network, seq):
    """

    """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    c.addPrefixList(vrouter_name, prefix_name, "permit", prefix_network, seq)
    pprint(
            "testing DELETE  for removeVrouterPrefixListByVnmNameUniqueKeyAll for url  http://%s/vRest/vrouters/%s/prefix-lists/name=%s,seq=%d" % (
                switch, vrouter_name, prefix_name, seq))
    response = requests.delete(
            "http://%s/vRest/vrouters/%s/prefix-lists/name=%s,seq=%d" % (switch, vrouter_name, prefix_name, seq),
            auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.showPrefixList()
    pprint(cliresponseListOfHashAfter)


def test_FailureAuthorizationshowVrouterBfdNeighborsByVrouterVnmName(switch):
    """

        """
    pprint(
            "testing Failed authentication  for showVrouterBfdNeighborsByVrouterVnmName for  url   http://%s/vRest/vrouters/vrouter-name/bfd-neighbors" % switch)
    response = requests.get("http://%s/vRest/vrouters/vrouter-name/bfd-neighbors" % switch)
    assert response.status_code == 401


testdata = [  #
    (testVRouter % random.randint(0, 200000), testVNet % random.randint(0, 200000))
]


@pytest.mark.parametrize("vrouter_name,vnet_name", testdata)
def test_GETshowVrouterBfdNeighborsByVrouterVnmName(switch, vrouter_name, vnet_name):
    """

        """
    c = vrouter(switch)
    c.createAVRouterForTesting(vrouter_name, vnet_name)
    pprint(
            "testing GET  for showVrouterBfdNeighborsByVrouterVnmName for url  http://%s/vRest/vrouters/%s/bfd-neighbors" % (
                switch, vrouter_name))
    response = requests.get("http://%s/vRest/vrouters/%s/bfd-neighbors" % (switch, vrouter_name),
                            auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    c.deleteVnetAssociatedWithVrouter(vnet_name)


def test_teardown(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()


