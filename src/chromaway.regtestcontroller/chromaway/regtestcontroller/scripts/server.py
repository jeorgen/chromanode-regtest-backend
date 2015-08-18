from bottle import run
from chromaway.regtestcontroller import bottle_json_rpc
from generated_config import config
from bitcoinrpc.authproxy import AuthServiceProxy

jsonrpc = bottle_json_rpc.register('/')


@jsonrpc
def add_confirmations(confirmations):
    if not confirmations in (1, 2, 3, 4, 5, 6):
        return {'error': 'confirmation value supplied not in interval from 1 through 6'}
    bitcoind=AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (config.rpc_user, config.rpc_password), timeout=600)
    blocks=bitcoind.generate(confirmations)
    return {'result': blocks}

def main():
    run(host='localhost', port=config.controller_port, debug=True)

if __name__ == '__main__':
    main()