import random
import sys

import pytest

from  admin_syslog_match import admin_syslog_match
from  admin_syslog import admin_syslog

sys.path.append(".")
import requests
import json
from pprint import pprint
import logging


def logAssert(test, msg):
    if not test:
        logging.error(msg)
        assert test, msg



username = "network-admin"
password = "test123"

testSysLog = "testSysLog-%d"
testName = "testName-%d"
testHost = "172.16.32.%d"
testPort = 89
testFormat = "structured"


def test_FailureAuthorizationcreateAdminSyslog(switch):
    """
           
        """
    logging.info("testing Failed authentication  for createAdminSyslog ")
    response = requests.get("http://%s/vRest/admin-syslogs" % switch)
    assert response.status_code == 401


testdata = [  # message_format,scope,host,name,port
    ('structured', 'fabric', testHost % random.randint(2, 200), testName % random.randint(2, 200),
     random.randint(2, 200))
]


@pytest.mark.parametrize("message_format,scope,host,name,port", testdata)
def test_POSTcreateAdminSyslog(message_format, scope, host, name, port, switch):
    """
       
    """
    c = admin_syslog(switch)
    logging.info("testing POST  for createAdminSyslog ")
    response = requests.post("http://%s/vRest/admin-syslogs" % (switch), auth=(username, password), data=json.dumps(
            {'message-format': message_format, 'scope': scope, 'host': host, 'name': name, 'port': port}))
    print response.json()
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashAfter)


def test_FailureAuthorizationshowAdminSyslogs(switch):
    """
           
        """
    logging.info("testing Failed authentication  for showAdminSyslogs ")
    response = requests.get("http://%s/vRest/admin-syslogs" % switch)
    assert response.status_code == 401


def test_GETshowAdminSyslogs(switch):
    """
           
        """
    c = admin_syslog(switch)
    syslog_server = testSysLog % random.randint(0, 20000)
    c.createSyslogServerForTesting(syslog_server)
    logging.info("testing GET  for showAdminSyslogs ")
    response = requests.get("http://%s/vRest/admin-syslogs" % (switch), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)


def test_FailureAuthorizationshowAdminSyslogByName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for showAdminSyslogByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testSysLog % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_GETshowAdminSyslogByName(switch,name):
    """
           
        """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(name)
    logging.info("testing GET  for showAdminSyslogByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/%s" % (switch, name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)


def test_FailureAuthorizationupdateAdminSyslogByName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for updateAdminSyslogByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/name" % switch)
    assert response.status_code == 401


testdata = [  # scope,host,port,message_format
    (testSysLog % random.randint(0, 20000), 'fabric', testHost % random.randint(2, 200), 78, 'legacy')
]


@pytest.mark.parametrize("name,scope,host,port,message_format", testdata)
def test_PUTupdateAdminSyslogByName(name, scope, host, port, message_format, switch):
    """
       
    """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(name)
    logging.info("testing PUT  for updateAdminSyslogByName ")
    response = requests.put("http://%s/vRest/admin-syslogs/%s" % (switch, name), auth=(username, password),
                            data=json.dumps(
                                    {'scope': scope, 'host': host, 'port': port, 'message-format': message_format}))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashAfter)


def test_FailureAuthorizationdeleteAdminSyslogByName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for deleteAdminSyslogByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/{name}" % switch)
    assert response.status_code == 401


testdata = [  #
    (testSysLog % random.randint(0, 20000))
]


@pytest.mark.parametrize("name", testdata)
def test_DELETEdeleteAdminSyslogByName(switch,name):
    """
       
    """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(name)
    logging.info("testing DELETE  for deleteAdminSyslogByName ")
    response = requests.delete("http://%s/vRest/admin-syslogs/%s" % (switch, name), auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashAfter)


def test_FailureAuthorizationaddAdminSyslogMatchByAdminSyslogName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for addAdminSyslogMatchByAdminSyslogName ")
    response = requests.get("http://%s/vRest/admin-syslogs/syslog-name/matches" % switch)
    assert response.status_code == 401


testdata = [  # message_format,scope,host,name,port
    (testSysLog % random.randint(2, 20000), testName % random.randint(2, 20000), 'event')
]


@pytest.mark.parametrize("syslog_name,name,message_category", testdata)
def test_POSTaddAdminSyslogMatchByAdminSyslogName(switch,syslog_name, name,message_category):
    """
       
    """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(syslog_name)
    logging.info("testing POST  for addAdminSyslogMatchByAdminSyslogName ")
    response = requests.post("http://%s/vRest/admin-syslogs/%s/matches" % (switch, syslog_name),
                             auth=(username, password), data=json.dumps(
                {
                  "name": name,
                  "msg-category": message_category,

}))
    pprint(response.json())
    assert str(response.status_code) == "201"
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashAfter)


def test_FailureAuthorizationshowAdminSyslogMatchesByAdminSyslogName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for showAdminSyslogMatchesByAdminSyslogName ")
    response = requests.get("http://%s/vRest/admin-syslogs/syslog-name/matches" % switch)
    assert response.status_code == 401


testdata = [  #
    (testSysLog % random.randint(0, 20000))
]


@pytest.mark.parametrize("syslog_name", testdata)
def test_GETshowAdminSyslogMatchesByAdminSyslogName(switch,syslog_name):
    """
           
        """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(syslog_name)
    m=admin_syslog_match(switch)
    m.createSysLogMatchForTestingMessageCategoryAudit(syslog_name,"name")
    logging.info("testing GET  for showAdminSyslogMatchesByAdminSyslogName ")
    response = requests.get("http://%s/vRest/admin-syslogs/%s/matches" % (switch, syslog_name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)


def test_FailureAuthorizationshowAdminSyslogMatchByNameByName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for showAdminSyslogMatchByNameByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/syslog-name/matches/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testSysLog % random.randint(0, 20000), testName % random.randint(0, 20000))
]


@pytest.mark.parametrize("syslog_name,name", testdata)
def test_GETshowAdminSyslogMatchByNameByName(switch,syslog_name, name):
    """
           
        """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(syslog_name)
    m= admin_syslog_match(switch)
    m.createSysLogMatchForTestingMessageCategoryAudit(syslog_name,name)
    logging.info("testing GET  for showAdminSyslogMatchByNameByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/%s/matches/%s" % (switch, syslog_name, name),
                            auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["data"]) != ""
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseHash = c.show()
    jsonResponseDat = json.loads(response.text)["data"]
    pprint(jsonResponseDat)
    pprint(cliresponseHash)


def test_FailureAuthorizationupdateAdminSyslogMatchByNameByName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for updateAdminSyslogMatchByNameByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/syslog-name/matches/name" % switch)
    assert response.status_code == 401


testdata = [  # scope,host,port,message_format
    (testSysLog % random.randint(2, 200000), testName % random.randint(2, 200), 'event')
]


@pytest.mark.parametrize("syslog_name,name,message_cateory", testdata)
def test_PUTupdateAdminSyslogMatchByNameByName(switch,syslog_name, name,message_cateory):
    """
       
    """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(syslog_name)
    conobj= admin_syslog_match(switch)
    conobj.createSysLogMatchForTestingMessageCategoryAudit(syslog_name,name)
    c.createSyslogServerForTesting(syslog_name)

    logging.info("testing PUT  for updateAdminSyslogMatchByNameByName ")
    response = requests.put("http://%s/vRest/admin-syslogs/%s/matches/%s" % (switch, syslog_name, name),
                            auth=(username, password), data=json.dumps(
                {'msg-name': name, 'msg-category': message_cateory}))
    pprint(response.json())
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = c.show()
    pprint(cliresponseListOfHashAfter)


def test_FailureAuthorizationremoveAdminSyslogMatchByNameByName(switch):
    """
           
        """
    logging.info("testing Failed authentication  for removeAdminSyslogMatchByNameByName ")
    response = requests.get("http://%s/vRest/admin-syslogs/syslog-name/matches/name" % switch)
    assert response.status_code == 401


testdata = [  #
    (testSysLog % random.randint(0, 20000), testName % random.randint(0, 20000))
]


@pytest.mark.parametrize("syslog_name,name", testdata)
def test_DELETEremoveAdminSyslogMatchByNameByName(switch,syslog_name, name):
    """
       
    """
    c = admin_syslog(switch)
    c.createSyslogServerForTesting(syslog_name)
    conobj= admin_syslog_match(switch)
    conobj.createSysLogMatchForTestingMessageCategoryAudit(syslog_name,name)
    c.createSyslogServerForTesting(syslog_name)
    logging.info("testing DELETE  for removeAdminSyslogMatchByNameByName ")
    response = requests.delete("http://%s/vRest/admin-syslogs/%s/matches/%s" % (switch, syslog_name, name),
                               auth=(username, password))
    assert response.status_code == 200
    assert str(json.loads(response.text)["result"]["result"][0]["code"]) == "0"
    assert str(json.loads(response.text)["result"]["result"][0]["status"]) == "Success"
    cliresponseListOfHashAfter = [ x   for  x  in  conobj.show() if x['name'] == name and  x['syslog-name'] == syslog_name ]
    assert(len(cliresponseListOfHashAfter)) ==0

