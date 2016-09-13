# coding: utf-8

import json

import requests

from stellar_base.exceptions import APIException

try:
    from sseclient import SSEClient
except ImportError:
    SSEClient = None
try:
    # Python 3
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode

HORIZON_LIVE = "https://horizon.stellar.org"
HORIZON_TEST = "https://horizon-testnet.stellar.org"


def query(url, params=None, sse=False):
    if sse is False:
        res = requests.get(url, params=params)
        if res.status_code in range(400, 501):
            error = res.json()
            raise APIException(error['title'], status_code=res.status_code, payload=error)
        return res.json()
    else:
        if SSEClient is None:
            raise ValueError('SSE not supported, missing sseclient module')
        if params:
            url = url + '?' + urlencode(params)
        messages = SSEClient(url)
        return messages


class Horizon(object):
    def __init__(self, horizon=None):
        if horizon is None:
            self.horizon = HORIZON_TEST
        else:
            self.horizon = horizon

    def submit(self, te):
        params = {'tx': te}
        url = self.horizon + '/transactions/'
        p = requests.post(url, data=params, )  # timeout=20
        return json.loads(p.text)

    def query(self, url, params=None, sse=False):
        return query(self.horizon + url, params, sse)

    def accounts(self, params=None, sse=False):
        url = self.horizon + '/accounts/'
        return query(url, params, sse)

    def account(self, address):
        url = self.horizon + '/accounts/' + address
        return query(url)

    def account_effects(self, address, params=None, sse=False):
        url = self.horizon + '/accounts/' + address + '/effects/'
        return query(url, params, sse)

    def account_offers(self, address, params=None):
        url = self.horizon + '/accounts/' + address + '/offers/'
        return query(url, params)

    def account_operations(self, address, params=None, sse=False):
        url = self.horizon + '/accounts/' + address + '/operations/'
        return query(url, params, sse)

    def account_transactions(self, address, params=None, sse=False):
        url = self.horizon + '/accounts/' + address + '/transactions/'
        return query(url, params, sse)

    def account_payments(self, address, params=None, sse=False):
        url = self.horizon + '/accounts/' + address + '/payments/'
        return query(url, params, sse)

    def transactions(self, params=None, sse=False):
        url = self.horizon + '/transactions/'
        return query(url, params, sse)

    def transaction(self, tx_hash):
        url = self.horizon + '/transactions/' + tx_hash
        return query(url)

    def transaction_operations(self, tx_hash, params=None):
        url = self.horizon + '/transactions/' + tx_hash + '/operations/'
        return query(url, params)

    def transaction_effects(self, tx_hash, params=None):
        url = self.horizon + '/transactions/' + tx_hash + '/effects/'
        return query(url, params)

    def transaction_payments(self, tx_hash, params=None):
        url = self.horizon + '/transactions/' + tx_hash + '/payments/'
        return query(url, params)

    def order_book(self, params=None):
        url = self.horizon + '/order_book/'
        return query(url, params)

    def order_book_trades(self, params=None):
        url = self.horizon + '/order_book/trades/'
        return query(url, params)

    def ledgers(self, params=None, sse=False):
        url = self.horizon + '/ledgers/'
        return query(url, params, sse)

    def ledger(self, ledger_id):
        url = self.horizon + '/ledgers/' + ledger_id
        return query(url)

    def ledger_effects(self, ledger_id, params=None):
        url = self.horizon + '/ledgers/' + ledger_id + '/effects/'
        return query(url, params)

    def ledger_offers(self, ledger_id, params=None):
        url = self.horizon + '/ledgers/' + ledger_id + '/offers/'
        return query(url, params)

    def ledger_operations(self, ledger_id, params=None):
        url = self.horizon + '/ledgers/' + ledger_id + '/operations/'
        return query(url, params)

    def ledger_payments(self, ledger_id, params=None):
        url = self.horizon + '/ledgers/' + ledger_id + '/payments/'
        return query(url, params)

    def effects(self, params=None, sse=False):
        url = self.horizon + '/effects/'
        return query(url, params, sse)

    def operations(self, params=None, sse=False):
        url = self.horizon + '/operations/'
        return query(url, params, sse)

    def operation(self, op_id, params=None):
        url = self.horizon + '/operations/' + op_id
        return query(url, params)

    def operation_effects(self, tx_hash, params=None):
        url = self.horizon + '/operations/' + tx_hash + '/effects/'
        return query(url, params)

    def payments(self, params=None, sse=False):
        url = self.horizon + '/payments/'
        return query(url, params, sse)


def horizon_testnet():
    return Horizon(HORIZON_TEST)


def horizon_livenet():
    return Horizon(HORIZON_LIVE)
