""" Determine high power usage hours""" #pylint: disable=invalid-name
from datetime import datetime
import sys
import time
import logging
from influxdb import InfluxDBClient #pylint: disable=import-error

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

def main(): #pylint: disable=too-many-locals
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
    maxuse = ["MAX1", "MAX2", "MAX3"]

    year = datetime.now().year
    month = datetime.now().month
    s_date = str(year) + "-" + str(month) + "-01T00:00:01Z"

    client = InfluxDBClient(host='localhost', port='8086', database='hansensor')
#pylint: disable=line-too-long
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
    for i in range(3):
        x, s = arr[i] #pylint: disable=invalid-name
        pusage.append(x/1000)
        ustime.append(datetime_from_utc_to_local(s))
        sumu = sumu + pusage[i]
        jbody = influx_json(pusage[i], ustime[i], maxuse[i])
        client.write_points(jbody)

    avg = sumu/3
    jbody = influx_json(avg, ustime[0], "MAXAVG")
    client.write_points(jbody)

    client.close()

    logging.info('Processing finished ...')

if __name__ == "__main__":
    main()
