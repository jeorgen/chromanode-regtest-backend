from bottle import run
from chromaway.regtestcontroller import bottle_json_rpc
from generated_config import config
from bitcoinrpc.authproxy import AuthServiceProxy


class FundingFailed(Exception):

    def __init__(self, message):
        msg = "Funding failed: " % message
        super(AddressNotFound, self).__init__(msg)

jsonrpc = bottle_json_rpc.register('/')


@jsonrpc
def add_confirmations(confirmations):
    if not confirmations in (1, 2, 3, 4, 5, 6):
        return {'error': 'confirmation value supplied not in interval from 1 through 6'}
    bitcoind = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (config.rpc_user, config.rpc_password), timeout=600)
    blocks = bitcoind.generate(confirmations)
    return {'result': blocks}


@jsonrpc
def getblockcount():
    bitcoind = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (config.rpc_user, config.rpc_password), timeout=600)
    count = bitcoind.getblockcount()
    return {'result': count}


@jsonrpc
def sendtoaddress(address, amount):
    bitcoind = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (config.rpc_user, config.rpc_password), timeout=600)
    result = bitcoind.sendtoaddress(address, amount)
    return {'result': result}


def find_funded_address(bitcoind, amount):
    groupings = bitcoind.listaddressgroupings()
    for grouping in groupings:
        for address_info in group:
            if address_info[1] >= amount:
                return {'address': address_info[0], 'amount': address_info[1]}
    return None


@jsonrpc
def getfundedaddress(amount, exact_amount=False):
    """ Given amount, returns a funded address with that amount on it or more. If exact_amount is True
        or if there is not enough coins, a new address is funded"""
    bitcoind = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (config.rpc_user, config.rpc_password), timeout=600)
    # check if we have any addresses that are funded
    if not exact_amount:
        funded_address = find_funded_address(bitcoind, amount)
        if funded_address:
            private_key = bitcoind.dumpprivkey(address)
            funded_address['private_key': private_key]
            return funded_address
    new_address = bitcoind.getnewaddress()
    result = bitcoind.sendtoaddress(new_address, amount)
    if result.haskey('error'):
        if result['error']['code'] == -6:
            add_confirmations(1)
            result = bitcoind.sendtoaddress(new_address, amount)
            if result.haskey('error'):
                if result['error']['code'] == -6:
                    raise FundingFailed("Cannot satisfy funding up to amount %s with one block of mining" % amount)
                else:
                    raise FundingFailed(result['error'])
        else:
            raise FundingFailed(result['error'])  # some error
    balance = bitcoind.getbalance(new_address)
    private_key = bitcoind.dumpprivkey(new_address)

    return {'result': result}


def main():
    run(host='localhost', port=config.controller_port, debug=True)

if __name__ == '__main__':
    main()
