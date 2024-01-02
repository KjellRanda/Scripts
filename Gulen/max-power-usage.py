""" Determine high power usage hours"""
from datetime import datetime
import sys
import time
import logging
from influxdb import InfluxDBClient

def datetime_from_utc_to_local(utc):
    """
    Convert date and time from UTC to local time
    """
    epoch = time.mktime(time.strptime(utc, '%Y-%m-%dT%H:%M:%SZ'))
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return (datetime.strptime(utc, '%Y-%m-%dT%H:%M:%SZ') + offset).strftime('%Y-%m-%d %H:%M:%S')

def influx_json(val, timev, typev):
    """
    Create json structure for line protocol in Influxdb
    """
    json_body = [
        {
            "measurement": "mqtt_consumer",
            "tags": {
                "Maxusage": typev
            },
            "fields": {
                "value": val,
                "date": timev
            }
        }
    ]
    return json_body

def main():
    """
    Find 3 hours each month with highest energy usage
    Store values in Influxdb
    """
    logging.basicConfig(filename='maxusage.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S', \
                        level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Processing starting ...')

    arr = []
    pusage = []
    ustime = []
    usdate = []
    maxuse = ["MAX1", "MAX2", "MAX3"]

    year = datetime.now().year
    month = datetime.now().month
    s_date = str(year) + "-" + str(f"{month:02d}") + "-01T00:00:01Z"

    client = InfluxDBClient(host='localhost', port='8086', database='hansensor')
    c_sql = "SELECT INTEGRAL(\"mean\")/3600 FROM ( SELECT MEAN(\"val\") AS mean FROM \"mqtt_consumer\" " + \
          "WHERE \"topic\" = \'pt:j1/mt:evt/rt:dev/rn:zigbee/ad:1/sv:meter_elec/ad:1_1\' AND \"unit\" = \'W\' AND time <= now() and time >= \'" + \
           s_date + "\' GROUP BY time(5s) fill(previous) ) GROUP BY time(1h)"
    result = client.query(c_sql)

    num = 0
    points = result.get_points()
    for point in points:
        arr.append([point['integral'],point['time']])
        num = num + 1

    if num <= 3:
        logging.warning("Not enough data to contine. Only %s found", str(num))
        client.close()
        sys.exit(1)

    arr.sort(reverse=True)

    sumu = 0.0
    n = 0
    for i in range(len(arr)):
        x, s = arr[i]
        t = datetime_from_utc_to_local(s)
        d = t.split()
        if not d[0] in usdate:
            pusage.append(x/1000)
            ustime.append(t)
            usdate.append(d[0])
            sumu = sumu + pusage[n]
            jbody = influx_json(pusage[n], ustime[n], maxuse[n])
            client.write_points(jbody)
            n = n + 1
        if n == 3:
            break;

    avg = sumu/n
    jbody = influx_json(avg, ustime[0], "MAXAVG")
    client.write_points(jbody)

    client.close()

    logging.info('Processing finished. %s values processed...', str(n))

if __name__ == "__main__":
    main()
