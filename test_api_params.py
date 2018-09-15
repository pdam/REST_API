import  requests
from pprint import pprint
import json

username = "network-admin"
password = "test123"

def test_ApiSwitch(switch):
    """
    Get switch  ids  for  a   fabric  and  then use the  current  switch ID to make  the  same call this   time  using api.switch
    get switch id from the  call using  api.switch  and  compare both .
    """
    response = requests.get("http://%s/vRest/fabric-nodes"%switch , auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    switch_id= [ x['id']  for  x in json.loads(response.text)["data"] if x['name'] == switch ][0]
    pprint(switch_id)
    response = requests.get("http://%s/vRest/fabric-nodes?api.switch=%s"%(switch,switch_id) , auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    switch_id_from_apiswitch= [ x['id']  for  x in json.loads(response.text)["data"] if x['name'] == switch  ][0]
    pprint(switch_id_from_apiswitch)
    assert switch_id_from_apiswitch == switch_id


def test_ApiList(switch):
    """
    Get a  list  of  all  ports  . Filter  the first  5 .
    Use  the  filtered  list of first 5   and  pass   to ports  api   with   api.list control param
    Compare  ports got  with  the 5  ports  passed

    :param switch:
    :return:
    """
    response = requests.get("http://%s/vRest/ports"%switch , auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    ports= [ x['port']  for  x in json.loads(response.text)["data"]]
    pList= ",".join(ports[0:5])
    pprint(pList)
    response = requests.get("http://%s/vRest/ports?api.list=%s"%(switch,pList) , auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    portListF= [ x['port']  for  x in json.loads(response.text)["data"]]
    pprint(portListF)
    assert len(portListF)==ports


