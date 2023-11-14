"""
Program to get properties border coordinates from Geonorge using their api or a json file downloaded Geonorge
Writes the data as WKT data for us in QGIS or other GIS software
"""
import sys
import json
import getopt
import requests

def usage(script):
    """
    How to use the program
    """
    print(script, '-f jasonfile .... to load matrikkel coordinates from file')
    print('or')
    print(script, '-k kommunenr -g gardsnummer -b bruksnummer -e EPGS code .... to load from GeoNorge using their api')
    sys.exit(2)

def parseArguments(name, argv):
    """
    Parse the program arguments. See function usage.
    """
    kommunenr = 0
    gnr = 0
    bnr = 0
    epgs = 0
    file_name = ""

    if len(argv) == 2:
        try:
            opts, arg = getopt.getopt(argv,"f:")
        except getopt.GetoptError as err:
            print(err)
            usage(name)
    if len(argv) == 8:
        try:
            opts, arg = getopt.getopt(argv,"k:g:b:e:")
        except getopt.GetoptError as err:
            print(err)
            usage(name)

    for opt, arg in opts:
        if opt == '-k':
            try:
                kommunenr = int(arg)
            except ValueError:
                usage(name)
        if opt == '-g':
            try:
                gnr = int(arg)
            except ValueError:
                usage(name)
        if opt == '-b':
            try:
                bnr = int(arg)
            except ValueError:
                usage(name)
        if opt == '-e':
            try:
                epgs = int(arg)
            except ValueError:
                usage(name)
        if opt == '-f':
            file_name = arg

    return(kommunenr, gnr, bnr, epgs, file_name)

def getfromGeoNorge(kommunenr, gnr, bnr, epgs):
    """
    Get propery border coordinates from Geonorge using their api
    """
    url = "https://ws.geonorge.no/eiendom/v1/geokoding?omrade=true&kommunenummer=" + str(kommunenr) + "&gardsnummer=" + str(gnr) + "&bruksnummer=" + str(bnr) + "&utkoordsys=" + str(epgs)
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.json()
    print("Error getting data from GeoNorge. Reurn code = ", response.status_code)
    sys.exit(3)

def readJsonFile(file_name):
    """
    Read a json file downloaded from Geonorge
    """
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data
    except (OSError, json.decoder.JSONDecodeError) as err:
        print("File", file_name, "does not exsist, is not readable or not a json file")
        print("Error reported:", err)
        sys.exit(4)

def writePolygon(coord):
    """
    Write WKT datatype POLYGON
    """
    print("POLYGON ((", end="", sep="")
    formatPoints(coord, "", "")
    print("))")

def writeLine(coord):
    """
    Write WKT datatype LINESTRING
    """
    print("LINESTRING (", end="", sep="")
    formatPoints(coord, "", "")
    print(")")

def writePoints(coord):
    """
    Write WKT datatype MULTIPOINT
    """
    print("MULTIPOINT (", end="", sep="")
    formatPoints(coord, "(", ")")
    print(")")

def formatPoints(coord, c1, c2):
    """
    Write the coordinates for the points in the WKT datatypes
    """
    n = len(coord[0])
    i = 1
    for coo in coord[0]:
        if i < n:
            print(c1, coo[0], " ", coo[1], c2 , ", ", end="", sep="")
        else:
            print(c1, coo[0], " ", coo[1], c2, end="", sep="")
        i = i + 1

def main(script, argv):
    """
    Parse arguments. Get data from Geonorge or exsisting downloaded json file
    Try to get the coordinates for up to 100 polygon in th einput data
    Wites the data as WKT
    """

    if len(argv) != 8 and len(argv) != 2:
        usage(script)

    kommunenr, gnr, bnr, epgs, file_name = parseArguments(script, argv)

    if kommunenr > 0 and gnr > 0 and bnr > 0 and epgs > 0:
        data = getfromGeoNorge(kommunenr, gnr, bnr, epgs)
    elif file_name != "" :
        data = readJsonFile(file_name)
    else:
        print("Fatal error in argument parsing. Exiting ....")
        sys.exit(5)

    geometry = data['features']
    n = 0
    while n < 100:
        try:
            ltype = geometry[n]['geometry']
            if ltype['type'] == 'Polygon':
                coord = ltype['coordinates']
                writePolygon(coord)
                writePoints(coord)
                writeLine(coord)
                print()
                n = n + 1
        except IndexError:
            break

    if n == 0:
        print("No Polygon data found")
        sys.exit(7)

if __name__ == "__main__":
    scriptName = sys.argv[0]
    main(scriptName, sys.argv[1:])
