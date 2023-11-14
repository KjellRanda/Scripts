
from datetime import date, timedelta, datetime
import sys
import os
import time
import configparser
from io import StringIO, BytesIO
import re
import requests
from lxml import etree as ET

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

def datetime_from_utc_to_local(utc):
    """
    Convert date and time from UTC to local time
    """
    epoch = time.mktime(time.strptime(utc, '%Y-%m-%dT%H:%MZ'))
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return (datetime.strptime(utc, '%Y-%m-%dT%H:%MZ') + offset).strftime('%Y-%m-%d %H:%M')

def getEntsoePrice(area, apikey):
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
    print("Error getting data from Entsso-E. Reurn code = ", response.status_code)
    sys.exit(3)

def parseXML(xml, lxslt):
    rlist = []
    tree = ET.parse(BytesIO(xml))
    transform=ET.XSLT(ET.parse(StringIO(lxslt)))
    tree = transform(tree)
    root = tree.getroot()
    for i in root.findall('./TimeSeries/Period'):
        res = i.find('resolution')
        tstart = i.find('timeInterval/start')
        t1 = datetime.strptime(datetime_from_utc_to_local(tstart.text),'%Y-%m-%d %H:%M')
        for j in i.findall('Point'):
            period = j.find('position')
            price = j.find('price.amount')
            t2 = t1 + timedelta(minutes=int(re.findall(r'\d+', res.text)[0]))
            a = []
            a.append(t1)
            a.append(t2)
            a.append(int(period.text))
            a.append(float(price.text))
            rlist.append(a)
            t1 = t2
    return rlist

def valutaKursNB():
    url = "https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=1&locale=no"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()
    print("Error getting data from Norges Bank code = ", response.status_code)
    sys.exit(3)

def getEntsoeArea(area):
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
    arg = ""
    if len(argv) >= 1:
        arg = argv[0].upper()
    return arg

def getConfig():
    home = os.path.expanduser("~")
    inifile = home + "/.entsoe.ini"
    config = configparser.ConfigParser()
    config.read(inifile)
    try:
        return config['ENTSOE']['APIKEY']
    except KeyError:
        return ""

def main(argv):
    area = "NO5"

    apikey = getConfig()
    if not apikey:
        print("Not able to find Entsoe api key. Exiting ....")
        sys.exit(1)

    arg = parseArgs(argv)
    if arg:
        area = arg

    areacode, name = getEntsoeArea(area)
    if not areacode:
        print("Unknown areacode", area, "exiting ....")
        sys.exit(1)

    xmlResponse = getEntsoePrice(areacode, apikey)
    timeprice = parseXML(xmlResponse, xslt)
    currency = valutaKursNB()
    prc = float(currency['data']['dataSets'][0]['series']['0:0:0:0']['observations']['0'][0])

    col = len(timeprice)
    print("======== Power price in NOK/kWh for area", area, "-", name, "========")
    for i in range(col):
        timeprice[i][3] = timeprice[i][3]*prc*1.25/1000
        print(timeprice[i][0], " - ", timeprice[i][1], " - ", f"{timeprice[i][2]:2d}", " - ", f"{timeprice[i][3]:7.4f}")

if __name__ == "__main__":
    main(sys.argv[1:])
