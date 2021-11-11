
import sys, getopt, time
from influxdb import InfluxDBClient

def db_data(serie, type, measure, value, time):
    message = [
                {
                    "measurement": serie,
                    "tags" : {
                        "type": type,
                        "measurement": measure
                            },
                            "time": time*1000000000,
                            "fields": {
                                    "value": value*1.0
                                    }
                }
            ]
    return message

def main(argv):

    if len(argv) != 6:
        print ('speed.py -d download -u upload -p ping')
        sys.exit(2)

    down = 0.0
    up   = 0.0
    ping = 0.0

    try:
        opts, args = getopt.getopt(argv,"d:u:p:")
    except getopt.GetoptError:
       print ('speed.py -d download -u upload -p ping')
       sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-d':
            down = float(arg)
        elif opt == '-u':
            up = float(arg)
        elif opt == '-p':
            ping = float(arg)

    timenow =  int(time.mktime(time.localtime()))

    db_host = 'nazgul.net.home'
    db_port = 8086
    db_name = 'speedtest'

    client = InfluxDBClient(host=db_host, port=db_port)
    client.switch_database(db_name)

    message = db_data('speedtest', 'Ookla', 'download', down, timenow)
    client.write_points(message)

    message = db_data('speedtest', 'Ookla', 'upload', up, timenow)
    client.write_points(message)

    message = db_data('speedtest', 'Ookla', 'ping', ping, timenow)
    client.write_points(message)

if __name__ == "__main__":
   main(sys.argv[1:])

