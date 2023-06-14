import threading
from machine.settings import MACHINE_NAME, MQTT_URL, MQTT_PORT
import pika
import json
import logging
from machine.infra import get_db
from machine.machine import Machine
import random
import time
from paho.mqtt import client as mqtt_client
import dataclasses


MQTT_TOPIC = f"cnc/{MACHINE_NAME}"
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(MQTT_CLIENT_ID)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(MQTT_URL, MQTT_PORT)
    return client

client_mqtt = connect_mqtt()
client_mqtt.loop_start()

def receive_thread():
    QUEUE_NAME = f'RC_{MACHINE_NAME}'
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    

    def callback(ch, method, properties, body):
        db = None
        db_cursor = None
        try:
            message = json.loads(body.decode())
            db = get_db()
            db_cursor = db.cursor()
            for i in range(10):
                machine = Machine(program='PROGRAM'
                , rpm=random.randint(100,3000)
                , x=random.randint(0,100)
                , y=random.randint(0,100)
                , z=random.randint(0,100))
                db_cursor.execute('UPDATE MACHINES SET PROGRAM=?, RPM=?, X=?, Y=?, Z=?', (
                    machine.program,
                    machine.rpm,
                    machine.x,
                    machine.y,
                    machine.z,             
                ))
                db.commit()
                client_mqtt.publish(MQTT_TOPIC, json.dumps(dataclasses.asdict(machine)))
                time.sleep(5)

        except Exception as e:            
            logging.exception(e)
        finally:
            if db_cursor is not None:
                db_cursor.close()
            if db is not None:
                db.close()



    channel.basic_consume(queue=QUEUE_NAME,
                        auto_ack=True,
                        on_message_callback=callback)
    channel.start_consuming()
    client_mqtt.loop_stop()

def start_receive():
    t_msg = threading.Thread(target=receive_thread)
    t_msg.start()
    t_msg.join(0)
    