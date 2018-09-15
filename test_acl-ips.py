import random
import sys
import pytest
sys.path.append(".")
import requests
import json
from acl_ip import acl_ip
from pprint  import pprint
import logging

def logAssert(test,msg):
    if not test:
        logging.error(msg)
        assert test,msg

username="network-admin"
password="test123"
testAclIP="restAclIp-%d"
test_src_ip="172.16.%d.4"
test_dst_ip="172.16.%d.66"
attributeList=[u'src-ip-mask',
                 u'vlan',
                 u'name',
                 u'proto',
                 u'dst-port',
                 u'src-ip',
                 u'dst-ip-mask',
                 u'port',
                 u'vnet-id',
                 u'id',
                 u'src-port',
                 u'dst-ip',
                 u'action',
                 u'scope']
def test_FailureAuthorizationcreateIpAcl(switch):
        """

        """
        logging.info("testing Failed authentication  for createIpAcl ")
        response = requests.get("http://%s/vRest/acl-ips"%switch )
        assert response.status_code == 401



testdata = [ # src_ip_mask,name,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,action,scope,dst_ip,port
               (testAclIP%random.randint(2,200), 0, 'ip', 0, 0, 0, str(test_src_ip%random.randint(2,200)), 41, 'permit', 'fabric', str(test_dst_ip%random.randint(2,200)), 0)
        ]

@pytest.mark.parametrize("name,src_ip_mask,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,action,scope,dst_ip,port", testdata)
def test_POSTcreateIpAcl(switch,name,src_ip_mask,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,action,scope,dst_ip,port):
    """

    """
    a=acl_ip(switch)
    logging.info("testing POST  for createIpAcl ")
    payload = { 'src-ip-mask' : src_ip_mask , 'name' : name, 'api.proto' : proto , 'vlan' : vlan , 'src-port' : src_port, 'dst-ip-mask' : dst_ip_mask, 'src-ip' : src_ip, 'dst-port' : dst_port, 'action' : 'permit' , 'scope' : 'fabric', 'dst-ip' : dst_ip , 'port' : port}
    response = requests.post("http://%s/vRest/acl-ips"%(switch) , auth=(username , password), data=json.dumps(payload))
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliobj = [ x  for x  in  a.show() if   x['name'] == name  ][0]
    pprint("=========CLI  OUTOUT =============")
    pprint(cliobj)
    pprint("=========END  OF CLI  OUTOUT =============")
    assert  cliobj['action'] == action
    assert  cliobj['src-ip'] == src_ip
    assert  cliobj['src-ip-mask'] == str(src_ip_mask)
    assert  cliobj['dst-ip'] == dst_ip
    assert  cliobj['dst-ip-mask'] == str(dst_ip_mask)





def test_FailureAuthorizationshowIpAcls(switch):
        """

        """
        logging.info("testing Failed authentication  for showIpAcls ")
        response = requests.get("http://%s/vRest/acl-ips"%switch )
        assert response.status_code == 401





testdata = [ #
    (testAclIP%random.randint(0,20000) ,  test_src_ip%random.randint(4,200) , test_dst_ip%random.randint(4,200))
        ]
@pytest.mark.parametrize("name,src_ip,dst_ip", testdata)
def test_GETshowIpAcls(switch,name,src_ip,dst_ip):
        """

        """
        c=acl_ip(switch)
        c.create(name , src_ip , dst_ip)
        logging.info("testing GET  for showIpAcls ")
        response = requests.get("http://%s/vRest/acl-ips"%(switch) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
        cliresponseHash = c.show()
        jsonResponseDat=json.loads(response.text)["data"]
        pprint("=========CLI  OUTOUT =============")
        pprint(cliresponseHash)
        pprint("=========END  OF CLI  OUTOUT =============")
        pprint("=========JSON  OUTOUT =============")
        pprint(jsonResponseDat)
        pprint("=========END  OF JSON  OUTOUT =============")
        assert len(cliresponseHash) == len(jsonResponseDat)


def test_FailureAuthorizationshowIpAclByName(switch):
        """

        """
        logging.info("testing Failed authentication  for showIpAclByName ")
        response = requests.get("http://%s/vRest/acl-ips/name/{name}"%switch )
        assert response.status_code == 401






testdata = [ #
    (testAclIP%random.randint(0,20000))
        ]
@pytest.mark.parametrize("name", testdata)
def test_GETshowIpAclByName(switch,name):
        """

        """
        c=acl_ip(switch)
        c.createACLIPForTesting(name)
        logging.info("testing GET  for showIpAclByName ")
        response = requests.get("http://%s/vRest/acl-ips/name/%s"%(switch ,name) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["data"]) != ""
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
        jsonResponseDat=json.loads(response.text)["data"][0]
        pprint(jsonResponseDat.keys())
        assert  attributeList.sort() ==jsonResponseDat.keys().sort()


def test_FailureAuthorizationupdateIpAclByName(switch):
        """

        """
        logging.info("testing Failed authentication  for updateIpAclByName ")
        response = requests.get("http://%s/vRest/acl-ips/name/%s"%(switch,testAclIP%random.randint(0,20000) ))
        assert response.status_code == 401






testdata = [ # acl_name ,src_ip_mask,name,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,action,scope,dst_ip,port
               (testAclIP%random.randint(0,20000),0, 'ip', 0, 0, 0, test_dst_ip%random.randint(5,230), 'deny', 41 ,  test_src_ip%random.randint(5,230), 0)
        ]

@pytest.mark.parametrize("acl_name,src_ip_mask,proto,vlan,src_port,dst_ip_mask,src_ip,action,dst_port,dst_ip,port", testdata)
def test_PUTupdateIpAclByName(switch,acl_name,src_ip_mask,dst_ip,proto,vlan,src_port,dst_ip_mask,src_ip,action,dst_port,port):
    """

    """
    c=acl_ip(switch)
    c.create(acl_name , src_ip , dst_ip)
    testAclIPId=c.getAclId(acl_name)
    pprint(testAclIPId)
    actionBefore = [ x['action']  for  x in  c.show()  if   x['name'] ==str(acl_name)]
    logging.info("testing PUT  for updateIpAclByName ")
    payload={  'action' : action }
    pprint(str(payload))
    response = requests.put("http://%s/vRest/acl-ips/name/%s"%(switch ,acl_name) , auth=(username , password) , data=json.dumps(payload))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    actionAfter =  [ x['action']  for  x in  c.show() if x['name'] == str(acl_name)][0]
    assert actionAfter == action


def test_GETshowIpAclByIdent(switch):
        """

        """
        c=acl_ip(switch)
        acl_ip_name = testAclIP%random.randint(0,20000)
        c.createACLIPForTesting(acl_ip_name)
        testAclIPId=c.getAclId(acl_ip_name)
        logging.info("testing GET  for showIpAclByIdent ")
        response = requests.get("http://%s/vRest/acl-ips/id/%s"%(switch ,testAclIPId) , auth=(username , password))
        assert response.status_code == 200
        assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
        assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
        cliresponseHash = [ x  for x  in  c.show()  if   x['name'] == acl_ip_name ][0]
        jsonResponseDat=json.loads(response.text)["data"][0]
        pprint("=========CLI  OUTOUT =============")
        pprint(cliresponseHash)
        pprint("=========END  OF CLI  OUTOUT =============")
        pprint("=========JSON  OUTOUT =============")
        pprint(jsonResponseDat)
        pprint("=========END  OF JSON  OUTOUT =============")
        attributeListToCompare=[u'src-ip-mask',
                 u'vlan',
                 u'name',
                 u'dst-port',
                 u'src-ip',
                 u'dst-ip-mask',
                 u'port',
                 u'src-port',
                 u'dst-ip',
                 u'action',
                 u'scope',
                 u'id']

        for attrib in attributeListToCompare:
            assert cliresponseHash[attrib] == str(jsonResponseDat[attrib])




def test_FailureAuthorizationupdateIpAclByIdent(switch):
        """

        """
        logging.info("testing Failed authentication  for updateIpAclByIdent ")
        response = requests.get("http://%s/vRest/acl-ips/id/8"%switch )
        assert response.status_code == 401





testdata = [ # src_ip_mask,name,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,action,scope,dst_ip,port
               (0, testAclIP%random.randint(0,20000), 'ip', 0, 0, 0, test_src_ip%random.randint(6,200), 41 ,  "deny",  test_dst_ip%random.randint(6,200), 0)
        ]
@pytest.mark.parametrize("src_ip_mask,name,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,action,dst_ip,port", testdata)
def test_PUTupdateIpAclByIdent(switch,src_ip_mask,name,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,action,dst_ip,port):
    """

    """
    c=acl_ip(switch)
    c.createACLIPForTesting(name)
    testAclIPId=c.getAclId(name)
    pprint(testAclIPId)
    actionBefore = [ x['action']  for  x in  c.show()  if   x['name'] ==str(name)]
    logging.info("testing PUT  for updateIpAclByIdent ")
    payload =  {  'action' : action }
    pprint(payload)
    response = requests.put("http://%s/vRest/acl-ips/id/%s"%(switch ,testAclIPId) , auth=(username , password) ,  data=json.dumps(payload))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    actionAfter =  [ x['action']  for  x in  c.show() if x['name'] == str(name)][0]
    assert actionAfter == action


def test_FailureAuthorizationdeleteIpAclByIdent(switch):
        """

        """
        logging.info("testing Failed authentication  for deleteIpAclByIdent ")
        response = requests.get("http://%s/vRest/acl-ips/id/7"%switch )
        assert response.status_code == 401




def test_FailureAuthorizationdeleteIpAclByName(switch):
        """

        """
        logging.info("testing Failed authentication  for deleteIpAclByName ")
        response = requests.get("http://%s/vRest/acl-ips/name/%s"%(switch,testAclIP%random.randint(0,20000)) )
        assert response.status_code == 401





testdata = [ #
           (testAclIP%random.randint(0,20000))
        ]

@pytest.mark.parametrize("acl_name", testdata)
def test_DELETEdeleteIpAclByName(switch,acl_name):
    """

    """
    c=acl_ip(switch)
    c.createACLIPForTesting(acl_name)
    logging.info("testing DELETE  for deleteIpAclByName ")
    response = requests.delete("http://%s/vRest/acl-ips/name/%s"%(switch ,acl_name) , auth=(username , password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    id = c.getAclId(acl_name)
    assert id == None


def test_FailureAuthorizationshowIpAclByIdent(switch):
        """

        """
        logging.info("testing Failed authentication  for showIpAclByIdent ")
        response = requests.get("http://%s/vRest/acl-ips/id/7"%switch )
        assert response.status_code == 401






testdata = [ #
           (testAclIP%random.randint(0,20000))
        ]

@pytest.mark.parametrize("acl_name", testdata)
def test_DELETEdeleteIpAclByIdent(switch,acl_name):
    """
       
    """
    c=acl_ip(switch)
    c.createACLIPForTesting(acl_name)
    aclid=c.getAclId(acl_name)
    pprint(aclid)
    logging.info("testing DELETE  for deleteIpAclByIdent ") 
    response = requests.delete("http://%s/vRest/acl-ips/id/%s"%(switch ,aclid) , auth=(username , password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"])  == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    id = c.getAclId(acl_name)
    assert id == None


def test_teardown(switch):
    v = acl_ip(switch)
    v.deleteAll()
