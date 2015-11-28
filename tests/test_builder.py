# encoding: utf-8


import json

import requests

from stellar_base.build import Builder, HORIZON_TEST
from stellar_base.keypair import Keypair


class TestBuilder(object):
    def __init__(self):

        self.cold = Keypair.random()
        self.hot = Keypair.random()
        # self.hot = Keypair.from_seed('SECRET')
        # self.cold = Keypair.from_seed('SECRET')

    def test_builder(self):
        cold_account = self.cold.address().decode()
        hot_account = self.hot.address().decode()

        fund(cold_account)

        cold = Builder(self.cold.seed().decode())

        cold.append_create_account_op(hot_account, 200)
        cold.append_trust_op(cold_account, 'BEER', 1000, address=hot_account)
        # append twice for test
        cold.append_payment_op(hot_account, 50.123, 'BEER', cold_account)
        cold.append_payment_op(hot_account, 50.123, 'BEER', cold_account)
        cold.sign(self.hot.seed().decode())

        try:
            response = cold.submit()
            print(response)
        except:
            assert False

    def test_builder_xdr(self):
        cold_account = self.cold.address().decode()
        hot_account = self.hot.address().decode()
        fund(cold_account)
        fund(hot_account)

        cold = Builder(self.cold.seed().decode())
        cold.append_trust_op(cold_account, 'BEER', 1000, hot_account)
        cold.append_payment_op(hot_account, 100, 'BEER', cold_account)
        cold.append_payment_op(cold_account, 2.222, 'BEER', cold_account, hot_account)

        xdr = cold.gen_xdr()
        hot = Builder(self.hot.seed().decode())
        hot.import_from_xdr(xdr)
        # hot.sign()

        try:
            response = hot.submit()
            print(response)
        except:
            assert False


def fund(address):
    r = requests.get(HORIZON_TEST + '/friendbot?addr=' + address)  # Get 10000 lumens
    t = r.text
    if 'hash' in json.loads(t):
        return True
    elif 'op_already_exists' in json.loads(t):
        return True
    else:
        return False