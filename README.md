WHAT IT DOES

This buildout is for testing use with chromanode, specifically to run it in regtest mode with bitcoind and in doing so having unlimited access to (regtest) bitcoins. The purpose is to facilitate testing bitcoin dependent services, including transactions and confirmations, without having to rely on bitcoin or testnet faucets. The buildout contains a json-rpc server through which you can tell bitcoind to add confirmations on top of submitted transactions.

This buildout builds from source and installs everything in its own local directory:

* postgresql
* bitcoind in regtest mode
* node.js and npm
* A small json-rpc server for mining new blocks from test scripts
* A regtest verson of bitcoin-abe, a crypto currency block explorer, to see what's actually in the regtest blockchain
* supervisord to run the above servers and to run the chromanode servers

DEPENDENCIES

The following packages are needed for bitcoind and postgresql to compile on Ubuntu 14.04LTS:

```build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config postgresql-server-dev-all python-virtualenv` libdb4.8++-dev```

The libdb4.8++-dev is not part of the standard Ubuntu repositories. You can add the following repository under ```/etc/apt/sources.list.d/``` to get it:

    deb http://ppa.launchpad.net/bitcoin/bitcoin/ubuntu trusty main
    # deb-src http://ppa.launchpad.net/bitcoin/bitcoin/ubuntu trusty main

Run:

```apt-get install build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config postgresql-server-dev-all python-virtualenv` libdb4.8++-dev```

On Debian 7, the libdb4.8++-dev and friends (libdb4.8, libdb4.8-dev) must be downloaded from a newer Debian and be manually
installed with dpkg -i, or there may be a third party repository as well.

INSTALLATION

Clone the chromanode-regtest-backend repository (this repository).  Go into the cloned repository. Type:

    virtualenv .

Then issue:

    ./bin/python bootstrap
    ./bin/buildout

The last one will take a bit of time (typically 5-20 minutes), since it will download and build postgresql, node.js, npm and bitcoind from source and install an assortment of python packages.

INSTALL CHROMANODE

The chromanode server is currently cloned from the develop branch of
https://github.com/chromaway/chromanode/

and will appear as "chromanode" inside the directory where this README file is. It gets installed as a git submodule. So you need to do:

    git submodule init
    git submodule update

Install the dependencies for chromanode with:

    cd chromanode
    ../bin/npm install .


SETTINGS FOR POSTGRESQL WITH CHROMANODE

Initialize the postgresql database cluster with the password ```masonit```:

    ./bin/initdb -U chromaway -W var/databases/postgres/

Start the server:

    ./bin/postgres -N 500 -i -p 17520 -D var/databases/postgres

In another terminal window, create a database by the name of ```chromaway```:

    ./bin/createdb -O chromaway -U chromaway -W -h 127.0.0.1 -p 17520 chromaway

You can now terminate the postgresql server with Ctrl-c.

INSTALL BITCOIN-ABE

The bitcoin-abe block explorer is currently cloned from the regtest branch of

git@github.com:jeorgen/bitcoin-abe.git

It gets installed as a git submodule. So unless you haven't done it already for chromanode, you need to do:

    git submodule init
    git submodule update


RUNNING THE SYSTEM

Issue:

    ./bin/supervisord

then check on the system with:

    ./bin/supervisorctl

Note that the chromanode servers are not automatically started. Inside of supervisorctl issue:

    start chromanode-master chromanode-slave

Here is a sample output from ./bin/supervisorctl:

    abe                              RUNNING   pid 17179, uptime 0:00:04
    bitcoind-controller              RUNNING   pid 17178, uptime 0:00:04
    bitcoind-server                  RUNNING   pid 17176, uptime 0:00:04
    chromanode-master                STOPPED   Not started
    chromanode-slave                 STOPPED   Not started
    postgresql-server                RUNNING   pid 17177, uptime 0:00:04
    supervisor> start chromanode-master chromanode-slave


The chromanode slave will serve http on port 3001, with the default settings in its YAML config file. The bitcoind-controller will serve json-rpc over http on port 17580.

TROUBLESHOOTING

If a service doesn't start or fails, you can run it from the command line to see what the problem is. Supervisord runs each service from a virtual terminal. To check what command it uses for each service, do:

    less parts/supervisor/supervisord.conf 

...and take the appropriate command from there and run it from a terminal to see what the problem is. var/log/ also has logs for each service.

CHANGING PORTS AND STUFF

Port and authentication settings can be changed in etc/base.cfg in the config section. For any port and auth changes to take effect:

* Stop supervisord (./bin/supervisorctl shutdown)
* Rerun buildout (./bin/buildout)
* restart supervisor (./bin/supervisord)

Things that can be changed
From the config section:

* database_host - host for the postgresql server. Most likely 127.0.0.1 or equivalent, since it is a part of the buildout
* database_port - port for the postgresql server.
* bitcoind_port - peer port for the bitcoind server
* rpc_user - JSON-RPC user name for accessing bitcoind
* rpc_password- JSON-RPC password for accessing bitcoind
* rpc_port- JSON-RPC port for accessing bitcoind
* controller_port - JSON-RPC http port for mining blocks, from your test scripts. This port should be proxied externally
* bitcoin_regtest_data_dir - where the regtest blocks are stored. A value of ```default``` means in the standard place in ~/.bitcoin/regtest
* abe_config_location - location of config file for bitcoin-abe
* abe_port - port tha the bitcoin-abe explorer can be accessed at. This port should be proxied externally

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

USING THE BITCOIN-ABE REGTEST BLOCKCHAIN EXPLORER

Currently the bitcoin-abe regtest blockchain explorer is not "url-safe" in the sense that it can be folded into the url name space (It could also be that I have made a mistake in the proxy conf). It wants to be at the root. So use a different domain for it, or a different port.