
import sys
import json
import getopt
import requests

def usage(script):
    print(script, '-f jasonfile .... to load matrikkel coordinates from file')
    print('or')
    print(script, '-k kommunenr -g gardsnummer -b bruksnummer -e EPGS code .... to load from GeoNorge using their api')
    sys.exit(2)

def parseArguments(script, argv):
    kommunenr = 0
    gnr = 0
    bnr = 0
    epgs = 0
    file_name = ""

    if len(argv) == 2:
        try:
            opts, args = getopt.getopt(argv,"f:")
        except getopt.GetoptError as err:
            print(err)
            usage(script)
    elif len(argv) == 8:
        try:
            opts, args = getopt.getopt(argv,"k:g:b:e:")
        except getopt.GetoptError as err:
            print(err)
            usage(script)

    for opt, arg in opts:
        if opt == '-k':
            try:
                kommunenr = int(arg)
            except ValueError:
                usage(script)
        elif opt == '-g':
            try:
                gnr = int(arg)
            except ValueError:
                usage(script)
        elif opt == '-b':
            try:
                bnr = int(arg)
            except ValueError:
                usage(script)
        elif opt == '-e':
            try:
                epgs = int(arg)
            except ValueError:
                usage(script)
        elif opt == '-f':
            file_name = arg

    return(kommunenr, gnr, bnr, epgs, file_name)

def getfromGeoNorge(kommunenr, gnr, bnr, epgs):
    url = "https://ws.geonorge.no/eiendom/v1/geokoding?omrade=true&kommunenummer=" + str(kommunenr) + "&gardsnummer=" + str(gnr) + "&bruksnummer=" + str(bnr) + "&utkoordsys=" + str(epgs)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error getting data from GeoNorge. Reurn code = ", response.status_code)
        sys.exit(3)

def readJsonFile(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    except BaseException:
        print("File", file_name, "does not exsist, is not readable or not a json file")
        sys.exit(4)

def writePolygon(coord):
    print("POLYGON ((", end="", sep="")
    formatPoints(coord, "", "")
    print("))")

def writeLine(coord):
    print("LINESTRING (", end="", sep="")
    formatPoints(coord, "", "")
    print(")")

def writePoints(coord):
    print("MULTIPOINT (", end="", sep="")
    formatPoints(coord, "(", ")")
    print(")")

def formatPoints(coord, c1, c2):
    n = len(coord[0])
    i = 1
    for coo in coord[0]:
        if i < n:
            print(c1, coo[0], " ", coo[1], c2 , ", ", end="", sep="")
        else:
            print(c1, coo[0], " ", coo[1], c2, end="", sep="")
        i = i + 1

def main(script, argv):

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
    ltype = geometry[0]['geometry']
    if ltype['type'] == 'Polygon':
        coord = ltype['coordinates']
        writePolygon(coord)
        writeLine(coord)
        writePoints(coord)
    else:
        print("No Polygon data found")
        sys.exit(7)

if __name__ == "__main__":
    script = sys.argv[0]
    main(script, sys.argv[1:])
