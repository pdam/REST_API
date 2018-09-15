import random

import py.test
import pytest

import sys

import time

from vflow import vflow

from fabric_node import fabric_node
from igmp_snooping import igmp_snooping
from igmp_static_group import igmp_static_group
from igmp_static_source import igmp_static_source
from switch_info import switch_info
from vflow_class import vflow_class
from vlag import vlag
from vlan import vlan

sys.path.append(".")
from switch_setup import switch_setup
from user import user
from port_config import port_config
from port_xcvr import port_xcvr
from port_stats import port_stats
from vlan_stats import vlan_stats
from l2_table import l2_table
from l2_setting import l2_setting
from lldp import lldp
import logging
import json
import requests
from pprint import pprint

username = "network-admin"
password = "test123"
ptype = ""


def getPlatform(switch):
    s = switch_info(switch)
    model = s.show()[0]['model']
    if "HDS" or "D2060" in model:
        return "nsu"
    elif "F64" in model:
        return "aquila"
    elif "F64" in model:
        return "leo"
    else:
        return "unknown"


def test_setup(switch):
    pass


def test_set_switch_name(switch):
    c = switch_setup(switch)
    logging.info("testing PUT  for updateSetup ")
    response = requests.put("http://%s/vRest/switch-setup" % (switch), auth=(username, password),
                            data=json.dumps({'switch-name': switch}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()[0]
    pprint(cliresponseListOfHashAfter)
    assert switch == cliresponseListOfHashAfter['switch-name']


testdata = [
    ("10.9.10.1")
]


@pytest.mark.parametrize("dns_ip", testdata)
def test_set_DNS_server(switch, dns_ip):
    c = switch_setup(switch)
    logging.info("testing PUT  for updateSetup ")
    response = requests.put("http://%s/vRest/switch-setup" % (switch), auth=(username, password),
                            data=json.dumps({'dns-ip': dns_ip}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()[0]
    pprint(cliresponseListOfHashAfter)
    assert dns_ip == cliresponseListOfHashAfter['dns-ip']


testdata = [
    ("Asia/Kolkata")
]


@pytest.mark.parametrize("timezone", testdata)
def test_set_time_zone(switch, timezone):
    c = switch_setup(switch)
    logging.info("testing PUT  for updateSetup ")
    response = requests.put("http://%s/vRest/switch-setup" % (switch), auth=(username, password),
                            data=json.dumps({'timezone': timezone}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()[0]
    pprint(cliresponseListOfHashAfter)
    assert timezone == cliresponseListOfHashAfter['timezone']


testdata = [
    ("ntp.ubuntu.com")
]


@pytest.mark.parametrize("ntp_server", testdata)
def test_set_ntp_server(switch, ntp_server):
    c = switch_setup(switch)
    logging.info("testing PUT  for updateSetup ")
    response = requests.put("http://%s/vRest/switch-setup" % (switch), auth=(username, password),
                            data=json.dumps({'ntp-server': ntp_server}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()[0]
    pprint(cliresponseListOfHashAfter)
    assert ntp_server == cliresponseListOfHashAfter['ntp-server']


testdata = [
    ("test_user%d" % random.randint(0, 20000), "test_password%d" % random.randint(0, 20000))
]


@pytest.mark.parametrize("uname,passwd", testdata)
def test_user_basic_administration(switch, uname, passwd):
    c = user(switch)
    logging.info("testing POST  for user creation ")
    response = requests.post("http://%s/vRest/users" % (switch), auth=(username, password),
                             data=json.dumps({"name": uname, "scope": "fabric", "password": passwd}))
    pprint(response.json())
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.show() if x['name'] == uname][0]
    pprint(cliresponseListOfHashAfter)
    assert uname == cliresponseListOfHashAfter['name']
    ## Update  the  password
    logging.info("testing PUT  for user updation ")
    response = requests.put("http://%s/vRest/users/%s" % (switch, uname), auth=(username, password),
                            data=json.dumps({"password": "n-%s" % passwd}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    ##Use  password   to login and  confirm  200
    logging.info("testing REST api  using user  credentials  ")
    response = requests.get("http://%s/vRest/users/" % (switch), auth=(uname, "n-%s" % passwd))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"


def test_User_Roles_Handling(switch):
    pass


def test_TACACS_Administration(switch):
    name = "name-%d"%(random.randint(2,100000))
    payload ={
          "name": name,
          "scope": "local",
          "server": "1.2.3.4",
          "port": random.randint(2,1000),
          "secret": "secret"
    }
    response = requests.post("http://%s/vRest/aaa-tacacs"%(switch) , auth=(username , password), data =json.dumps(payload))
    print  response.json()
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    response = requests.delete("http://%s/vRest/aaa-tacacs/%s"%(switch,name) , auth=(username , password))
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_TACACS_List(switch):
    name = "name-%d"%(random.randint(2,100000))
    payload ={
          "name": name,
          "scope": "local",
          "server": "1.2.3.4",
          "port": random.randint(2,1000),
          "secret": "secret"
    }
    response = requests.post("http://%s/vRest/aaa-tacacs"%(switch) , auth=(username , password), data =json.dumps(payload))
    print  response.json()
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    ##Check now
    response = requests.get("http://%s/vRest/aaa-tacacs/name"%(switch) , auth=(username , password))
    print  response.json()
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"




def test_Reboot(switch):
    pass


def test_Configuration_reset(switch):
    pass


def test_Management_IP_address(switch):
    c = fabric_node(switch)
    mgmt_ip = [x['mgmt-ip'] for x in c.show() if x['name'] == switch][0]
    response = requests.get("http://%s/vRest/fabric-nodes" % switch, auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    rest_mgmt_ip = [x['mgmt-ip'] for x in json.loads(response.text)["data"] if x['name'] == switch][0]
    assert rest_mgmt_ip == mgmt_ip



def test_Export_import_configuration(switch):
    payload ={
        "export-file": "conf.tgz"
    }
    response = requests.post("http://%s/vRest/switch-configs/export"%(switch) , auth=(username , password), data =json.dumps(payload))
    print  response.json()
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    ##Check now
    response = requests.get("http://%s/vRest/switch-configs"%(switch) , auth=(username , password))
    print  response.json()
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert "conf.tgz" in json.loads(response.text)["data"][0]["export-file"]




@pytest.mark.skip(reason=None)
def test_sW_Upgrade(switch):
    pass


@pytest.mark.skip(reason=None)
def test_show_Running_Configuration(switch):
    pass



def test_Admin_Syslog(switch):
    response = requests.post("http://%s/vRest/admin-syslogs" % (switch), auth=(username, password), data=json.dumps(
            {'message-format': 'structured', 'scope': 'local', 'host': '1.2.3.4', 'name': 'name', 'port': 512 }))
    print response.json()
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    response = requests.delete("http://%s/vRest/admin-syslogs/name" % (switch), auth=(username, password))
    print response.json()
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_Log_events(switch):
    response = requests.get("http://%s/vRest/log-events" % (switch), auth=(username, password))
    print response.json()
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert str(json.loads(response.text)["data"]) !=  ""



def test_Admin_Services(switch):
    response = requests.get("http://%s/vRest/admin-services" % (switch), auth=(username, password))
    print response.json()
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert json.loads(response.text)["data"][0]["web"] == True


def test_port_enable_disable(switch):
    c = port_config(switch)
    ptouse = [x for x in c.show()][20]['port']
    logging.info("disable port  ")
    response = requests.put("http://%s/vRest/port-configs/%s" % (switch, ptouse), auth=(username, password),
                            data=json.dumps({"enable": "disable"}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliPort = [x for x in c.show() if x['port'] == ptouse][0]
    pprint(cliPort)
    assert cliPort["enable"] == "off"
    logging.info("enable port ")
    response = requests.put("http://%s/vRest/port-configs/%s" % (switch, ptouse), auth=(username, password),
                            data=json.dumps({"enable": "enable"}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliPort = [x for x in c.show() if x['port'] == ptouse][0]
    pprint(cliPort)
    assert cliPort["enable"] == "on"


def test_Port_auto_negotioation(switch):
    c = port_config(switch)
    ptouse = [x for x in c.show()][20]['port']
    logging.info("disable autoneg  on port  ")
    response = requests.put("http://%s/vRest/port-configs/%s" % (switch, ptouse), auth=(username, password),
                            data=json.dumps({"autoneg": "no-autoneg"}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliPort = [x for x in c.show() if x['port'] == ptouse][0]
    pprint(cliPort)
    assert cliPort["autoneg"] == "off"

    logging.info("enable autoneg on port ")
    response = requests.put("http://%s/vRest/port-configs/%s" % (switch, ptouse), auth=(username, password),
                            data=json.dumps({"autoneg": "autoneg"}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliPort = [x for x in c.show() if x['port'] == ptouse][0]
    pprint(cliPort)
    assert cliPort["autoneg"] == "on"


def test_port_speed(switch):
    c = port_config(switch)
    ptouse = [x for x in c.show()][10]['port']
    pspeed = [x for x in c.show()][10]['speed']
    logging.info("setting speed  on port  ")
    response = requests.put("http://%s/vRest/port-configs/%s" % (switch, ptouse), auth=(username, password),
                            data=json.dumps({"api.speed": pspeed}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliPort = [x for x in c.show() if x['port'] == ptouse][0]
    pprint(cliPort)
    assert cliPort["speed"] == pspeed


def test_jumbo_frames(switch):
    c = port_config(switch)
    ptouse = [x for x in c.show()][10]['port']
    logging.info("disable jumbo  on port  ")
    response = requests.put("http://%s/vRest/port-configs/%s" % (switch, ptouse), auth=(username, password),
                            data=json.dumps({"jumbo": "no-jumbo"}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliPort = [x for x in c.show() if x['port'] == ptouse][0]
    pprint(cliPort)
    assert cliPort["jumbo"] == "off"
    logging.info("enable jumbo on port ")
    response = requests.put("http://%s/vRest/port-configs/%s" % (switch, ptouse), auth=(username, password),
                            data=json.dumps({"jumbo": "jumbo"}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliPort = [x for x in c.show() if x['port'] == ptouse][0]
    pprint(cliPort)
    assert cliPort["jumbo"] == "on"


def test_Transceiver_information(switch):
    c = port_xcvr(switch)
    plist = [(x['part-number'], x['port'], x['serial-number']) for x in c.show()]
    logging.info("get  a  list of  xcvr  ports ")
    response = requests.get("http://%s/vRest/port-xcvrs?api.switch=fabric" % switch, auth=(username, password))
    pprint(response.json())
    plistRest = [(x['part-number'], str(x['port']), x['serial-number']) for x in json.loads(response.text)["data"]]
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plist


def test_port_statistics(switch):
    c = port_stats(switch)
    plist = [(x['port']) for x in c.show()]
    logging.info("get  a  list of    port statistics ")
    response = requests.get("http://%s/vRest/port-stats?api.switch=fabric" % switch, auth=(username, password))
    pprint(response.json())
    plistRest = [(x['port']) for x in json.loads(response.text)["data"]]
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plist





def test_Display_all_VLANs(switch):
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


def test_Display_one_VLAN(switch):
    c = vlan(switch)
    id = random.randint(5, 4090)
    c.createVlanForTesting(id)
    pprint("testing GET  for showVlanByIdent with url  http://%s/vRest/vlans/%s" % (switch, id))
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


def test_Display_vlan_statistics(switch):
    c = vlan_stats(switch)
    plist = [x['vlan'] for x in c.show()]
    logging.info("get  a  list of    port statistics ")
    response = requests.get("http://%s/vRest/vlan-stats?api.switch=fabric" % switch, auth=(username, password))

    pprint(response.json())
    plistRest = [str(x['vlan']) for x in json.loads(response.text)["data"]]
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plist


testdata = [  # id,scope,ports
    (random.randint(4, 4000), "local", "20,21,22,23,24,25")
]


@pytest.mark.parametrize("id,scope,ports", testdata)
def test_POSTcreateVlan(switch, id, scope, ports):
    """

    """
    c = vlan(switch)
    description = "descVlan-%d" % id
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





testdata = [
    (random.randint(4, 4000))
]


@pytest.mark.parametrize("id", testdata)
def test_DELETEVlan(switch, id):
    """

    """
    c = vlan(switch)
    c.createVlanForTesting(id)
    pprint("testing DELETE  for deleteVlanByIdent with url  http://%s/vRest/vlans/%d" % (switch, id))
    response = requests.delete("http://%s/vRest/vlans/id/%d" % (switch, id), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert (len([x for x in c.show() if x['id'] == str(id)])) == 0




def test_show_L2_tables(switch):
    c = l2_table(switch)
    plist = [(x['mac'], x['vlan']) for x in c.show()].sort()
    pprint(plist)
    logging.info("get  a  list of  l2 settings")
    response = requests.get("http://%s/vRest/l2-tables" % switch, auth=(username, password))
    pprint(response.json())
    plistRest = [(x['mac'], str(x['vlan'])) for x in
                 json.loads(response.text)["data"]].sort()
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plist



def test_Flush_L2_table(switch):
    response = requests.post("http://%s/vRest/l2-tables/flush" % switch, auth=(username, password),
                            data=json.dumps({}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_Update_L2_setting(switch):
    c = l2_setting(switch)
    plistbefore = [x['aging-time(s)'] for x in c.show()]
    pprint(plistbefore)
    logging.info("get  aging time setting of l2-settings")
    response = requests.put("http://%s/vRest/l2-setting?api.switch=fabric" % switch, auth=(username, password),
                            data=json.dumps({"aging-time": "200"}))
    pprint(response.json())
    plistafter = [x['aging-time(s)'] for x in c.show()]
    pprint(plistafter)
    assert plistbefore != plistafter
    logging.info("get  a  list of l2-settings ")
    response = requests.get("http://%s/vRest/l2-setting?api.switch=fabric" % switch, auth=(username, password))
    plistRest = [str(x['aging-time']) for x in json.loads(response.text)["data"]]
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plistafter
    response = requests.put("http://%s/vRest/l2-setting?api.switch=fabric" % switch, auth=(username, password),
                            data=json.dumps({"aging-time": "300"}))
    pprint(response.json())
    response = requests.get("http://%s/vRest/l2-setting?api.switch=fabric" % switch, auth=(username, password))
    plistRest = [str(x['aging-time']) for x in json.loads(response.text)["data"]]
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plistbefore


testdata = [  # failover_move_L2,name,lacp_mode,peer_switch,mode,lacp_timeout,port,peer_port
    ("testVlag-%d" % random.randint(0, 200000), 'slow', 'active-standby', 16, 'active-standby', 'slow', 34, 34)
]


@pytest.mark.parametrize("name,failover_move_L2,lacp_mode,peer_switch,mode,lacp_timeout,port,peer_port", testdata)
def test_CreateVlag(switch, name, failover_move_L2, lacp_mode, peer_switch, mode, lacp_timeout, port, peer_port):
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


@pytest.mark.skip(reason=None)
def test_Load_Sharing(switch):
    pass


@pytest.mark.skip(reason=None)
def test_static_link_aggregation(switch):
    pass


@pytest.mark.skip(reason=None)
def test_LAG_with_LACP(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_LAG_mode(switch):
    pass



def test_set_LACP_system_priority(switch):
    payload = {
    "enable": 'false',
    "system-priority": 10
    }
    response = requests.put("http://%s/vRest/lacp" % (switch), auth=(username, password), data=json.dumps(payload))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"





def test_show_LACP_for_ports(switch):
    response = requests.get("http://%s/vRest/lacp-port-stats-settings" % (switch), auth=(username, password))
    pprint("=========JSON  OUTOUT =============")
    pprint(response.json())
    pprint("=========END  OF  JSON  OUTOUT =============")
    assert str(response.status_code) == "200"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert str(json.loads(response.text)["data"]) != ""




def test_show_LLDP_port(switch):
    c = lldp(switch)
    plistbefore = [(x['local-port'], x['chassis-id'], x['port-id'], x['port-desc'], x['port-vlan-id'], x['sys-name'],
                    x['ttl'], x['system-cap'], x['system-cap-enabled'], x['max-frame-size']) for x in c.show()]
    pprint(plistbefore)
    logging.info("get list of LLDP ports")
    response = requests.get("http://%s/vRest/lldps?api.switch=fabric" % switch, auth=(username, password))
    plistRest = [(str(x['local-port']), x['chassis-id'], x['port-id'], x['port-desc'], str(x['port-vlan-id']),
                  x['sys-name'], str(x['ttl']), x['system-cap'], x['system-cap-enabled'], str(x['max-frame-size'])) for
                 x in json.loads(response.text)["data"]]
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plistbefore


def test_show_LLDP_ports(switch):
    c = lldp(switch)
    plistbefore = [x['port-id'] for x in c.show()]
    pChoose = plistbefore[len(plistbefore) - 2]
    pprint(pChoose)
    logging.info("get list of LLDP ports")
    response = requests.get("http://%s/vRest/lldps/port-id/%s?api.switch=fabric" % (switch, pChoose),
                            auth=(username, password))
    plist = [(
                 x['local-port'], x['chassis-id'], x['port-id'], x['port-desc'], x['port-vlan-id'], x['sys-name'],
                 x['ttl'],
                 x['system-cap'], x['system-cap-enabled'], x['max-frame-size']) for x in c.show() if
             x['port-id'] == pChoose]
    pprint(plist)
    plistRest = [(str(x['local-port']), x['chassis-id'], x['port-id'], x['port-desc'], str(x['port-vlan-id']),
                  x['sys-name'], str(x['ttl']), x['system-cap'], x['system-cap-enabled'], str(x['max-frame-size'])) for
                 x in json.loads(response.text)["data"]]
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plist




def test_set_IGMP_snooping(switch):
    c = igmp_snooping(switch)
    dbool = {'no': 'False', 'yes': 'True'}
    response = requests.put("http://%s/vRest/igmp-snooping" % switch, auth=(username, password),
                            data=json.dumps({"enable": "false"}))
    plistbefore = [dbool[x['enable']] for x in c.show()]
    logging.info("get igmp-snooping state")
    response = requests.get("http://%s/vRest/igmp-snooping?api.switch=fabric" % switch, auth=(username, password))
    plistRest = [str(x['enable']) for x in json.loads(response.text)["data"]]
    pprint(plistRest)
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plistbefore
    response = requests.delete("http://%s/vRest/igmp-snooping" % switch, auth=(username, password),
                               data=json.dumps({"enable": "true"}))
    plistbefore = [dbool[x['enable']] for x in c.show()]
    logging.info("get igmp-snooping state after modifying it to true")
    response = requests.get("http://%s/vRest/igmp-snooping?api.switch=fabric" % switch, auth=(username, password))
    plistRest = [str(x['enable']) for x in json.loads(response.text)["data"]]
    pprint(plistRest)
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    assert plistRest == plistbefore





def test_STP(switch):
    response = requests.get("http://%s/vRest/stp" % (switch), auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



testdata = [
    ("test_class%d" % random.randint(0, 20000), random.randint(1, 7))
]


@pytest.mark.parametrize("name,priority", testdata)
def test_Vflow_class_create(switch, name, priority):
    c = vflow_class(switch)
    logging.info("testing POST  for vflow creation ")
    response = requests.post("http://%s/vRest/vflow-classes" % (switch), auth=(username, password),
                             data=json.dumps({
                                 "name": name,
                                 "scope": "fabric",
                                 "priority": priority
                             }))
    pprint(response.json())
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.show() if x['name'] == name][0]
    pprint(cliresponseListOfHashAfter)
    assert name == cliresponseListOfHashAfter['name']
    assert str(priority) == cliresponseListOfHashAfter['priority']


def test_Vflow_class_show(switch):
    c = vflow_class(switch)
    logging.info("testing POST  for vflow creation ")
    response = requests.get("http://%s/vRest/vflow-classes" % (switch), auth=(username, password))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    plistRest = [(str(x['name']), str(x['type']), str(x['priority']), str(x['cos'])) for x in
                 json.loads(response.text)["data"]]
    cliresponse = [(x['name'], x['type'], x['priority'], x['cos']) for x in c.show()]
    pprint(cliresponse)
    assert plistRest == cliresponse


testdata = [
    ("test_class%d" % random.randint(0, 20000), random.randint(1, 7))
]


@pytest.mark.parametrize("name,priority", testdata)
def test_Vflow_class_delete(switch, name, priority):
    c = vflow_class(switch)
    logging.info("testing POST  for vflow creation ")
    response = requests.post("http://%s/vRest/vflow-classes" % (switch), auth=(username, password),
                             data=json.dumps({
                                 "name": name,
                                 "scope": "fabric",
                                 "priority": priority
                             }))
    response = requests.delete("http://%s/vRest/vflow-classes/%s" % (switch, name), auth=(username, password))
    cliresponse = [(x['name'], x['type'], x['priority'], x['cos']) for x in c.show() if x['name'] == name]
    assert len(cliresponse) == 0


testdata = [
    ("test_flow%d" % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_Vflow_create_show(switch, name):
    c = vflow(switch)
    logging.info("testing POST  for vflow creation ")
    response = requests.post("http://%s/vRest/vflows" % (switch), auth=(username, password),
                             data=json.dumps({
                                 "name": name,
                                 "scope": "fabric",
                                 "vlan": 10,
                                 "tos": 11,
                                 "action": "to-cpu"
                             }))
    response = requests.get("http://%s/vRest/vflows/name/%s" % (switch, name), auth=(username, password))
    print str(json.loads(response.text))
    plistRest = [str(x['name']) for x in json.loads(response.text)["data"]][0]
    assert plistRest == name
    response = requests.delete("http://%s/vRest/vflows/name/%s" % (switch, name), auth=(username, password))
    assert response.status_code == 200

    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"


testdata = [
    ("test_flow%d" % random.randint(0, 20000), random.randint(10, 4000))
]


@pytest.mark.parametrize("name,vlan", testdata)
def test_Vflow_modify(switch, name, vlan):
    c = vflow(switch)
    pprint(name)
    logging.info("testing POST  for vflow creation ")
    response = requests.post("http://%s/vRest/vflows" % (switch), auth=(username, password),
                             data=json.dumps({
                                 "name": name,
                                 "scope": "fabric",
                                 "vlan": vlan,
                                 "tos": 11,
                                 "action": "to-cpu"
                             }))
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponse = [x['vlan'] for x in c.show(name) if x['name'] == name][0]
    response = requests.put("http://%s/vRest/vflows/%s" % (switch, name), auth=(username, password),
                            data=json.dumps({
                                "vlan-pri": 4
                            }))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    response = requests.delete("http://%s/vRest/vflows/name/%s" % (switch, name), auth=(username, password)
                               )
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"


testdata = [
    ("test_flow%d" % random.randint(0, 20000), random.randint(10, 4000))
]


@pytest.mark.parametrize("name,vlan", testdata)
def test_Vflow_delete(switch, name, vlan):
    c = vflow(switch)
    pprint(name)
    logging.info("testing POST  for vflow creation ")
    response = requests.post("http://%s/vRest/vflows" % (switch), auth=(username, password),
                             data=json.dumps({
                                 "name": name,
                                 "scope": "fabric",
                                 "vlan": vlan,
                                 "tos": 11,
                                 "action": "to-cpu"
                             }))
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponse = [x['vlan'] for x in c.show(name) if x['name'] == name][0]
    response = requests.delete("http://%s/vRest/vflows/name/%s" % (switch, name), auth=(username, password)
                               )
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_Vflow_stats_settings_show(switch):
    payload = {
          "enable": "false",
          "interval": 1,
          "disk-space": 10
    }
    response = requests.get("http://%s/vRest/vflow-stats-settings" % (switch), auth=(username, password)
                               )
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_Vflow_stats_settings_modify(switch):
    payload = {
          "enable": "false",
          "interval": 1,
          "disk-space": 10
    }
    response = requests.put("http://%s/vRest/vflow-stats-settings" % (switch), auth=(username, password), data=json.dumps(payload)
                               )
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_Vflow_stats_show(switch):
    response = requests.get("http://%s/vRest/vflow-stats" % (switch), auth=(username, password)
                               )
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_set_mirroring(switch):
    payload = {
      "name": "mirror",
      "out-port": "10",
      "in-port": "11"
    }
    logging.info("testing POST  for vflow creation ")
    response = requests.post("http://%s/vRest/mirrors" % (switch), auth=(username, password),
                             data=json.dumps(payload))
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"

    response = requests.delete("http://%s/vRest/mirrors/mirror" % (switch), auth=(username, password)
                               )
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"



def test_Display_mirroring(switch):
    pass





@pytest.mark.skip(reason=None)
def test_Modify_VNET_to_add_ports(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_VNET_to_add_restricted_ports(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_all_VNETs(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Traffic_shaping_create_modify_delete_vFlow(switch):
    pass


@pytest.mark.skip(reason=None)
def test_show_QoS_classes(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_flow_classes(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_delete_VRG(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Get_clients_of_VRG(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Assign_delete_ports_to_VRG(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_VRG(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Configure_vlan_in_fabric(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_vlan_in_fabric(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Delete_vlan_from_fabric(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Port_statistics(switch):
    pass


@pytest.mark.skip(reason=None)
def test_set_switch_name(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_primary_secondary_DNS(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_time_zone(switch):
    pass


@pytest.mark.skip(reason=None)
def test_set_NTP_server(switch):
    pass


testdata = [
    ("test_user%d" % random.randint(0, 20000), "test_pass%d" % random.randint(1, 7000))
]


@pytest.mark.parametrize("uname,passwd", testdata)
def test_Create_user(switch, uname, passwd):
    c = user(switch)
    logging.info("testing POST  for user creation ")
    response = requests.post("http://%s/vRest/users" % (switch), auth=(username, password),
                             data=json.dumps({"name": uname, "scope": "fabric", "password": passwd}))
    pprint(response.json())
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.show() if x['name'] == uname][0]
    pprint(cliresponseListOfHashAfter)
    assert uname == cliresponseListOfHashAfter['name']


testdata = [
    ("test_user%d" % random.randint(0, 20000), "test_pass%d" % random.randint(1, 7000))
]


@pytest.mark.parametrize("uname,passwd", testdata)
def test_Modify_user(switch, uname, passwd):
    c = user(switch)
    logging.info("testing POST  for user creation ")
    response = requests.post("http://%s/vRest/users" % (switch), auth=(username, password),
                             data=json.dumps({"name": uname, "scope": "fabric", "password": passwd}))
    pprint(response.json())
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [x for x in c.show() if x['name'] == uname][0]
    pprint(cliresponseListOfHashAfter)
    assert uname == cliresponseListOfHashAfter['name']
    ## Update  the  password
    logging.info("testing PUT  for user updation ")
    response = requests.put("http://%s/vRest/users/%s" % (switch, uname), auth=(username, password),
                            data=json.dumps({"password": "n-%s" % passwd}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    ##Use  password   to login and  confirm  200
    logging.info("testing REST api  using user  credentials  ")
    response = requests.get("http://%s/vRest/users/" % (switch), auth=(uname, "n-%s" % passwd))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"


testdata = [
    ("test_user%d" % random.randint(0, 20000), "test_pass%d" % random.randint(1, 7000))
]


@pytest.mark.parametrize("uname,passwd", testdata)
def test_Display_user(switch, uname, passwd):
    c = user(switch)
    logging.info("testing POST  for user creation ")
    response = requests.post("http://%s/vRest/users" % (switch), auth=(username, password),
                             data=json.dumps({"name": uname, "scope": "fabric", "password": passwd}))
    pprint(response.json())
    assert response.status_code == 201
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    response = requests.get("http://%s/vRest/users/%s" % (switch, uname), auth=(username, password))
    jsonData = [x for x in json.loads(response.text)["data"] if x['name'] == uname][0]
    pprint(jsonData)
    assert len(jsonData) != 0


@pytest.mark.skip(reason=None)
def test_IP_pool_creation(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DHCP_service_creation(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DHCP_pool_update(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DHCP_leases_display(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DHCP_status_update(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DHCP_service_display(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DHCP_service_delete(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DNS_service_creation(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DNS_interface_add(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DNS_domain_add(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DNS_record_add(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DNS_service_display(switch):
    pass


@pytest.mark.skip(reason=None)
def test_DNS_service_delete(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Vnet_Mgr_interface_create(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Vnet_Mgr_services_management(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Vnet_Mgr_display(switch):
    pass


@pytest.mark.skip(reason=None)
def test_VPORT_display(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_IP_ACL_and_verify_traffic_allowing(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_IP_ACL_deny_and_verify_traffic_denial(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Delete_ACL_IP(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Modify_ACL_IP(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Display_ACL_IP(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Create_ACL_IP(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Create_ACL_MAC(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Display_ACL_MAC(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Modify_ACL_MAC(switch):
    pass


@pytest.mark.skip(reason=None)
def test__Delete_ACL_MAC(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_L2_MAC_ACL_deny_and_verify_traffic_denial(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_L2_MAC_ACL_permit_and_verify_traffic_allowing(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_vport(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_vports_with_path_arguments(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Clear_port_statistics(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_vports(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_connection_latencies(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Clear_all_connection_stats(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Clear_connection_stats(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_connections_statistics(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_connections(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Clear_connections(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Clear_all_connections(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_SNMP_user(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_SNMP_user_password_is_below_the_length(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_SNMP_Community(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_SNMP_communities(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_SNMP_community(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Delete_SNMP_Community(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Enable_SNMP_traps(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_enabled_SNMP_traps(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_V1_V2_SNMP_trap_sink(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_V1_V2_SNMP_trap_sink(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_V1_V2_SNMP_trap_sink(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Delete_V1_V2_SNMP_trap_sink(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Delete_SNMP_users(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_SNMP_user(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_SNMP_user(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Define_V3_SNMP_trap_sink(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Delete_V3_SNMP_trap_sink(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_V3_SNMP_trap_sink(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_V3_SNMP_trap_sink(switch):
    pass


def test_Display_SNMP_engine_ID(switch):
    response = requests.get("http://%s/vRest/snmp-engineid" % switch, auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    engineid = [str(x['engineid']) for x in json.loads(response.text)["data"]][0]
    pprint(engineid)
    assert engineid != ""


@pytest.mark.skip(reason=None)
def test_show_OpenStack_Configuration_List(switch):
    pass


@pytest.mark.skip(reason=None)
def test_show_OpenStack_Configuration(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Create_OpenStack_Configuration(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Delete_OpenStack_Configuration(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Modify_OpenStack_Configuration(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Install_OpenStack_Plugins(switch):
    pass


@pytest.mark.skip(reason=None)
def test_show_OpenStack_Nodes(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Get_Routes_connected_type(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Get_Routes_static_type(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Get_Routes_resource_network(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Get_Routes_filter_network(switch):
    pass


def test_Get_Routes_filter_type(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Get_Routes_empty(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Create_SW_vRouter(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Create_HW_vRouter(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_available_boot_environments_explicitly_after_rolling_fabric_upgrade(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Display_available_boot_environments(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Rollback_booting_to_older_BE(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Validate_api_docs_schema_for_bootenvs(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Delete_boot_environment(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Create_vLAG_with_mandatory_parameters_only(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Create_vLAG_active_active_with_different_LACP_params(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Create_vLAG_active_standby_with_different_LACP_params(switch):
    pass


@pytest.mark.skip(reason=None)
def test_ErrCase_Create_vLAG_with_incorrect_params(switch):
    pass


@pytest.mark.skip(reason=None)
def test_ErrCase_Create_vLAG_with_incorrect_ports(switch):
    pass


@pytest.mark.skip(reason=None)
def test_ErrCase_Update_vLAG_with_lacp_mode(switch):
    pass


@pytest.mark.skip(reason=None)
def test_api_switch_query_in_REST_API(switch):
    pass


@pytest.mark.skip(reason=None)
def test_VNET_manager_interface(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Limit_test_to_check_VNET_number(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Assign_ports_to_VNET_with_empty_VLAN_tag(switch):
    pass


@pytest.mark.skip(reason=None)
def test_Import_switch_config_after_reset_with_fabric_join(switch):
    pass


@pytest.mark.skip(reason=None)
def test_create_VNET_without_any_VLAN_specified(switch):
    pass


@pytest.mark.skip(reason=None)
def test_perform_fabric_upgrade(switch):
    pass


@pytest.mark.skip(reason=None)
def test_TLS_1_2_support_on_REST_API_vManage(switch):
    pass


@pytest.mark.skip(reason=None)
def test_PTP_boundary_clock_configuration(switch):
    pass


@pytest.mark.skip(reason=None)
def test_stressing_HTTP_GET_valid_requests(switch):
    pass


@pytest.mark.skip(reason=None)
def test_stressing_HTTP_GET_not_existing_resource(switch):
    pass


@pytest.mark.skip(reason=None)
def test_stressing_HTTP_GET_valid_requests_in_fabric_scope(switch):
    pass
