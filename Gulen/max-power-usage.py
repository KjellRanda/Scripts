
from datetime import datetime
from time import mktime
import time
import logging
from influxdb import InfluxDBClient

def datetime_from_utc_to_local(utc):
    epoch = time.mktime(time.strptime(utc, '%Y-%m-%dT%H:%M:%SZ'))
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return (datetime.strptime(utc, '%Y-%m-%dT%H:%M:%SZ') + offset).strftime('%Y-%m-%d %H:%M:%S')

def influx_json(val, time, type):
    json_body = [
        {
            "measurement": "mqtt_consumer",
            "tags": {
                "Maxusage": type
            },
            "fields": {
                "value": val,
                "date": time
            }
        }
    ]
    return json_body

logging.basicConfig(filename='maxusage.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Processing starting ...')

arr = []
pusage = []
ustime = []
maxuse = ["MAX1", "MAX2", "MAX3"]

year = datetime.now().year
month = datetime.now().month
sdate = str(year) + "-" + str(month) + "-01T00:00:01Z"

client = InfluxDBClient(host='localhost', port='8086', database='hansensor')

SQL = "SELECT INTEGRAL(\"mean\")/3600 FROM ( SELECT MEAN(\"val\") AS mean FROM \"mqtt_consumer\" " + \
      "WHERE \"topic\" = \'pt:j1/mt:evt/rt:dev/rn:zigbee/ad:1/sv:meter_elec/ad:1_1\' AND \"val\" < 20000 AND time <= now() and time >= \'" + \
       sdate + "\' GROUP BY time(5s) fill(previous) ) GROUP BY time(1h)"
result = client.query(SQL)

n = 0
points = result.get_points()
for point in points:
    arr.append([point['integral'],point['time']])
    n = n + 1

if n <= 3:
    logging.warning("Not enough data to contine. Only " + str(n) + " found")
    client.close()
    exit()

arr.sort(reverse=True)

sum = 0.0
for i in range(3):
    x, s = arr[i]
    pusage.append(x/1000)
    ustime.append(datetime_from_utc_to_local(s))
    sum = sum + pusage[i]
    jbody = influx_json(pusage[i], ustime[i], maxuse[i])
    client.write_points(jbody)

avg = sum/3
jbody = influx_json(avg, ustime[0], "MAXAVG")
client.write_points(jbody)

client.close()

logging.info('Processing finished ...')