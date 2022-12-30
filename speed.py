""" Okoola speed test """
import sys
import getopt
import time
from influxdb import InfluxDBClient #pylint: disable=import-error

def db_data(serie, atype, measure, value, atime):
    """ Write data to Influxdb in line format """
    message = [
                {
                    "measurement": serie,
                    "tags" : {
                        "type": atype,
                        "measurement": measure
                            },
                            "time": atime*1000000000,
                            "fields": {
                                    "value": value*1.0
                                    }
                }
            ]
    return message

def main(argv):
    """ Control writing of Okoola speed measurements to Influxdb """
    if len(argv) != 6:
        print ('speed.py -d download -u upload -p ping')
        sys.exit(2)

    down = 0.0
    upl  = 0.0
    ping = 0.0

    try:
        opts, args = getopt.getopt(argv,"d:u:p:") #pylint: disable=unused-variable
    except getopt.GetoptError:
        print ('speed.py -d download -u upload -p ping')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-d':
            try:
                down = float(arg)
            except ValueError:
                sys.exit(-1)
        elif opt == '-u':
            try:
                upl = float(arg)
            except ValueError:
                sys.exit(-1)
        elif opt == '-p':
            try:
                ping = float(arg)
            except ValueError:
                sys.exit(-1)

    timenow =  int(time.mktime(time.localtime()))

    db_host = 'nazgul.net.home'
    db_port = 8086
    db_name = 'speedtest'

    client = InfluxDBClient(host=db_host, port=db_port)
    client.switch_database(db_name)

    message = db_data('speedtest', 'Ookla', 'download', down, timenow)
    client.write_points(message)

    message = db_data('speedtest', 'Ookla', 'upload', upl, timenow)
    client.write_points(message)

    message = db_data('speedtest', 'Ookla', 'ping', ping, timenow)
    client.write_points(message)

if __name__ == "__main__":
    main(sys.argv[1:])
