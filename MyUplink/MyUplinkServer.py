import time
import os
import configparser
import random
import logging
import logging.handlers
import paho.mqtt.client as mqtt

from MyUplinkApi import myuplinkapi

VERSION = "0.1.00"

script_name = os.path.basename(__file__).split('.')[0]
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s ' + script_name + ' ver:' + str(VERSION) + ' %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler(script_name + ".log", mode='a', maxBytes=8388608, backupCount=16)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Starting ...")

def getConfig(kind):
    home = os.path.expanduser("~")
    inifile = home + "/.MyUplink.ini"
    config = configparser.ConfigParser()
    config.read(inifile)
    try:
        if kind == "MYUPLINK":
            return config['MYUPLINK']['USERNAME'], config['MYUPLINK']['PASSWORD']
        if kind == "MQTT":
            return config['MQTT']['USERNAME'], config['MQTT']['PASSWORD']
        if kind == "MQTTINFO":
            return config['MQTT']['SERVER'], config['MQTT']['PORT']
        if kind == "TOPIC":
            return config['MQTT']['TOPICBASE']
        if kind == "DATA":
            return config['MQTT']['DATALIST']
        if kind == "SLEEP":
            return config['MQTT']['SLEEPTIME']
    except KeyError:
        return ""

def on_connect(m_client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected to MQTT broker with result code {rc}")
    else:
        logger.error(f"Failed to connect to MQTT broker, return code {rc}")

def on_disconnect(client, userdata,rc=0):
    logger.info(f"DisConnected result code {str(rc)}")

def updateMQTT(client, topic, name, mqttData):
    for items in mqttData:
        ptopic = topic + "/" + name + "/" + capUnspace(items[1])
        if items[0] == '406':
            msg = items[3]
        else:
            if float(items[2]).is_integer():
                msg = int(items[2])
            else:
                msg = items[2]
        result = client.publish(ptopic, msg, 0, True)
        if result[0] == 0:
            logger.debug(f"Sendt `{msg}` to topic `{ptopic}`")
        else:
            logger.error(f"Failed to send message to topic {ptopic} Error code {result[0]}")

def capUnspace(s):
    return ''.join( (c.upper() if i == 0 or s[i-1] == ' ' else c) for i, c in enumerate(s) ).replace(" ", "")


SLEEPTIME = 300
TOPIC = getConfig("TOPIC")
DATAL = getConfig("DATA")

devid = ""
tleft = 0
sleep = SLEEPTIME

USERNAME, PASSWORD = getConfig("MYUPLINK")
mqttUSER, mqttPASS = getConfig("MQTT")
mqttHOST, mqttPORT = getConfig("MQTTINFO")
sleep = int(getConfig('SLEEP'))

upl = myuplinkapi()
upl.apiUserPasswd(USERNAME, PASSWORD)
upl.setLogger(logger)

client = mqtt.Client(f'python-mqtt-{random.randint(0, 1000)}')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(mqttUSER, mqttPASS)
client.connect(mqttHOST, int(mqttPORT), 600)
client.loop_start()

while True:
    if tleft < 2*SLEEPTIME:
        tleft = upl.authorize()

    if devid == "":
        devid =  upl.getDevID()
        name = upl.getDevName()

    mqttData = upl.getdevData(DATAL)

    updateMQTT(client, TOPIC, name, mqttData)

    time.sleep(sleep)
    tleft = tleft - sleep
    logger.info(f"Token lifetime left {tleft}s")

client.loop_stop()
    