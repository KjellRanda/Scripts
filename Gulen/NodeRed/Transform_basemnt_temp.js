let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

node.log("")
node.log(dt + " Host - " + hostname)
node.log("Topic - " + msg.topic)

let val = msg.payload.val;

node.log("Basement temperature=" + val.toFixed(2) + "\xB0C")

msg = {}
msg.payload = [{
    "bsmnt_temp": val,
    "time": dt.getTime() * 1000000
},
{
    "host": hostname,
    "topic": topic
}];

return msg;