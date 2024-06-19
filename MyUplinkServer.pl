import requests
import json
import time
import sys
import os
import configparser

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
    response = requests.post(authurl, headers=headers, data=payload)
    if response.status_code == 200:
        tResponse = response.json()
        lifetime = tResponse["expires_in"]
        token = tResponse["access_token"]
        print(f"Got token with lifetime {lifetime}s")
        return token, lifetime
    else:
         print(f"Failed to get a token: {response.status_code}")
         sys.exit(1)

def getdevID(BASEURL, dheaders):
    url = BASEURL + "/v2/systems/me"
    response = requests.get(url, headers=dheaders)
    if response.status_code == 200:
        sysList = response.json()
        ndev = sysList["numItems"]
        for i in range(ndev):
            sys = sysList["systems"][i]
            dev = sys["devices"]
            if sys["securityLevel"] == "admin":
                devid = dev[0]["id"]
            print(f"Found device {devid}")
            return devid
    else:
        print(f"Failed to get devices: {response.status_code}")
        sys.exit(2)

def getdevData(BASEURL, dheaders):
    params = "406,527,528,404,302,400,303,509,514"
    url = BASEURL + "/v2/devices/" + devid + "/points?parameters=" + params
    response = requests.get(url, headers=dheaders)
    if response.status_code == 200:
        dlist = response.json()
        for item in dlist:
            if item["parameterId"] == '406':
                unit = item["strVal"]
            else:
                unit = item["parameterUnit"]
            print(item["parameterId"], item["parameterName"], item["value"], unit)
        print("")
    else:
        print(f"Failed to get device data: {response.status_code}")
        sys.exit(3)

def getConfig(kind):
    home = os.path.expanduser("~")
    inifile = home + "/.MyUplinkServer.ini"
    config = configparser.ConfigParser()
    config.read(inifile)
    try:
        if kind == "MYUPLINK":
            return config['MYUPLINK']['USERNAME'], config['MYUPLINK']['PASSWORD']
    except KeyError:
        return ""

BASEURL = "https://api.myuplink.com"
SLEEPTIME = 300

devid = ""
tleft = 0

USERNAME, PASSWORD = getConfig("MYUPLINK")
while True:
    if tleft < 2*SLEEPTIME:
        token, tleft = authorize(BASEURL, USERNAME, PASSWORD)
        dheaders = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + token
        }

    if devid == "":
        devid = getdevID(BASEURL, dheaders)

    getdevData(BASEURL, dheaders)
    
    time.sleep(SLEEPTIME)
    tleft = tleft - SLEEPTIME
    print(f"Token lifetime left {tleft}s")