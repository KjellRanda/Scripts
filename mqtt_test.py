import paho.mqtt.client as mqtt
import json
from datetime import datetime
from time import mktime


def timemark(timestamp):
    date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z").date()
    time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z").time()

    dt = datetime.combine(date, time)
    msepoc = int((mktime(dt.timetuple()) + dt.microsecond/1000000.0)*1000)

    return dt, msepoc


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("pt:j1/mt:evt/rt:dev/rn:zigbee/ad:1/sv:meter_elec/ad:1_1")


def on_message(client, userdata, msg):
    #print(f"Message received [{msg.topic}]: {msg.payload}")
    data = json.loads(msg.payload)
    report = data["type"]
    timestamp = data["ctime"]
    (dt, msepoc) = timemark(timestamp)

    if report == "evt.meter.report":
        power = float(data["val"])
        unit = data["props"]["unit"]
        print("%s \t%s \t%i \t%7.1f%s" %(report, dt, msepoc, power, unit))

    if report == "evt.meter_ext.report":
        power = float(data["val"]["p_import"])
        i1 = float(data["val"]["i1"])
        i2 = float(data["val"]["i2"])
        i3 = float(data["val"]["i3"])
        u1 = float(data["val"]["u1"])
        u2 = float(data["val"]["u2"])
        u3 = float(data["val"]["u3"])
        print("%s \t%s \t%i \t%7.1fW\t(%6.3fA %6.3fA %6.3fA)  (%5.1fV %5.1fV %5.1fV)" %(report, dt, msepoc, power, i1, i2, i3, u1, u2, u3))

client = mqtt.Client("mqtt-test")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqtt", "mqtt01")
client.connect('192.168.1.102', 1884, 300)

client.loop_forever()