""" Module to test Futurehome mqtt broker """
import json
from datetime import datetime
from time import mktime
import paho.mqtt.client as mqtt #pylint: disable=import-error

def timemark(timestamp):
    """ Create timemark for Influxdb data """
    date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z").date()
    time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z").time()

    dt = datetime.combine(date, time) #pylint: disable=invalid-name
    msepoc = int((mktime(dt.timetuple()) + dt.microsecond/1000000.0)*1000)

    return dt, msepoc

def print_pdata(jdata, report, dt0, msepoc):
    """ Print ampere and volt values """
    a_fac = 1000
    v_fac = 10
#    power = float(data["val"]["p_import"])
    power = 0
#pylint: disable=invalid-name
    i1 = float(jdata["val"]["i1"])/a_fac
    i2 = float(jdata["val"]["i2"])/a_fac
    i3 = float(jdata["val"]["i3"])/a_fac
    u1 = float(jdata["val"]["u1"])/v_fac
    u2 = float(jdata["val"]["u2"])/v_fac
    u3 = float(jdata["val"]["u3"])/v_fac
    print(f'{report} \t{dt0} \t{msepoc} \t{power:7.1f}W\t({i1:6.3f}A {i2:6.3f}A {i3:6.3f}A)  ({u1:5.1f}V {u2:5.1f}V {u3:5.1f}V)') #pylint: disable=line-too-long

def on_connect(m_client, userdata, flags, rc0): #pylint: disable=unused-argument
    """ Mqtt connect callback function """
    print(f"Connected with result code {rc0}")
    m_client.subscribe([("pt:j1/mt:evt/rt:dev/rn:zigbee/ad:1/sv:meter_elec/ad:1_1",0),\
                        ("pt:j1/mt:evt/rt:app/rn:energy_guard/ad:1",0)])

def on_message(m_client, userdata, msg): #pylint: disable=unused-argument
    """ Mqtt message callback function """
#    print(f"Message received [{msg.topic}]: {msg.payload}")
    data = json.loads(msg.payload)
    report = data["type"]
    timestamp = data["ctime"]
    (dt, msepoc) = timemark(timestamp) #pylint: disable=invalid-name

    if report == "evt.meter.report":
        power = float(data["val"])
        unit = data["props"]["unit"]
        print(f'{report} \t{dt} \t{msepoc} \t{power:7.1f}{unit}')

    if report == "evt.meter_ext.report":
        print_pdata(data, report, dt, msepoc)

client = mqtt.Client("mqtt-test")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqtt", "mqtt01")
client.connect('192.168.86.88', 1884, 300)

client.loop_forever()
