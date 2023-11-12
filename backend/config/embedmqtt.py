import paho.mqtt.client as mqtt
import os
import json
from ..config.db import conn
from ..models.waterpoint import Waterpoint
from pydantic import ValidationError

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# MQTT connection parameters
host = os.getenv('MQTT_HOST')
port = int(os.getenv('MQTT_PORT'))
username = os.getenv('MQTT_USERNAME')
password = os.getenv('MQTT_PASSWORD')

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to a topic when connected
    client.subscribe('testtopic/1')

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    try :
        data = json.loads(msg.payload.decode())
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        conn.local.waterpoint.insert_one(dict(Waterpoint(**data)))
        print("---save success---")
    except (ValidationError, json.JSONDecodeError) as err:

        print(f"!!!invalid message: {msg.payload.decode()} on topic {msg.topic}")

# Initialize the MQTT client
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Set the connection parameters
client.username_pw_set(username, password)
client.tls_set()

# Connect to the broker
client.connect(host, port, 60)
