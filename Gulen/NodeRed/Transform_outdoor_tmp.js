let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

let arr = dt + " Host - " + hostname
node.log("")
node.log(arr)
node.log("Topic - " + msg.topic)

let val = msg.payload.val;

arr = "Outdoor temperature=" + val.toFixed(2) + "\xB0C"
node.log(arr)

msg = {}

msg.payload = [{
    "out_temp": val,
    "time": dt.getTime() * 1000000
},
{
    "host": hostname,
    "topic": topic
}];

return msg;
