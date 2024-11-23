import json
import os
from datetime import datetime
import logging
import logging.handlers
import holidays

from MyUplinkApi import myuplinkapi
from MyUplinkUtil import MyUptimeConfig
from MyUplinkConst import MODE_M4, MODE_M5, MODE_M6, POWER_PRICE_HIGH, POWER_PRICE_MEDIUM, POWER_PRICE_LOW
from MyUplinkConst import DEF_MAX_POWER_HOURS, DEF_MEDIUM_POWER_HOURS
from MyUplinkConst import FILE_SCHEDULE, FILE_SCHEDULE_MODE

VERSION = "0.1.30"

script_name = os.path.basename(__file__).split('.')[0]
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s ' + script_name + ' ver:' + str(VERSION) + ' %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler(script_name + ".log", mode='a', maxBytes=8388608, backupCount=16)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Starting ...")

def dailyPriceList(lines):
    pricel = {}
    id = 1
    for line in lines:
        arr = line.replace("\n", "").split()
        string = '{"sdate":"' + arr[0] + '", "stime":"' + arr[1] + '", "edate":"' + arr[3] + '", "etime":"' + arr[4] + '", "price":"' + arr[8] + '"}'
        pricel[id] = json.loads(string)
        id = id + 1
    return pricel

def updatePriceList(pricel, pricesd, MaxPowerHours, MediumPowerHours):
    n = 0
    for line in pricesd.items():
        if n < MaxPowerHours:
            s = POWER_PRICE_LOW
        elif n < MaxPowerHours + MediumPowerHours:
            s = POWER_PRICE_MEDIUM
        else:
            s = POWER_PRICE_HIGH
        pricel[line[0]]['state'] = s
        n = n + 1
    return pricel

def buildJsonPrice(pricel):
    pjson = ''
    usedMode = 0
    for line in pricel.items():
        s = line[1]['state']
        if s == POWER_PRICE_HIGH:
            mode = MODE_M4
        if s == POWER_PRICE_MEDIUM:
            mode = MODE_M5
        if s == POWER_PRICE_LOW:
            mode = MODE_M6

        if usedMode != mode:
            pjson += '{"enabled": true,'
            pjson += '"modeId": ' + str(mode)  + ',"startDay": "' + wday + '",'
            pjson += '"startTime": "' + line[1]['stime'] + '","stopDay": null,"stopTime": null},'
            usedMode = mode
    return pjson

def readGridFee(nFile):
    f = open(nFile)
    allLines = f.readlines()[2: ]
    f.close()

    price = [None]*4
    n = 0
    for line in allLines:
        arr = line.replace("\n", "").split()
        price[n] = float(arr[3])/100
        price[n+1] = float(arr[4])/100
        n += 2
    return price

def getGridFee(price, date):
    winter = [1,2,3]
    weekend = [5,6]

    no_holidays = holidays.NO()
    day = datetime.strptime(date, "%Y-%m-%d").date()

    wend = False
    wnt = False
    if day.weekday() in weekend or day in no_holidays:
        wend = True
    if day.month in winter:
        wnt = True

    prc = [0]*24
    for i in range(len(prc)):
        if wnt:
            if wend:
                prc[i] = price[1]
            else:
                if (i < 6 or i > 21):
                    prc[i] = price[1]
                else:
                    prc[i] = price[0]
        else:
            if wend:
                prc[i] = price[3]
            else:
                if (i < 6 or i > 21):
                    prc[i] = price[3]
                else:
                    prc[i] = price[2]
    return prc


weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
jstring = '[{"weeklyScheduleId": 0,"weekFormat": "mon,tue,wed,thu,fri,sat,sun","events": ['

MaxPowerHours = DEF_MAX_POWER_HOURS
MediumPowerHours = DEF_MEDIUM_POWER_HOURS

scheduleFile = FILE_SCHEDULE
scheduleFileMode = FILE_SCHEDULE_MODE

iniConf = MyUptimeConfig(".MyUplink.ini")

USERNAME = iniConf.getKey('MYUPLINK', 'USERNAME')
PASSWORD = iniConf.getKey('MYUPLINK', 'PASSWORD')

if int(iniConf.getKey('SCHEDULE', 'CHEAPHOURS')):
    MaxPowerHours = int(iniConf.getKey('SCHEDULE', 'CHEAPHOURS'))
if int(iniConf.getKey('SCHEDULE', 'MEDIUMHOURS')):
    MediumPowerHours = int(iniConf.getKey('SCHEDULE', 'MEDIUMHOURS'))

priceFile = iniConf.getKey('SCHEDULE', 'PRICEFILE')
nFile = iniConf.getKey('SCHEDULE', 'GRIDFEE')

if iniConf.getKey('SCHEDULE', 'SCHEDULEFILE'):
    scheduleFile = iniConf.getKey('SCHEDULE', 'SCHEDULEFILE')
if iniConf.getKey('SCHEDULE', 'SCHEDULEFILEMODE'):
    scheduleFileMode = iniConf.getKey('SCHEDULE', 'SCHEDULEFILEMODE')

upl = myuplinkapi()
upl.apiUserPasswd(USERNAME, PASSWORD)
upl.setIntAPI()
upl.setLogger(logger)

tleft = upl.authorize()

devid = upl.getDevID()

f = open(priceFile)
logger.info(f"Reading powerprice from {priceFile}")
allLines = f.readlines()[1: ]
f.close()

price = readGridFee(nFile)
logger.info(f"Reading gridfee from {nFile}")

n1 = 0
for i in range(2):
    lines = allLines[n1:n1+24]
    n1 += 24
    pricel = dailyPriceList(lines)

    pdate = pricel[1]['sdate']
    wday = weekdays[datetime.strptime(pdate, '%Y-%m-%d').weekday()]
    logger.info(f"Date {pdate} is weekday {wday}")

    prc = getGridFee(price, pdate)

    for j in range(len(prc)):
        pricel[j+1]['price'] = f"{prc[j]+float(pricel[j+1]['price']):.4f}"

    slist = sorted(pricel.items(), key=lambda item: float(item[1]['price']), reverse=False)
    pricesd = dict(slist)

    pricel = updatePriceList(pricel, pricesd, MaxPowerHours, MediumPowerHours)

    pjson = buildJsonPrice(pricel)
    if i == 0:
        wday1 = wday
        pstring1 = pjson
    else:
        wday2 = wday
        pstring2 = pjson

    for j in pricel.items():
        logger.debug(f"{j}")

for day in weekdays:
    if day == wday1:
        jstring += pstring1
    elif day == wday2:
        jstring += pstring2
    else:
        jstring += '{"enabled": true,"modeId": ' + str(MODE_M6) + ',"startDay": "' + day + '","startTime": "00:00:00","stopDay": null,"stopTime": null},'
        jstring += '{"enabled": true,"modeId": ' + str(MODE_M4) + ',"startDay": "' + day + '","startTime": "06:00:00","stopDay": null,"stopTime": null},'
        jstring += '{"enabled": true,"modeId": ' + str(MODE_M5) + ',"startDay": "' + day + '","startTime": "12:00:00","stopDay": null,"stopTime": null},'

jstring = jstring[:-1]
jstring += ']}]'
json_data = json.dumps(json.loads(jstring))
upl.updateSchedule(json_data)
