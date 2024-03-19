let power = msg.payload;
let n = power.length - 1;
const date = new Date();
let current = date.getMinutes();
const maxLimit = 4.7;

var usedP = context.get('usedP');
if (typeof usedP == "undefined") {
    usedP = "high";
    context.set('usedP', usedP);
}

let estimate = 0;
if (current > 0) {
    estimate = 60*power[n].integral/current;
}

msg = {};
msg.payload = {
    "price": "",
    "reason": "usage"
}
node.log("");
node.log("Used so far " + power[n].integral.toFixed(2) + " KWh. Estimated houarly usage " + estimate.toFixed(2) + " KWh");

if (current > 14 && estimate > maxLimit) {
    msg.payload.price = "high";
    node.log("High estimated power usage. Lowering setpoints");
    usedP = "high";
    context.set('usedP', usedP);
    return msg;
} else {
    usedP = context.get('usedP');
    if (usedP == "high") {
        usedP = "low";
        context.set('usedP', usedP);
        msg.payload.price = "low";
        node.log("Power usage reset to low");
        return msg;
    }
    return null;
}
return null;