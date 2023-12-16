let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

node.log("")
node.log(dt + " Host - " + hostname)
node.log("Topic - " + msg.topic)

let temp = msg.payload.val;
let unit = msg.payload.props.unit

node.log("Temperature = " + temp + "\xB0" + unit)

msg = {}
msg.payload = [{
    "val_temp": temp,
    "time": dt.getTime() * 1000000
},
{
    "host": hostname,
    "topic": topic
}];

return msg;