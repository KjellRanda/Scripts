import sys
import requests
from MyUplinkConst import PUB_API, INT_API, PUB_BASEURL, INT_BASEURL 

class myuplinkapi:

    def __init__(self) -> None:
        self.apiver  = PUB_API
        self.baseurl = PUB_BASEURL
        self.usrname = None
        self.passwd  = None
        self.token = None
        self.lifetime = None
        self.devid = None
        self.devname = None
        self.logger = None
        self.DEBUG = "DEBUG"
        self.INFO  = "INFO"
        self.ERROR = "ERROR"

    def getDevName(self):
        return self.devname
    
    def setLogger(self, logger):
        self.logger = logger
    
    def setIntAPI(self) -> None:
        self.apiver  = INT_API
        self.baseurl = INT_BASEURL
        
    def apiUserPasswd(self, USERNAME, PASSWORD) -> None:
        self.usrname = USERNAME
        self.passwd  = PASSWORD

    def authorize(self):
        message = f"Using MyUplink API {self.baseurl}"
        self._output_(self.INFO, message)
        url = self.baseurl + "/oauth/token"
        self.payload = {
            "client_id": "My-Uplink-Web",
            "grant_type": "password",
            "username": self.usrname,
            "password": self.passwd
        }
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, headers=self.headers, data=self.payload, timeout=60)
        if response.status_code == 200:
            tResponse = response.json()
            self.lifetime = tResponse["expires_in"]
            self.token = tResponse["access_token"]
            message = f"Got token with lifetime {self.lifetime}s"
            self._output_(self.INFO, message)
            return self.lifetime
        message = f"Failed to get a token: {response.status_code}"
        self._output_(self.ERROR, message)
        sys.exit(1)

    def getDevID(self):
        if self.apiver == PUB_API:
            url = self.baseurl + "/v2/systems/me"
        else:
            url = self.baseurl + "/v2/groups/me"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self.token
        }
        response = requests.get(url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            sysList = response.json()
            if self.apiver == PUB_API:
                ndev = sysList["numItems"]
                for i in range(ndev):
                    system = sysList["systems"][i]
                    dev = system["devices"]
                    if system["securityLevel"] == "admin":
                        self.devid = dev[0]["id"]
                        self.devname = system["name"]
            else:
                for item in sysList["groups"]:
                    if item["role"] == "admin":
                        self.devid = item["devices"][0]["id"]
                        self.devname = item["name"]
            message = f"Found device with role admin {self.devid} with name {self.devname}"
            self._output_(self.INFO, message)
            return self.devid
        message = f"Failed to get devices: {response.status_code}"
        self._output_(self.ERROR, message)
        sys.exit(2)

    def getdevData(self, params):
        retData = []
        url = self.baseurl + "/v2/devices/" + self.devid + "/points?parameters=" + params
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self.token
        }
        response = requests.get(url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            dlist = response.json()
            for item in dlist:
                if item["parameterId"] == '406':
                    unit = item["strVal"]
                else:
                    unit = item["parameterUnit"]
                retData.append([item["parameterId"], item["parameterName"], item["value"], unit])
                message = f'{item["parameterId"]} {item["parameterName"]} {item["value"]} {unit}'
                self._output_(self.DEBUG, message)
            return retData
        message = f"Failed to get device data: {response.status_code}"
        self._output_(self.ERROR, message)
        sys.exit(3)

    def updateSchedule(self, json_data):
        url = self.baseurl + "/v2/devices/" + self.devid + "/weekly-schedules"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = requests.put(url, headers=self.headers, data=json_data, timeout=60)
        if response.status_code == 200 or response.status_code == 204:
            message = f"Schedule sucessfully updated: {response.status_code}"
            self._output_(self.INFO, message)
            return
        message = f"Failed to update schedule: {response.status_code}"
        self._output_(self.ERROR, message)
        sys.exit(4)

    def getSchedule(self):
        url = self.baseurl + "/v2/devices/" + self.devid + "/weekly-schedules"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = requests.get(url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            return response.json()
        message = f"Failed to get schedule: {response.status_code}"
        self._output_(self.ERROR, message)
        sys.exit(5)

    def getScheduleMode(self):
        url = self.baseurl + "/v2/devices/" + self.devid + "/schedule-modes"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = requests.get(url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            return response.json()
        message = f"Failed to get schedule modes: {response.status_code}"
        self._output_(self.ERROR, message)
        sys.exit(6)

    def _output_(self, severity, mess):
        mylogger = self.logger
        if mylogger:
            if severity == self.INFO:
                mylogger.info(mess)
            elif severity == self.DEBUG:
                mylogger.debug(mess)
            elif severity == self.ERROR:
                mylogger.error(mess)
        else:
            print(f"{severity}: {mess}")