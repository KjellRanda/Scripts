let power = msg.payload;
let n = power.length - 1;
const date = new Date();
let current = date.getMinutes();

let estimate = 0;
if (current > 0) {
    estimate = 60*power[n].integral/current;
}

msg = {};
msg.payload = power[n].integral;
node.log("");
node.log("Used so far " + msg.payload.toFixed(2) + " KWh. Estimated houarly usage " + estimate.toFixed(2) + " KWh");
return msg;