'''
Setup the enviroment variables
.. code:bash

    $> export RACKSPACETOKEN="<rackspace_token>"
    $> export RACKSPACEUSER="<rackspace_username>"

'''

import json
import os

from collections import namedtuple
from typing import Dict

import requests


class Domain:
    ''' representation od a DOMAIN metadata '''

    def __init__(
        self, ttl=None, accountId=None,
        id=None, name=None, emailAddress=None,
        updated=None, created=None
    ) -> None:
        self.ttl = None  # 300,
        self.accountId = None  # 769012,
        self.id = None  # 6362479,
        self.name = None  # "necto.com.br",
        self.emailAddress = None  # "name@mail.com",
        self.updated = None  # "2020-01-04T01:54:21.000+0000",
        self.created = None  # "2019-01-08T07:20:22.000+0000"


class Record:
    '''representation od a record domain metadata '''

    def __init__(self, name=None, id=None, type=None, data=None, updated=None, ttl=None, created=None):
        self.name = None  # "example.com",
        self.id = None  # "A-6822994",
        self.type = None  # "A",
        self.data = None  # "192.0.2.17",
        self.updated = None  # "2011-06-24T01:12:52.000+0000",
        self.ttl = None  # 86400,
        self.created = None  # "2011-06-24T01:12:52.000+0000"


class RAXAccess:
    def __init__(self, rax_username=None, rax_token=None):
        # params takes precedence over enviroment vars

        if not rax_username:
            self.rax_username = os.getenv('RAXUserName')
        else:
            self.rax_username = rax_username

        if not rax_token:
            self.rax_token = os.getenv('RAXToken')
        else:
            self.rax_token = rax_token

        if self.rax_username is None:
            raise OSError("Username environment var is not set.")

        if self.rax_token is None:
            raise OSError("Token  environment var is not set.")

        self.user_name = None
        self.user_id = None
        self.token = None
        self.tenant = None
        self.expires = None
        self.api_base_url = 'https://dns.api.rackspacecloud.com/v1.0'

    def _json_object_hook(self, d: Dict):
        return namedtuple('X', d.keys(), rename=True)(*d.values())

    def json2obj(self, data_json):
        return json.loads(data_json, object_hook=self._json_object_hook)

    def auth(self):
        req_token_url = r'https://identity.api.rackspacecloud.com/v2.0/tokens'
        req_token_headers = {"content-type": "application/json"}
        req_token_payload = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials": {
                    "username": self.rax_username,
                    "apiKey": self.rax_token
                }
            }
        }
        resp = requests.post(
            req_token_url,
            data=json.dumps(req_token_payload),
            headers=req_token_headers)
        if resp.status_code == 200:
            obj = self.json2obj(resp.text)
            self.user_id = obj.access.user.id
            self.user_name = obj.access.user.name
            self.user_email = obj.access.user.email

            self.token = obj.access.token.id
            self.tenant = obj.access.token.tenant.id

        else:
            obj = None

        return self.user_name


class RAXDomains:

    def __init__(self, rax_access: RAXAccess):
        self.rax_access = rax_access
        self.json_domains = None  # raw response text
        self.domains = []  # domains list

    def get_domains(self, domn_ids=None):
        headers = {
            'content-type': 'application/json',
            'X-Auth-Token': self.rax_access.token,  # token
            'X-Project-Id': self.rax_access.tenant
        }
        url = f'{self.rax_access.api_base_url}/{self.rax_access.tenant}/domains'
        resp = requests.get(url, headers=headers)
        self.json_domains = resp.text
        d = json.loads(resp.text)
        domain_dicts = d['domains']
        self.domains = []

        for item in domain_dicts:
            self.domains.append(Domain(**item))

        return resp.text

    def get_records(self):
        headers = {
            'content-type': 'application/json',
            'X-Auth-Token': self.rax_access.token,  # token
            'X-Project-Id': self.rax_access.tenant
        }
        url = f'{self.rax_access.api_base_url}/{self.rax_access.tenant}/domains'
        resp = requests.get(url, headers=headers)
        self.json_domains = resp.text
        d = json.loads(resp.text)
        domain_dicts = d['recordsList']['records']
        self.domains = []

        for item in domain_dicts:
            self.domains.append(Record(**item))
        return [{'x': 1}, {'x': 1}]
