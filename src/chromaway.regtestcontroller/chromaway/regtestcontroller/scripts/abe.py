import sys
from generated_config import config
import json
from Abe import abe


datadir = [{
       "dirname": '/home/jorgen/.bitcoin',
       "chain": "Bitcoin"
      }]


db_arg = '--connect-args=/mnt/ramdisk/foo/abe.sqlite'
commit_arg = '--commit-bytes=100000'
no_serve =  '--no-serve'
datadir_arg = '--datadir=' + json.dumps(datadir)
port_arg = '--port='+ str(config.abe_port)
config_arg = '--config='+ config.abe_config_location

argv = [datadir_arg, no_serve, port_arg, config_arg]

def main():
    abe.main(argv)

