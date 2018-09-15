import sys

import pytest

sys.path.append(".")
import requests
import json
from vnet import vnet
from pprint import pprint
import logging
import random


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg


username = "network-admin"
password = "test123"
portList = "40,41,42,43,45"
testVnet = "VnetRest-%d"


def test_setup(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()


def test_FailureAuthorizationcreateVnet(switch):
    """
           
        """
    pprint("testing Failed authentication  for createVnet with url http://%s/vRest/vnets" % switch)
    response = requests.get("http://%s/vRest/vnets" % switch)
    assert response.status_code == 401




testdata = [  # name,scope,vlan,ports,admin,vrg_id,num_vlans,managed_ports,vlan_ports,config_admin,vnet_mgr_name,vnet_mgr_storage_pool,message
      ("", "fabric" , random.randint(2, 4090),random.randint(2, 60), 0 , "0" ,0,  "" , "false", "vnet-mgr-name", "vnet-mgr-storage-pool", "Illegal value for name. Legal values are: letters, numbers, _, ., :, and -"),
     ]
@pytest.mark.parametrize("name,scope,vlans,ports,admin,num_vlans,managed_ports,vlan_ports,config_admin,vnet_mgr_name,vnet_mgr_storage_pool,message", testdata)
def test_POSTcreateVnetErrorMessages(switch, name, scope,vlans,ports,admin,num_vlans,managed_ports,vlan_ports,config_admin,vnet_mgr_name,vnet_mgr_storage_pool,message):
    """
    """

    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "vlans": vlans,
          "ports": ports,
          "admin": admin,
          "num-vlans": num_vlans,
          "managed-ports": managed_ports,
          "vlan-ports": vlan_ports,
          "config-admin": config_admin,
          "vnet-mgr-name": vnet_mgr_name,
          "vnet-mgr-storage-pool": vnet_mgr_storage_pool
}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({'name': name, 'scope': 'fabric'}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0



testdata = [  # name,scope,message
        (testVnet % random.randint(2, 20000), "fab" ,"Invalid value for scope.")
]
@pytest.mark.parametrize("name,scope,message", testdata)
def test_POSTcreateVnetErrorMessagesWrongScope(switch, name, scope,message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope

}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0



testdata = [  # name,scope,message
        (testVnet % random.randint(2, 20000), "fabric" , "88888", "The value 88888 is invalid. Value should be a comma delimited list of vlans or vlan ranges such as 22,33,40-42,45. Vlan value should be between 0 and 4095.")
]
@pytest.mark.parametrize("name,scope,vlans,message", testdata)
def test_POSTcreateVnetErrorMessagesWrongVlans(switch, name, scope,vlans, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "vlans" : vlans

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "vlans" : vlans


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0


testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "88888", "The value 88888 is invalid. Value should be a comma delimited list of vlans or vlan ranges such as 22,33,40-42,45. Vlan value should be between 0 and 4095.")
]
@pytest.mark.parametrize("name,scope,vlans,message", testdata)
def test_POSTcreateVnetErrorMessagesWrongVlans(switch, name, scope,vlans, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "vlans" : vlans

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "vlans" : vlans


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0


testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "", "For input string: \"\"")
]
@pytest.mark.parametrize("name,scope,admin,message", testdata)
def test_POSTcreateVnetErrorMessagesBlankAdmin(switch, name, scope,admin, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "admin" : admin

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "admin" : admin


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0


testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "", " is an invalid value for admin")
]
@pytest.mark.parametrize("name,scope,admin,message", testdata)
def test_POSTcreateVnetErrorMessagesBlankAdmin(switch, name, scope,admin, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "admin" : admin

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "admin" : admin


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0



testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "", " is an invalid value for num-vlans")
]
@pytest.mark.parametrize("name,scope,num_vlans,message", testdata)
def test_POSTcreateVnetErrorMessagesBlankNumVlans(switch, name, scope,num_vlans, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "num-vlans" : num_vlans

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "num-vlans" : num_vlans


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0



testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "aaa", "The value aaa is invalid. Value should be a comma delimited list of ports or port ranges such as 22,33,40-42,45. Port value should be between 0 and 255.")
]
@pytest.mark.parametrize("name,scope,managed_ports,message", testdata)
def test_POSTcreateVnetErrorMessagesManagedPortsWrongType(switch, name, scope,managed_ports, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "managed-ports" : managed_ports

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "managed-ports" : managed_ports


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0



testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "aaa", "Parameter vlan-ports is not recognized as type string.")
]
@pytest.mark.parametrize("name,scope,vlan_ports,message", testdata)
def test_POSTcreateVnetErrorMessagesVlanPortsWrongType(switch, name, scope,vlan_ports, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "vlan-ports" : vlan_ports

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "vlan-ports" : vlan_ports


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0




testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "", "Illegal value for vnet-mgr-name. Legal values are: letters, numbers, _, ., :, and -")
]
@pytest.mark.parametrize("name,scope,vnet_mgr_name,message", testdata)
def test_POSTcreateVnetErrorMessagesEmptyVnetManager(switch, name, scope,vnet_mgr_name, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "vnet-mgr-name" : vnet_mgr_name

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "vnet-mgr-name" : vnet_mgr_name


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0







testdata = [  # name,scope,ports, message
        (testVnet % random.randint(2, 20000), "fabric" , "", "Vnet manager create failed: storage pool  not found")
]
@pytest.mark.parametrize("name,scope,vnet_mgr_storage_pool,message", testdata)
def test_POSTcreateVnetErrorMessagesEmptyVnetManagerStoragePool(switch, name, scope,vnet_mgr_storage_pool, message):
    """
    """
    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({
          "name": name,
          "scope": scope,
          "vnet-mgr-storage-pool" : vnet_mgr_storage_pool

}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({
          "name": name,
          "scope": scope,
          "vnet-mgr-storage-pool" : vnet_mgr_storage_pool


}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")

    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    assert json.loads(response.text)["result"]["result"][0]["code"] != 0









testdata = [  # vlans,ports
    (testVnet % random.randint(2, 20000), random.randint(2, 4090), random.randint(2, 60))
]


@pytest.mark.parametrize("name,vlan,ports", testdata)
def test_POSTcreateVnet(switch, name, vlan, ports):
    """
       
    """

    v = vnet(switch)
    pprint("testing POST  for createVnet with  url  %s and  payload  %s"%("http://%s/vRest/vnets" % (switch)  ,json.dumps({'name': name, 'scope': 'fabric'}) ))
    response = requests.post("http://%s/vRest/vnets" % (switch), auth=(username, password),
                             data=json.dumps({'name': name, 'scope': 'fabric'}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    pprint("=========CLI  OUTOUT =============")
    pprint([x for x in v.show() if x['name'] == name])
    pprint("=========END  OF  CLI  OUTOUT =============")
    assert str(response.status_code) == "201"
    cliObjCreated = [x for x in v.show() if x['name'] == name]
    assert cliObjCreated[0]['name'] == name
    assert cliObjCreated[0]['admin'] == "%s-admin" % name
    assert cliObjCreated[0]['scope'] == "fabric"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    v.deleteVnet(name)

def test_FailureAuthorizationshowVnets(switch):
    """
           
        """
    pprint("testing Failed authentication  for showVnets with url http://%s/vRest/vnets" % switch )
    response = requests.get("http://%s/vRest/vnets" % switch)
    assert response.status_code == 401


def test_GETshowVnets(switch):
    """
           
        """
    c = vnet(switch)
    pprint("testing GET  for showVnets http://%s/vRest/vnets" % switch)
    response = requests.get("http://%s/vRest/vnets" % (switch), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    vnetList = [x['name'] for x in c.show()]
    jsonResponseDat = json.loads(response.text)["data"]
    vnetListFromREST = [x['name'] for x in jsonResponseDat]
    pprint("=========CLI  OUTOUT =============")
    pprint(vnetList)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(vnetListFromREST)
    pprint("=========END  OF JSON  OUTOUT =============")
    assert len(vnetList) == len(vnetListFromREST)


def test_FailureAuthorizationshowVnetByName(switch):
    """
           
    """
    test_vnet=testVnet % random.randint(0, 20000)
    pprint("testing Failed authentication  for showVnetByName with  http://%s/vRest/vnets/%s" % (switch,test_vnet ))
    response = requests.get("http://%s/vRest/vnets/%s" % (switch, test_vnet))
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_GETshowVnetByName(switch, name):
    """
           
        """
    v = vnet(switch)
    v.createVNetForTesting(name)
    pprint("testing GET  for showVnetByName http://%s/vRest/vnets/%s" % (switch, name))
    response = requests.get("http://%s/vRest/vnets/%s" % (switch, name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    vnetList = [x for x in v.show() if x['name'] == str(name)]
    vnetListFromREST = json.loads(response.text)["data"]
    descCLI = [x['name'] for x in v.show() if x['name'] == str(name)][0]
    descREST = [x['name'] for x in json.loads(response.text)["data"]][0]
    assert descCLI == descREST
    pprint("=========CLI  OUTOUT =============")
    pprint(vnetList)
    pprint("=========END  OF CLI  OUTOUT =============")
    pprint("=========JSON  OUTOUT =============")
    pprint(vnetListFromREST)
    pprint("=========END  OF JSON  OUTOUT =============")
    v.deleteVnet(name)


testdata = [  #
    ("1=1","Illegal value for name. Legal values are: letters, numbers, _, ., :, and -")
]


@pytest.mark.parametrize("name,message", testdata)
def test_GETshowVnetByNameErrorMessage(switch, name,message):
    """

        """
    v = vnet(switch)
    v.createVNetForTesting(name)
    pprint("testing GET  for showVnetByName http://%s/vRest/vnets/%s" % (switch, name))
    response = requests.get("http://%s/vRest/vnets/%s" % (switch, name), auth=(username, password))
    pprint("==============JSON=======")
    pprint(response.json())
    pprint("=============")
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) != 0
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    v.deleteVnet(name)






def test_FailureAuthorizationupdateVnetByName(switch):
    """
           
    """
    test_vnet=testVnet % random.randint(0, 20000)
    pprint("testing Failed authentication  for updateVnetByName http://%s/vRest/vnets/%s" % (switch, test_vnet))
    response = requests.get("http://%s/vRest/vnets/%s" % (switch, test_vnet))
    assert response.status_code == 401


testdata = [  # restricted_resources,data_bw_min,data_bw_max,numflows, vlans,ports
    (testVnet % random.randint(0, 20000), "ports", 0, 0, 0, str(random.randint(0, 4090)), str(random.randint(2, 60)))
]


@pytest.mark.parametrize("name,restricted_resources,data_bw_min,data_bw_max,num_flows,vlans,managed_ports,", testdata)
def test_PUTupdateVnetByName(switch, name, restricted_resources, data_bw_min, data_bw_max, num_flows, vlans,
                             managed_ports):
    """
       
    """
    v = vnet(switch)
    v.createVNetForTesting(name)
    vlansBefore = [x['vlans'] for x in v.show() if x['name'] == str(name)]
    pprint("testing PUT  for updateVnetByName with url %s  and  payload  %s"%("http://%s/vRest/vnets/%s" % (switch, name) ,json.dumps({'vlans': vlans, 'managed-ports': managed_ports})  ))
    response = requests.put("http://%s/vRest/vnets/%s" % (switch, name), auth=(username, password),
                            data=json.dumps({'vlans': vlans, 'managed-ports': managed_ports}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliResp = [x for x in v.show() if x['name'] == name]
    vlansAfter = [x['vlans'] for x in v.show() if x['name'] == name][0]
    portsAfter = [x['managed-ports'] for x in v.show() if x['name'] == name][0]
    assert vlans == vlansAfter
    assert managed_ports == portsAfter
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    v.deleteVnet(name)


def test_FailureAuthorizationdeleteVnetByName(switch):
    """
           
    """
    test_vnet=testVnet % random.randint(0, 20000)
    pprint("testing Failed authentication  for deleteVnetByName  for   url  http://%s/vRest/vnets/%s" % (switch, test_vnet))
    response = requests.get("http://%s/vRest/vnets/%s" % (switch, test_vnet))
    assert response.status_code == 401


def test_FailureAuthorizationaddVnetPortByVnetName(switch):
    """
           
    """
    test_vnet=testVnet % random.randint(0, 20000)
    pprint("testing Failed authentication  for addVnetPortByVnetName  for   url  http://%s/vRest/vnets/%s/ports" % (switch, test_vnet))
    response = requests.get("http://%s/vRest/vnets/%s/ports" % (switch, test_vnet))
    assert response.status_code == 401


testdata = [  # vlans,ports
    (testVnet % random.randint(0, 20000), str(random.randint(2, 4000)), str(random.randint(2, 60)))
]


@pytest.mark.parametrize("vnet_name,vlans,portToAdd", testdata)
def test_POSTaddVnetPortByVnetName(switch, vnet_name, vlans, portToAdd):
    """
       
    """
    v = vnet(switch)
    v.createVNetForTesting(vnet_name)
    pprint("testing POST  for addVnetPortByVnetName for  url %s and   payload  %s" %("http://%s/vRest/vnets/%s/ports" % (switch, vnet_name)  ,json.dumps({'ports': portToAdd}) ))
    response = requests.post("http://%s/vRest/vnets/%s/ports" % (switch, vnet_name), auth=(username, password),
                             data=json.dumps({'ports': portToAdd}))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    lPortsAfter = [x['managed-ports'] for x in v.show() if x['name'] == vnet_name][0]

    cliResp = [x for x in v.show() if x['name'] == vnet_name]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliResp)
    pprint("=========END  OF CLI  OUTOUT =============")
    assert lPortsAfter == portToAdd
    v.deleteVnet(vnet_name)


def test_FailureAuthorizationremoveVnetPortByNameByPmap(switch):
    """
           
    """
    vnet_name , ports =testVnet % random.randint(0, 4090), random.randint(0, 40)
    pprint("testing Failed authentication  for removeVnetPortByNameByPmap with  http://%s/vRest/vnets/%s/ports/%d" % (switch,vnet_name ,ports ))
    response = requests.get(
            "http://%s/vRest/vnets/%s/ports/%d" % (switch,vnet_name ,ports ))
    assert response.status_code == 401


testdata = [  #
    (testVnet % random.randint(0, 20000), random.randint(2, 60))
]


@pytest.mark.parametrize("name,ports", testdata)
def test_DELETEremoveVnetPortByName(switch, name, ports):
    """
       
    """
    v = vnet(switch)
    v.createVnetAndAssociatePorts(name, ports)
    pprint("testing DELETE  for removeVnetPortByNameByPmap with  url  http://%s/vRest/vnets/%s/ports/%s" % (switch, name, ports))
    response = requests.delete("http://%s/vRest/vnets/%s/ports/%s" % (switch, name, ports),
                               auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    portsForVnet = [x['managed-ports'] for x in v.show() if x['name'] == name]
    assert ports not in portsForVnet
    v.deleteVnet(name)


testdata = [  #
    (testVnet % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_DELETEdeleteVnetByName(switch, name):
    """

    """
    v = vnet(switch)
    v.createVNetForTesting(name)
    pprint("testing DELETE  for deleteVnetByName with  url  http://%s/vRest/vnets/%s" % (switch, name) )
    response = requests.delete("http://%s/vRest/vnets/%s" % (switch, name), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert (len([x for x in v.show() if x['name'] == str(name)])) == 0



testdata = [  #
    ("1=1","Illegal value for name. Legal values are: letters, numbers, _, ., :, and -")
]


@pytest.mark.parametrize("name,message", testdata)
def test_DELETEshowVnetByNameErrorMessage(switch, name,message):
    """

        """
    v = vnet(switch)
    v.createVNetForTesting(name)
    pprint("testing DELETE  for showVnetByName http://%s/vRest/vnets/%s" % (switch, name))
    response = requests.delete("http://%s/vRest/vnets/%s" % (switch, name), auth=(username, password))
    pprint("==============JSON=======")
    pprint(response.json())
    pprint("=============")
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) != 0
    assert str(json.loads(response.text)["result"]["result"][0]["message"]) == message
    v.deleteVnet(name)




def test_teardown(switch):
    v = vnet(switch)
    v.cleanUpAllVnets()


