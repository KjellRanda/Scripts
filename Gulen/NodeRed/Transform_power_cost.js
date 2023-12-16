let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

node.log("")
node.log(dt + " Host - " + hostname)
node.log("Topic - " + msg.topic)

if (msg.payload.type != "evt.energy_price.report") {
    node.log("Unsupported payload type " + msg.payload.type + " ... returning")
    return null;
}

var perc = context.get('perc');
if (typeof perc == "undefined") {
    perc = 0;
    context.set('perc', perc);
}

var avr = context.get('avr');
if (typeof avr == "undefined") {
    avr = 0;
    context.set('avr', avr);
}

let price = msg.payload.val.price;
let scale = msg.payload.val.scale;
let percentile = msg.payload.val.percentile;
let average = msg.payload.val.average;

if (typeof percentile == "undefined") {
    percentile = context.get('perc');
    node.log("Replacing undefiened percentile with " + percentile)
} else {
    context.set('perc', percentile);
}

if (typeof average == "undefined") {
    average = context.get('avr');
    node.log("Replacing undefiened average with " + average)
} else {
    context.set('avr', average);
}

node.log("Price=" + price + " Scale=" + scale + " Percentile=" + percentile + " Average=" + average)

msg = {}
msg.payload = [{
    "val_price": price,
    "val_scale": scale,
    "val_percentile": percentile,
    "val_average": average,
    "time": dt.getTime() * 1000000
},
{
    "host": hostname,
    "topic": topic
}];

return msg;