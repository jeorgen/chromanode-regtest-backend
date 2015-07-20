WHAT IT DOES

This buildout builds from source and configures in a local directory

* postgresql
* bitcoind in regtest mode
* node.js and npm
* supervisord to run the above and chromanode

...for experimental use with chromanode, specifically to test regtest mode in bitcoind.

DEPENDENCIES

The following packages are needed for bitcoind to work on Ubuntu 14.04LTS:

```build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config libdb4.8++-dev```

Run:

```apt-get install build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config libdb4.8++-dev```


On Debian 7, the libdb4.8++-dev and friends (libdb4.8, libdb4.8-dev) must be downloaded from a newer Debian and be manually
installed with dpkg -i

Clone the chromanode-regtest-backend repository, install with virtualenv a python2.7 (may work wth other versions of python, python just builds the environment).

    virtualenv .

Then issue:

    ./bin/python bootstrap
    ./bin/pip install --upgrade zc.buildout
    ./bin/buildout

The last one will take a bit of time

INSTALL CHROMANODE

The chromanode server is currently cloned from 
https://github.com/jeorgen/chromanode-regtest-test

and must appear as "chromanode" inside the directory where this README file is. Currently it is not installed as a submodule so this must be done manually.

The chromanode repository https://github.com/jeorgen/chromanode-regtest-test is identical to the original right now, except user names and passwords.

SETTINGS FOR BITCOIND WITH CHROMANODE

bitcoind must be configured with the same user name and password as is used in chromanode.
bitcoind's setting are in etc/base.cfg, under the ```supervisor``` section:

    -regtest -server -rpcuser=chromaway -rpcpassword=masonit -port=8333

SETTINGS FOR POSTGRESQL WITH CHROMANODE

Initialize the postgresql database with the password ```masonit```:

    ./bin/initdb -U chromaway -W var/databases/postgres/

Create a database by the name of ```chromaway```:

    ./bin/createdb -h 127.0.0.1 -p 17520 chromaway

Make sure the postgresql urls in:

* chromanode/config/master.yml
* chromanode/config/slave.yml

agree with this.

RUNNING THE SYSTEM

Issue:

    ./bin/supervisord

then check on the system with:

    ./bin/supervisorctl

The chromanode slave (the json-rpc server) will serve on port 3001, with the default settings.

CONSTRUCTING A BLOCKCHAIN

Make sure the ~/.bitcoin/bitcoin.conf has the the same username and password as you started the server with.

    ./bin/bitcoin-cli -regtest generate 101

Or if you need more coins and blocks:

    ./bin/bitcoin-cli -regtest generate 3000


SPENDING BITCOINS

Generate an address with:

    ./bin/bitcoin-cli -regtest getnewaddress

and make a payment to it via bitcoin-cli:

    ./bin/bitcoin-cli -regtest sendtoaddress <address> 12

Then bury your transaction under some blocks:

    ./bin/bitcoin-cli -regtest generate 6

Then use the dumpprivkey command in bitcoin-cli for that address to get the private key.

    ./bin/bitcoin-cli -regtest dumpprivkey <address>



