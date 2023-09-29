let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

let arr = dt + " Host - " + hostname
node.log("")
node.log(arr)
node.log("Topic - " + msg.topic)

let power = msg.payload.val;
let unit = msg.payload.props.unit

let title = "Power"
if (unit == "kWh") {
    title = "Energy"
}

arr = title + " usage=" + power + unit

node.log(arr)

let offset = 0
if (unit == "kWh") {
    offset = 1000000000
}

msg = {}

msg.payload = [{
    "val_hpower": power,
    "val_hunit": unit,
    "time": dt.getTime() * 1000000 + offset
},
{
    "host": hostname,
    "topic": topic
}];

return msg;
