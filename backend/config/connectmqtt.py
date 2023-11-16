import paho.mqtt.client as mqtt
import os
from ..config.db import conn
from pydantic import ValidationError
from .mqttclient import MQTTClient
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# MQTT connection parameters
host = os.getenv('MQTT_HOST')
port = int(os.getenv('MQTT_PORT'))
username = os.getenv('MQTT_USERNAME')
password = os.getenv('MQTT_PASSWORD')
topic = os.getenv('MQTT_TOPIC')

client = MQTTClient(host,port,username,password,topic,conn)

