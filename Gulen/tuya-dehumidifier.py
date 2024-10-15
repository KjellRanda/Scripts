import time
import json
import logging
import logging.handlers
import tinytuya
from influxdb import InfluxDBClient

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler("tuya-dehumidifier.log", mode='a', maxBytes=8388608, backupCount=16)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Starting ...")

DEVICEFILE = "devices.json"

f = open(DEVICEFILE)
data = json.load(f)
f.close()

id = data[0]['id']
key = data[0]['key']
ip = data[0]['ip']
ver = float(data[0]['version'])

map = data[0]['mapping']

num = [2, 6, 18, 19]

client = InfluxDBClient(host='localhost', port='8086', database='hansensor')
while True:
    d = tinytuya.Device(id, ip, key, version=ver)
    devdata = d.status()
    if "Error" in devdata and devdata['Err'] == "901":
        logger.error("Device at IP %s is offline", ip)
    else:
        message = '[{' +  '"measurement": "tuya", "tags": {"name": "avfukter", "ipaddr": "' + ip + '"}, "fields": {'
        for item in devdata['dps']:
            if int(item) in num:
               message += '"' + str(map[item]['code']) + '": ' + str(devdata['dps'][item]) + ', '
            else:
               message += '"' + str(map[item]['code']) + '": "' + str(devdata['dps'][item]) + '", '
        message = message[:-2]
        message += '}}]'
        logger.info(json.dumps(json.loads(message), indent=4))
        client.write_points(json.loads(message))
    time.sleep(600)