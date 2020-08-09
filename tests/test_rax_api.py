
import json

import unittest
from unittest.mock import patch
from unittest.mock import Mock

import requests

from rax_dns.rax_dns import RAXAccess
from rax_dns.rax_dns import RAXDomains

# json response expected for a googd identity request on raxapi
JSON_IDENTITY_RESPONSE_OK = r'''
{
    "access": {
        "serviceCatalog": [
            {
                "endpoints": [
                    {
                        "tenantId": "MossoCloudF",
                        "publicURL": "https://cdn6.clouddrive.com/v1/MossoCloudFS",
                        "region": "REG"
                    }
                ],
                "name": "cloudFilesCDN",
                "type": "rax:object-cdn"
            }
        ],
        "user": {
            "RAX-AUTH:sessionInactivityTimeout": "PT12H",
            "RAX-AUTH:defaultRegion": "REG",
            "roles": [
                {
                    "name": "checkmate",
                    "description": "Checkmate Access role",
                    "id": "10000150"
                }
            ],
            "RAX-AUTH:phonePin": "7777777",
            "name": "usernameapi",
            "id": "999999",
            "RAX-AUTH:domainId": "88888890",
            "email": "nameuser@mail.com",
            "RAX-AUTH:phonePinState": "ACTIVE"
        },
        "token": {
            "expires": "2020-01-04T11:01:01.001Z",
            "RAX-AUTH:issued": "2020-01-03T18:46:51.436Z",
            "RAX-AUTH:authenticatedBy": [
                "APIKEY"
            ],
            "id": "lettersSoup123123123_lettersSoup123123123_",
            "tenant": {
                "name": "88888890",
                "id": "88888890"
            }
        }
    }
}
'''


class TestRAXAccess(unittest.TestCase):

    def setUp(self):
        self.patch_request_get = patch('requests.get')
        self.MockedRequest_get = self.patch_request_get.start()

        self.patch_request_post = patch('requests.post')
        self.MockedRequest_post = self.patch_request_post.start()

    def tearDown(self):
        # sem o STOP os tests reais de acesso a API FAIL !
        self.patch_request_get.stop()
        self.patch_request_post.stop()

    def test_obj_access_created(self):
        rax = RAXAccess('raxaccesstoken', 'token')
        self.assertTrue(True)

    def test_params(self):
        rax = RAXAccess('raxaccesstoken', 'token')
        rax.auth()
        requests.post.assert_called()
        requests.post.stop()

    def test_login(self):
        self.MockedRequest_post.return_value = Mock(status_code=200, text=JSON_IDENTITY_RESPONSE_OK)

        rax = RAXAccess('username', 'token')
        auth_username = rax.auth()

        self.assertEqual(auth_username, 'usernameapi')

    def test_login_unauthorized(self):
        response_unauthorized = '{"unauthorized": \
            {"code": 401, \
                "message": "Error code": "AUTH-008; \
                Username or api key is invalid."}}'

        self.MockedRequest_get.return_value = Mock(
            status_code=401, text=response_unauthorized)
        rax = RAXAccess('username', 'token')
        auth_username = rax.auth()

        self.assertEqual(auth_username, None)


class TestDomains(unittest.TestCase):

    def setUp(self):
        self.patch_request_get = patch('requests.get')
        self.MockedRequest_get = self.patch_request_get.start()

    def tearDown(self):
        self.patch_request_get.stop()

    def test_simple_raxdomains(self):
        raxaccess = RAXAccess('raxaccesstoken', 'token')
        raxdom = RAXDomains(raxaccess)

        self.MockedRequest_get.return_value = Mock(
            status_code=200,
            text='{"totalEntries":2,\
            "domains":[{"ttl":300,\
            "accountId":999999,\
            "id":8888888,\
            "name":"noorg.com",\
            "emailAddress":"name@mail.com",\
            "updated":"2020-07-22T19:47:55.000+0000",\
            "created":"2001-01-10T19:07:06.000+0000"},\
            {"ttl":300,\
            "accountId":999999,\
            "id":9999999,\
            "name":"noorg.org",\
            "emailAddress":"name@mail.com",\
            "updated":"2012-08-10T19:07:09.000+0000",\
            "created":"2002-01-10T10:07:09.000+0000"}]}')

        raxdom.get_domains()
        self.assertEqual(len(raxdom.domains), 2)

    def test_json_load(self):
        j = '{"totalEntries":2,\
        "domains":[{"ttl":300,"accountId":999999,"id":8888888,\
        "name":"noorg.com","emailAddress":"name@mail.com",\
        "updated":"2020-07-22T19:47:55.000+0000",\
        "created":"2001-01-10T19:07:06.000+0000"},\
        {"ttl":300,"accountId":999999,"id":9999999,\
        "name":"noorg.org","emailAddress":"name@mail.com",\
        "updated":"2012-08-10T19:07:09.000+0000",\
        "created":"2002-01-10T10:07:09.000+0000"}]}'
        jt = json.loads(j)['domains']
        self.assertEqual(len(jt), 2)

    def test_get_records_dumps_json(self):
        self.MockedRequest_get.return_value = Mock(
            status_code=200,
            text='{\
            "recordsList": {\
                "totalEntries": 2,\
                "records": [\
                    {\
                        "id": "A-999999999",\
                        "name": "dom.com",\
                        "type": "A",\
                        "data": "99.999.999.999",\
                        "ttl": 300,\
                        "updated": "2000-01-01T01:01:29.000+0000",\
                        "created": "2000-01-01T01:01:19.000+0000"\
                    },\
                    {\
                        "id": "A-999999998",\
                        "name": "xxx.dom.com",\
                        "type": "A",\
                        "data": "999.999.99.999",\
                        "ttl": 300,\
                        "updated": "2000-01-01T01:01:19.000+0000",\
                        "created": "2000-01-01T01:01:19.000+0000"\
                    }\
                ]\
            },\
            "ttl": 300,\
            "nameservers": [\
                {\
                    "name": "dns1.dnsdomainagent.com"\
                },\
                {\
                    "name": "dns2.dnsdomainagent.com"\
                }\
            ],\
            "accountId": 111111,\
            "id": 222222,\
            "name": "necto.com.br",\
            "emailAddress": "useremail@dom.com.",\
            "updated": "2001-01-01T01:01:21.000+0000",\
            "created": "2001-01-01T01:01:22.000+0000"\
        }')
        raxaccess = RAXAccess('raxaccesstoken', 'token')
        raxdom = RAXDomains(raxaccess)
        self.assertEqual(len(raxdom.get_records()), 2)


