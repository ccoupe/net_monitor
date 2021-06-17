import json
import socket
from uuid import getnode as get_mac
import os 
import sys

class Settings:

  def __init__(self, etcf, log):
    self.etcfname = etcf
    self.log = log
    self.mqtt_server = "192.168.1.7"   # From json
    self.mqtt_port = 1883              # From json
    self.mqtt_client_name = "detection_1"   # From json
    self.homie_device = None            # From json
    self.homie_name = None              # From json
    # IP and MacAddr are not important (should not be important).
    if sys.platform.startswith('linux'):
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      s.connect(('<broadcast>', 0))
      self.our_IP =  s.getsockname()[0]
      # from stackoverflow (of course):
      self.macAddr = ':'.join(("%012x" % get_mac())[i:i+2] for i in range(0, 12, 2))
    elif sys.platform.startswith('darwin'):
      host_name = socket.gethostname() 
      self.our_IP = socket.gethostbyname(host_name) 
      self.macAddr = ':'.join(("%012x" % get_mac())[i:i+2] for i in range(0, 12, 2))
    else:
      self.our_IP = "192.168.1.255"
      self.macAddr = "de:ad:be:ef"
    self.load_settings(self.etcfname)
    print("Settings from", self.etcfname)
    
  def load_settings(self, fn):
    conf = json.load(open(fn))
    self.mqtt_server = conf.get("mqtt_server_ip", "192.168.1.255")
    self.mqtt_port = conf.get("mqtt_port", 1883)
    self.mqtt_client_name = conf.get("mqtt_client_name", "Bad Client")
    #  Homie, 
    self.mqtt_root = conf.get("mqtt_root", "homie/network/status")
    self.mqtt_basic = conf.get("mqtt_basic", "basic")     # is a property, root+basic+/set
    self.mqtt_tb = conf.get("mqtt_tb" "trumpybear")      
    self.check_every = conf.get("check_every", 120)
    self.ping_list = conf.get("ping_list", None)
    self.hubitat = conf.get("hubitat", "192.168.1.5")

  def print(self):
    print("==== Settings ====")
    print(self.settings_serialize())
  
  def settings_serialize(self):
    st = {}
    st['mqtt_server_ip'] = self.mqtt_server
    st['mqtt_port'] = self.mqtt_port
    st['mqtt_client_name'] = self.mqtt_client_name
    st["mqtt_root"] = self.mqtt_root
    st["mqtt_basic"] = self.mqtt_basic
    st["mqtt_tb"] = self.mqtt_tb
    st["check_every"] = self.check_every
    st["ping_list"] = self.ping_list
    st["hubitat"] = self.hubitat
    str = json.dumps(st)
    return str

  def settings_deserialize(self, jsonstr):
    st = json.loads(jsonstr)
