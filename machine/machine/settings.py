import os

MACHINE_NAME = os.getenv('MACHINE_NAME', 'MACHINE_1') 
MQTT_URL = os.getenv('MQTT_URL','localhost')
MQTT_PORT = os.getenv('MQTT_PORT',1883)