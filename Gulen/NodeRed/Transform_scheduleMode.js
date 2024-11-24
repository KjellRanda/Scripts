let topic = "heater/VVB/scheduleMode";
var os = global.get('os');
var hostname = os.hostname();

let scheduleMode = msg.payload;
let dt = new Date();

msg = {}
msg.payload = [{
   "scheduleMode": scheduleMode,
   "time": dt.getTime()*1000000
},
{
   "host": hostname,
   "topic": topic
}];

node.log("")
node.log(dt + " Host - " + hostname)
node.log("Topic - " + topic)
node.log("scheduleMode = " + scheduleMode)

return msg;