import os
import random
from datetime import datetime
import json
import paho.mqtt.client as mqtt

from MyUplinkUtil import MyUptimeConfig, myLogger
from MyUplinkConst import FILE_SCHEDULE, FILE_SCHEDULE_MODE

def readSchedule(sFile):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    with open(sFile, 'r', encoding='utf8') as f:
        data = json.load(f)
        f.close()
        nEvents = len(data[0]['events'])
        tNow = datetime.now()
        toDay = weekdays[tNow.weekday()]
        hNow = tNow.hour
        for i in range(nEvents-1, -1,- 1):
            if data[0]['events'][i]['startDay'] == toDay:
                dHour = int(data[0]['events'][i]['startTime'].split(':')[0])
                if dHour <= hNow:
                    fMode = data[0]['events'][i]['modeId']
                    return fMode
    return None

def readScheduleMode(smFile, fMode):
    with open(smFile, 'r', encoding='utf8') as f:
        data = json.load(f)
        f.close()
        for i in range(len(data)):
            if data[i]['modeId'] == fMode:
                fName =  data[i]['name']
                return fName
    return None

def updateMQTT(iniConf, logger, fName):
    mqttUSER = iniConf.getKey('MQTT', 'USERNAME')
    mqttPASS = iniConf.getKey('MQTT', 'PASSWORD')
    mqttHOST = iniConf.getKey('MQTT', 'SERVER')
    mqttPORT = iniConf.getKey('MQTT', 'PORT')
    TOPIC = iniConf.getKey('MQTT', 'TOPICBASE')

    client = mqtt.Client(f'python-mqtt-{random.randint(0, 1000)}')

    client.username_pw_set(mqttUSER, mqttPASS)
    client.connect(mqttHOST, int(mqttPORT), 600)

    client.loop_start()
    mTopic = TOPIC + "/VVB/scheduleMode"
    result = client.publish(mTopic, fName, 0, True)
    if result[0] == 0:
        logger.debug("Sendt %s to topic %s", fName, mTopic)
    else:
        logger.error("Failed to send message to topic %s Error code %i", mTopic, result[0])
    client.loop_stop()
    return

def main():
    VERSION = "0.1.10"
    script_name = os.path.basename(__file__).split('.')[0]
    lo = myLogger(script_name, VERSION)
    logger = lo.getLogger()

    scheduleFile = FILE_SCHEDULE
    scheduleFileMode = FILE_SCHEDULE_MODE

    iniConf = MyUptimeConfig(".MyUplink.ini")

    if iniConf.getKey('SCHEDULE', 'SCHEDULEFILE'):
        scheduleFile = iniConf.getKey('SCHEDULE', 'SCHEDULEFILE')
    if iniConf.getKey('SCHEDULE', 'SCHEDULEFILEMODE'):
        scheduleFileMode = iniConf.getKey('SCHEDULE', 'SCHEDULEFILEMODE')

    fMode = readSchedule(scheduleFile)
    fName = readScheduleMode(scheduleFileMode, fMode)

    updateMQTT(iniConf, logger, fName)

    logger.info("Finishing ...")

if __name__ == "__main__":
    main()
