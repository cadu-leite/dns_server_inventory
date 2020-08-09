import json

import os

import unittest

import tracemalloc

import sys

from rax_dns.do_droplets import Droplets


class TestRAXAccess(unittest.TestCase):
    def teste_get_token_from_environment(self):
        DO_TOKEN = 'environment_token'
        os.environ['DO_ACCESS_TKN'] = DO_TOKEN
        do = Droplets()
        self.assertEqual(do.token, DO_TOKEN)

    def teste_get_token_from_param_precedes_env(self):
        DO_TOKEN = 'environment_token'
        os.environ['DO_ACCESS_TKN'] = DO_TOKEN + '_environment'
        do = Droplets(token=DO_TOKEN)
        self.assertEqual(do.token, DO_TOKEN)

    def test_list_droplets(self):
        exception_ocurr = False
        do = Droplets()
        try:
            do.get_droplets()
        except:
            sys.stdout.write(f'PROGRAM MSG - Unexpected error: {sys.exc_info()[0]}')
            exception_ocurr = True
        self.assertFalse(exception_ocurr)


tracemalloc.start()

# ... run your application ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

sys.stdout.write(f"\n ==== TRACE MALLOC - [ Top 10 ] =========")
for stat in top_stats[:10]:
    sys.stdout.write(f"{stat}\n")
sys.stdout.write(f"\n ----------------------------------------\n")
