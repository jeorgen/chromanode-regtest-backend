WHAT IT DOES

This buildout is for testing use with chromanode, specifically to run it in regtest mode with bitcoind and in doing so having unlimited access to (regtest) bitcoins. The purpose is to facilitate testing bitcoin dependent services, including transactions and confirmations, without having to rely on bitcoin or testnet faucets. The buildout contains a json-rpc server through which you can tell bitcoind to add confirmations on top of submitted transactions.

This buildout builds from source and installs everything in its own local directory:

* postgresql
* bitcoind in regtest mode
* node.js and npm
* A small json-rpc server for mining new blocks
* supervisord to run the above and to run chromanode

DEPENDENCIES

The following packages are needed for bitcoind to compile on Ubuntu 14.04LTS:

```build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config libdb4.8++-dev```

Run:

```apt-get install build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config libdb4.8++-dev```

Make sure you have virtualenv installed for python2.7. In Ubuntu 14.04 that would be:

```apt-get install python-virtualenv```

On Debian 7, the libdb4.8++-dev and friends (libdb4.8, libdb4.8-dev) must be downloaded from a newer Debian and be manually
installed with dpkg -i

INSTALLATION

Clone the chromanode-regtest-backend repository (this repository).  Go into the cloned repository. Type:

    virtualenv .

Then issue:

    ./bin/python bootstrap
    ./bin/buildout

The last one will take a bit of time (typically 5-20 minutes), since it will download and build postgresql, bitcoind from source and install an assortment of python packages.

INSTALL CHROMANODE

The chromanode server is currently cloned from 
https://github.com/jeorgen/chromanode-regtest-test

and must appear as "chromanode" inside the directory where this README file is. Currently it does not get installed as a git submodule so this must be done manually.

The chromanode repository https://github.com/jeorgen/chromanode-regtest-test is identical to the original right now, except user names and passwords.

SETTINGS FOR POSTGRESQL WITH CHROMANODE

Initialize the postgresql database cluster with the password ```masonit```:

    ./bin/initdb -U chromaway -W var/databases/postgres/

Start the server:

    bin/postgres -N 500 -i -p 17520 -D

In another terminal window, create a database by the name of ```chromaway```:

    ./bin/createdb -O chromaway -U chromaway -W -h 127.0.0.1 -p 17520 chromaway

You can now terminate the postgresql server with Ctrl-c.

RUNNING THE SYSTEM

Issue:

    ./bin/supervisord

then check on the system with:

    ./bin/supervisorctl

Here is a sample output from ./bin/supervisorctl:

    bitcoind-controller              RUNNING   pid 29703, uptime 0:00:21
    bitcoind-server                  RUNNING   pid 29699, uptime 0:00:21
    chromanode-master                RUNNING   pid 29767, uptime 0:00:19
    chromanode-slave                 RUNNING   pid 29702, uptime 0:00:21
    postgresql-server                RUNNING   pid 29700, uptime 0:00:21

The chromanode slave will serve http on port 3001, with the default settings in its YAML config file. The bitcoind-controller will serve json-rpc over http on port 17580. 

CHANGING PORTS AND STUFF

All port and authentication settings can be changed in etc/base.cfg in the config section. For any port and auth changes to take effect:

* Stop supervisord (./bin/supervisorctl shutdown)
* Rerun buildout (./bin/buildout) 
* restart supervisor (./bin/supervisord) 

CONSTRUCTING A BLOCKCHAIN

    ./bin/bitcoin-cli -regtest  -rpcuser=chromaway -rpcpassword=masonit -regtest generate 101

101 is the minimum for you to get any coins to spend in regtest mode.

Or if you need more coins and blocks:

    ./bin/bitcoin-cli -regtest  -rpcuser=chromaway -rpcpassword=masonit -regtest generate 3000

Mining 3000 blocks will take minutes to hours, depending on your hardware.

SPENDING BITCOINS

Generate an address with:

    ./bin/bitcoin-cli -rpcuser=chromaway -rpcpassword=masonit -regtest getnewaddress

and make a payment to it:

    ./bin/bitcoin-cli -rpcuser=chromaway -rpcpassword=masonit -regtest sendtoaddress <address> 12

Then bury your transaction under some blocks:

    ./bin/bitcoin-cli -rpcuser=chromaway -rpcpassword=masonit -regtest generate 6

Then use the dumpprivkey command in bitcoin-cli for that address to get the private key.

    ./bin/bitcoin-cli -regtest dumpprivkey <address>

GENERATING BLOCKS THROUGH THE BITCOIND-CONTROLLER SERVER

How do you mine blocks when you are not at the command line? The bitcoind-controller json-rpc server accepts instructions to mine from one up to six blocks, so that you can bury your transactions and make them appear confirmed. Beware that it takes a bit of time to mine a block, tens of seconds (depending on your hardware). Here an example using pyjsonrpc for instructing bitcoind to mine one block:

    import pyjsonrpc
    client = pyjsonrpc.HttpClient(url = "http://localhost:17580")
    client.add_confirmations(1)

Will give a result similar to:

    {u'result': [u'00000001c2cf5c571d09117b832ec1b6a36c72c768504ffc28fce0b443ef6a3a']}

With the use of a fronting Apache, Nginx or similar as a proxy, you can fold the bitcoind-controller server into some unused part of the url namespace of the chromanode web server. For example under:

    /regtest




