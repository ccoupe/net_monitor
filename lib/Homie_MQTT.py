#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import sys, traceback
import json
from datetime import datetime
from threading import Thread
import time

import time

class Homie_MQTT:

  def __init__(self, settings, msgInCb):
    self.settings = settings
    self.log = settings.log
    self.msgInCb = msgInCb
    # init server connection
    self.client = mqtt.Client(settings.mqtt_client_name, False)
    self.client.on_message = self.on_message
    self.client.on_disconnect = self.on_disconnect
    rc = self.client.connect(settings.mqtt_server, settings.mqtt_port)
    if rc != mqtt.MQTT_ERR_SUCCESS:
        self.log.warn("network missing?")
        exit()
    self.client.loop_start()
        
    self.sub = settings.mqtt_root+'/'+settings.mqtt_basic+'/cmd'
    self.log.debug("Homie_MQTT __init__")
    #self.create_topics(hdevice, hlname)
    for sub in [self.sub]:
      rc,_ = self.client.subscribe(sub)
      if rc != mqtt.MQTT_ERR_SUCCESS:
        self.log.warn("Subscribe failed: %d" %rc)
      else:
        self.log.debug("Init() Subscribed to %s" % sub)
    
 
  def on_subscribe(self, client, userdata, mid, granted_qos):
    self.log.debug("Subscribed to %s" % self.hurl_sub)

  def on_message(self, client, userdata, message):
    settings = self.settings
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    #self.log.debug("on_message %s %s" % (topic, payload))
    try:
      self.msgInCb(payload)
    except:
      traceback.print_exc()

    
  def isConnected(self):
    return self.mqtt_connected

  def on_connect(self, client, userdata, flags, rc):
    self.log.debug("Subscribing: %s %d" (type(rc), rc))
    if rc == 0:
      self.log.debug("Connecting to %s" % self.mqtt_server_ip)
      rc,_ = self.client.subscribe(self.hurl_sub)
      if rc != mqtt.MQTT_ERR_SUCCESS:
        self.log.debug("Subscribe failed: ", rc)
      else:
        self.log.debug("Subscribed to %s" % self.hurl_sub)
        self.mqtt_connected = True
    else:
      self.log.debug("Failed to connect: %d" %rc)
    self.log.debug("leaving on_connect")
       
  def on_disconnect(self, client, userdata, rc):
    self.mqtt_connected = False
    log("mqtt reconnecting")
    self.client.reconnect()
    
