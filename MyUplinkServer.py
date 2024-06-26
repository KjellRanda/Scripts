import json
import time
import sys
import os
import configparser
import random
import logging
import logging.handlers
import requests
import paho.mqtt.client as mqtt

VERSION = "0.0.001"

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler("MyUplinkServer.log", mode='a', maxBytes=8388608, backupCount=16)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Starting ...")

def authorize(BASEURL, USERNAME, PASSWORD):
    authurl = BASEURL + "/oauth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "client_id": "My-Uplink-Web",
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(authurl, headers=headers, data=payload, timeout=60)
    if response.status_code == 200:
        tResponse = response.json()
        lifetime = tResponse["expires_in"]
        token = tResponse["access_token"]
        logger.info(f"Got token with lifetime {lifetime}s")
        return token, lifetime
    logger.error(f"Failed to get a token: {response.status_code}")
    sys.exit(1)

def getdevID(BASEURL, dheaders):
    url = BASEURL + "/v2/systems/me"
    response = requests.get(url, headers=dheaders, timeout=60)
    if response.status_code == 200:
        sysList = response.json()
        ndev = sysList["numItems"]
        for i in range(ndev):
            sys = sysList["systems"][i]
            dev = sys["devices"]
            if sys["securityLevel"] == "admin":
                devid = dev[0]["id"]
                name = sys["name"]
            logger.info(f"Found device {devid} with name {name}")
            return devid, name
    logger.error(f"Failed to get devices: {response.status_code}")
    sys.exit(2)

def getdevData(BASEURL, dheaders, params):
    mqttData = []
    url = BASEURL + "/v2/devices/" + devid + "/points?parameters=" + params
    response = requests.get(url, headers=dheaders, timeout=60)
    if response.status_code == 200:
        dlist = response.json()
        for item in dlist:
            if item["parameterId"] == '406':
                unit = item["strVal"]
            else:
                unit = item["parameterUnit"]
            mqttData.append([item["parameterId"], item["parameterName"], item["value"], unit])
            logger.debug(f'{item["parameterId"]} {item["parameterName"]} {item["value"]} {unit}')
        return mqttData
    logger.error(f"Failed to get device data: {response.status_code}")
    sys.exit(3)

def getConfig(kind):
    home = os.path.expanduser("~")
    inifile = home + "/.MyUplinkServer.ini"
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


BASEURL = "https://api.myuplink.com"
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

client = mqtt.Client(f'python-mqtt-{random.randint(0, 1000)}')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.username_pw_set(mqttUSER, mqttPASS)
client.connect(mqttHOST, int(mqttPORT), 600)
client.loop_start()

while True:
    if tleft < 2*SLEEPTIME:
        token, tleft = authorize(BASEURL, USERNAME, PASSWORD)
        dheaders = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + token
        }

    if devid == "":
        devid, name = getdevID(BASEURL, dheaders)

    mqttData = getdevData(BASEURL, dheaders, DATAL)

    updateMQTT(client, TOPIC, name, mqttData)

    time.sleep(sleep)
    tleft = tleft - sleep
    logger.info(f"Token lifetime left {tleft}s")

client.loop_stop()
    