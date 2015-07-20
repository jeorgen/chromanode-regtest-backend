WHAT IT DOES
This buildout builds from source and configures in a local directory

x postgresql
x bitcoind in regtest mode
x node.js and npm
x supervisord to run the above and chromanode

...for experimental use with chromanode, specifically to test regtest mode in bitcoind.

DEPENDENCIES
The following packages are needed for bitcoind to work on Ubuntu 14.04LTS:

```build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config libdb4.8++-dev```

Run:

```apt-get install build-essential libtool autotools-dev autoconf libssl-dev libboost-all-dev pkg-config libdb4.8++-dev```


On Debian 7, the libdb4.8++-dev and friends (libdb4.8, libdb4.8-dev) must be downloaded from a newer Debian and be manually
installed with dpkg -i

Clone this repository, install with virtualenv a python2.7.

Then issue:

    ./bin/python bootstrap
    ./bin/pip install --upgrade zc.buildout
    ./bin/buildout

The last one will take a bit of time

INSTALL CHROMANODE

The chromanode server is currently cloned from 
https://github.com/jeorgen/chromanode-regtest-test

and must appear as "chromanode" inside the directory where this README file is. Currently it is not installed as a submodule so ths must be doen manually.

https://github.com/jeorgen/chromanode-regtest-test is identical to the original right now, except user names and passwords.

SETTINGS FOR BITCOIND WITH CHROMANODE
bitcoind must be configured with the same user name and password as is used in chromanode
bitcoind's setting are in etc/base.cfg, under the "supervisor# section.



SETTINGS FOR POSTGRESQL WITH CHROMANODE
Initialize the postgresql database iwth password ```masonit```:
./bin/initdb -U chromaway -W var/databases/postgres/

Create a database by the name of ```chromaway```
./bin/createdb -h 127.0.0.1 -p 17520 chromaway

Make sure the postgresql urls in:

* chromanode/config/master.yml
* chromanode/config/slave.yml

agree with this.


