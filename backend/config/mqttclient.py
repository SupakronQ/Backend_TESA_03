import paho.mqtt.client as mqtt
import os
import json
from ..config.db import conn
from ..models.waterpoint import Waterpoint
from pydantic import ValidationError

class MQTTClient:

    def __init__(self,host,port,username,password,topic,db):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.db = db

        # MQTT client
        self.client = mqtt.Client()

        #Set the callback function 
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        #Set the connection parameters
        self.client.username_pw_set(self.username,self.password)
        self.client.tls_set()

        # Connect to the broker
        self.client.connect(self.host, self.port)

    def on_connect(self,client,userdata,flags,rc):

        print(f"Connected with result code {rc}")
        # Subscribe to a topic when connected

        self.client.subscribe(self.topic)

    def on_message(self,client,userdata,msg):

        try :
            data = json.loads(msg.payload.decode())
            print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
            self.db.local.waterpoint.insert_one(dict(Waterpoint(**data)))
            print("---save success---")
        except (ValidationError, json.JSONDecodeError) as err:

            print(f"!!!invalid message: {msg.payload.decode()} on topic {msg.topic}")

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()


