let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

node.log("")
node.log(dt + " Host - " + hostname)
node.log("Topic - " + msg.topic)

let val = msg.payload.val;
let unit = msg.payload.props.unit

let title = "Power"
if (unit == "kWh") {
    title = "Energy"
}

node.log(title + " usage=" + val.toFixed(2) + unit)

msg = {}
msg.payload = [{
    "val": val,
    "time": dt.getTime() * 1000000
},
{
    "host": hostname,
    "topic": topic
}];

return msg;