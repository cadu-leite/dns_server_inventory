'''
Setup the enviroment variables
.. code:bash

    $> export RACKSPACETOKEN="<rackspace_token>"
    $> export RACKSPACEUSER="<rackspace_username>"

'''

from collections import namedtuple
import json
import os
from typing import Dict

import requests

# Source: https://en.wikipedia.org/wiki/List_of_DNS_record_types
DNS_REC_TYPE = [
    ('A', '32/IPV4 128/Ipv6 IP '),
    ('CNAME', 'Alias to another name '),
    ('MX', 'Map domain to tranfers list '),
    ('NS', 'Delegates a DNS zone to use the given authoritative name servers'),
    ('SRV', 'Generalized (ex.: mx) service location record unkown protocols'),
    ('TXT', 'Originally for arbitrary human-readable text in a DNS record, machine data ...'),
]


class RackSpaceAccess(object):

    def __init__(self, rackspaceusername=None, rackspaceapitoken=None):

        # params takes precedence over enviroment vars
        if not rackspaceusername:
            self.racksp_username = os.getenv('RACKSPACEUSER')
        else:
            self.racksp_username = rackspaceusername

        if not rackspaceusername:
            self.racksp_api_token = os.getenv('RACKSPACETOKEN')
        else:
            self.racksp_api_token = rackspaceapitoken

        if self.racksp_username is None:
            raise OSError("Username environment is not set.")

        if self.racksp_api_token is None:
            raise OSError("Username environment is not set.")

    def _json_object_hook(self, d: Dict):
        return namedtuple('X', d.keys(), rename=True)(*d.values())

    def json2obj(self, data_json):
        return json.loads(data_json, object_hook=self._json_object_hook)

    def _login_(self):
        '''
        returns an object representing the json response for RAX api identify

        Returns:
            obj:
                Main attributes
                # obj.ok boolean
                # obj.reason str
                # obj.status_code 200
                # obj.access.token.id
                # obj.access.token.expires
                # obj.access.token.tenant.id
                # obj.access.token.tenant.name
                # obj.access.user.email
                # obj.access.user.id
                # obj.access.user.name
        '''
        req_token_url = r'https://identity.api.rackspacecloud.com/v2.0/tokens'
        req_token_headers = {"content-type": "application/json"}
        req_token_payload = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials": {
                    "username": self.racksp_username,
                    "apiKey": self.racksp_api_token
                }
            }
        }
        data = requests.post(req_token_url, data=json.dumps(req_token_payload), headers=req_token_headers)
        obj = self.json2obj(data.text)
        return (obj)


class RAXDomains():

    def __init__(self, identity_object):
        self.token_id = identity_object.access.token.id
        self.tenant_id = identity_object.access.token.tenant.id
        self.domn_id = None
        self.rax_api_baseurl = 'https://dns.api.rackspacecloud.com/v1.0'
        self.rax_url_dmn = f'{self.rax_api_baseurl}/{self.tenant_id}/domains/'
        self.rax_url_rcs = f'{self.rax_url_dmn}{self.domn_id}'  # records

    def get_domains(self, domn_ids=None):
        headers = {
            'content-type': 'application/json',
            'X-Auth-Token': self.token_id,  # token
            'X-Project-Id': self.tenant_id
        }
        url = f'https://{self.rax_api_baseurl}/{self.tenant_id}/domains'

        data = requests.get(url)

        return data

# HTTPSConnectionPool(host='https', port=443): Max retries exceeded with url: //dns.api.rackspacecloud.com/v1.0/769012/domains (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x10d0720a0>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known'))
