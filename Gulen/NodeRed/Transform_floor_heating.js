let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

node.log("")
node.log(dt + " Host - " + hostname)
node.log("Topic - " + msg.topic)

let p_val = msg.payload.val.p_import;
let e_val = msg.payload.val.e_import;

node.log("Power and energy usage = " + p_val.toFixed(2) + "W " + e_val.toFixed(2) + "kWh")

msg = {}
msg.payload = [{
    "val_e_import": e_val,
    "val_p_import": p_val,
    "time": dt.getTime() * 1000000
},
{
    "host": hostname,
    "topic": topic
}];

return msg;