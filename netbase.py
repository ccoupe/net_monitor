import os
import os.path
# Listen on mqtt topic that the 'monitor' script publishes to:
#   'bt_monitor/lost_pi' 
# Slight sanitizing and feed updates to influxdb.

import json
import sys
import time, threading, sched
import paho.mqtt.client as mqtt
import urllib.request
import rpyc
from lib.Settings import Settings
from lib.Homie_MQTT import Homie_MQTT
import logging
import logging.handlers
import argparse
from datetime import datetime

#import asyncio
#import websockets    
#import websocket  # websocket-client
#import base64

# globals
settings = None
hmqtt = None


# TODO new thread per mqtt message ? 
def msgInCb(payload):
  global settings, log, dbclient, devices
  args = json.loads(payload)
  # cancel timer when 
  
def ping_this(ip):
  print(ip)

def main():
  global log,  hmqtt, settings, dbclient
  # process cmdline arguments
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--conf", required=True, type=str,
    help="path and name of the json configuration file")
  ap.add_argument("-s", "--syslog", action = 'store_true',
    default=False, help="use syslog")
  args = vars(ap.parse_args())
  
  log = logging.getLogger('netbase')
  if args['syslog']:
    log.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    # formatter for syslog (no date/time or appname. Just  msg.
    formatter = logging.Formatter('%(name)s-%(levelname)-5s: %(message)-40s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
  else:
    logging.basicConfig(level=logging.DEBUG,datefmt="%H:%M:%S",format='%(asctime)s %(levelname)-5s %(message)-40s')

  settings = Settings(args["conf"], 
                      log)
  
  hmqtt = Homie_MQTT(settings, msgInCb)
  settings.print()

  while True:
    pings = {}
    for ip in settings.ping_list:
      pings[ip] = ping_this(ip)
    time.sleep(settings.check_every)

if __name__ == '__main__':
  sys.exit(main())

