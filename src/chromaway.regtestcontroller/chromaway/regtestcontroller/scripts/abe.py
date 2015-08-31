import sys
from generated_config import config
import json
from Abe import abe


datadir = [{
       "dirname": config.bitcoin_regtest_data_dir,
       "chain": "Regtest"
      }]



datadir_arg = '--datadir=' + json.dumps(datadir)
port_arg = '--port='+ str(config.abe_port)
config_arg = '--config='+ config.abe_config_location

argv = [datadir_arg, port_arg, config_arg]

def main():
    abe.main(argv)