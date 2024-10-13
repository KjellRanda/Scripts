"""
Program to get today and tomorrow from Entsoe and exchange rate from Norges Bank.
"""
from datetime import date, timedelta, datetime
import sys
import os
import time
import configparser
from io import StringIO, BytesIO
import logging
import logging.handlers
import re
import requests
from lxml import etree as ET
import pandas as pd
import numpy as np

xslt='''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="no"/>

<xsl:template match="/|comment()|processing-instruction()">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

<xsl:template match="*">
    <xsl:element name="{local-name()}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
</xsl:template>

<xsl:template match="@*">
    <xsl:attribute name="{local-name()}">
      <xsl:value-of select="."/>
    </xsl:attribute>
</xsl:template>
</xsl:stylesheet>
'''

VERSION = "1.1.000"

script_name = os.path.basename(__file__).split('.')[0]
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s ' + script_name + ' ver:' + str(VERSION) + ' %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler("powerprice.log", mode='a', maxBytes=8388608, backupCount=16)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Starting ...")

def datetime_from_utc_to_local(utc):
    """ Convert date and time from UTC to local time """
    epoch = time.mktime(time.strptime(utc, '%Y-%m-%dT%H:%MZ'))
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return (datetime.strptime(utc, '%Y-%m-%dT%H:%MZ') + offset).strftime('%Y-%m-%d %H:%M')

def getEntsoePrice(area, apikey):
    """ Get power price as xml from Entsoe using their api """
    baseURL = "https://web-api.tp.entsoe.eu/api"
    docCode = "A44"

    today = date.today()
    startDate = str(today.strftime("%Y%m%d")) + "0000"
    tomorrow = today + timedelta(1)
    endDate = str(tomorrow.strftime("%Y%m%d")) + "0000"

    url = baseURL + "?documentType=" + docCode + "&in_Domain=" + area + "&out_Domain=" + area + "&periodStart=" + startDate + "&periodEnd=" + endDate + "&securityToken=" + apikey
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.text.encode('UTF-8')
    logger.error(f"Error getting data from Entsso-E. Reurn code = {response.status_code}")
    sys.exit(3)

def parseXML(xml, lxslt):
    """ Parse the Entsoe xml and extract price in Euro for each hour for today and tomorrow if it is available
        Remove xml namespace using the xslt structure """

    rlist = []
    tree = ET.parse(BytesIO(xml))
    transform=ET.XSLT(ET.parse(StringIO(lxslt)))
    tree = transform(tree)
    root = tree.getroot()
    for i in root.findall('./TimeSeries/Period'):
        res = i.find('resolution')
        tstart = i.find('timeInterval/start')
        t0 = datetime.strptime(datetime_from_utc_to_local(tstart.text),'%Y-%m-%d %H:%M')
        td = timedelta(minutes=int(re.findall(r'\d+', res.text)[0]))
        for j in i.findall('Point'):
            period = j.find('position')
            price = j.find('price.amount')
            t1 = t0 + td*(int(period.text) - 1)
            a = []
            a.append(t1)
            a.append(t1 + td)
            a.append(int(period.text))
            a.append(float(price.text))
            rlist.append(a)
    return rlist

def valutaKursNB():
    """ Get the exchange rate Euro to NOK from Norges Bank using their api
        Use tlatest exchange rate available """

    url = "https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=1&locale=no"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()
    logger.error(f"Error getting data from Norges Bank code = {response.status_code}")
    sys.exit(3)

def getEntsoeArea(area):
    """ Get the Entsoe area code from Norwegian area codes """
    entsoeArea = [["NO1", "10YNO-1--------2", "Oslo"],
                  ["NO2", "10YNO-2--------T", "Kristiansand"],
                  ["NO3", "10YNO-3--------J", "Trondheim"],
                  ["NO4", "10YNO-4--------9", "Tromsø"],
                  ["NO5", "10Y1001A1001A48H", "Bergen"]]

    for entArea in enumerate(entsoeArea):
        if area == entArea[1][0]:
            return entArea[1][1], entArea[1][2]
    return "", ""

def parseArgs(argv):
    """ Get area code given as argument. Only care about the first argument """
    arg = ""
    if len(argv) >= 1:
        arg = argv[0].upper()
    return arg

def getConfig():
    """ Read the program ini file and get the Entsoe api key """
    home = os.path.expanduser("~")
    inifile = home + "/.entsoe.ini"
    config = configparser.ConfigParser()
    config.read(inifile)
    try:
        return config['ENTSOE']['APIKEY']
    except KeyError:
        return ""

def fixPriceInfo(rlist):
    """ Interpolate missing price data using pandas """
    newList = []
    td = timedelta(minutes=60)
    n = 1
    j = 0

    nlist =24
    if len(rlist) > 24:
        nlist = 48

    for i in range(nlist):
        n1 = rlist[j][2]
        if n1 == n:
            newList.append(rlist[j])
            j += 1
        else:
            newItem = []
            newItem.append(newList[-1][0] + td)
            newItem.append(newList[-1][1] + td)
            newItem.append(n)
            newItem.append(np.nan)
            newList.append(newItem)
        n += 1
        if n1 == 24:
            n = 1

    arr = []
    for i in range(len(newList)):
        arr.append(newList[i][3])
    arrpd = pd.Series(arr)
    arrpd = arrpd.interpolate(method="linear")
    for i in range(len(newList)):
        newList[i][3] = float(arrpd.values[i])

    return newList

def main(argv):
    """ Get the api key, arguments used, Entsoe area code
        Get the xml from Entsoe, parse the xmlto get price, get the exchange rate from NB and print the price """

    area = "NO5"

    apikey = getConfig()
    if not apikey:
        logger.error("Not able to find Entsoe api key. Exiting ....")
        sys.exit(1)

    arg = parseArgs(argv)
    if arg:
        area = arg

    areacode, name = getEntsoeArea(area)
    if not areacode:
        logger.error(f"Unknown areacode {area} exiting ....")
        sys.exit(1)

    xmlResponse = getEntsoePrice(areacode, apikey)
    timeprice = parseXML(xmlResponse, xslt)
    logger.info(f"Entsoe api reurned {len(timeprice)} price points")
    if len(timeprice) != 48 or len(timeprice) != 24:
        logger.info(f"Using linear interpolation to calculate missing data")
        timeprice = fixPriceInfo(timeprice)
        logger.info(f"After interpolation {len(timeprice)} price points")

    currency = valutaKursNB()
    prc = float(currency['data']['dataSets'][0]['series']['0:0:0:0']['observations']['0'][0])

    col = len(timeprice)
    print("======== Power price in NOK/kWh for area", area, "-", name, "========")
    for i in range(col):
        timeprice[i][3] = timeprice[i][3]*prc*1.25/1000
        print(timeprice[i][0], " - ", timeprice[i][1], " - ", f"{timeprice[i][2]:2d}", " - ", f"{timeprice[i][3]:7.4f}")

    logger.info("Finishing ...")

if __name__ == "__main__":
    main(sys.argv[1:])
