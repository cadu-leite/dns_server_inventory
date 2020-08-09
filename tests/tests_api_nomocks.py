
import json

import unittest


import requests

from rax_dns.rax_dns import RAXAccess
from rax_dns.rax_dns import RAXDomains


class TestRealAccess(unittest.TestCase):
    '''
    before run , set env vars
    export RAXUserName='racksapce user'
    export RAXToken='racksapce API access token '
    '''
    @unittest.skip('access real api  ...')
    def test_get_domains(self):
        '''
        intgration test , real access to the api.
        '''
        # print(f'TETE DE CONEXAO ')
        rax_access = RAXAccess()
        rax_access.auth()
        print(f'\n>>>>> TENANT: {rax_access.tenant}<<<<<<<<')
        rax_doms = RAXDomains(rax_access)
        rax_doms.get_domains()
        # print(rax_doms.domains)
        self.assertTrue(True, 'teste de conexão')

