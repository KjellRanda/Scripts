let pay = msg.payload[1];
let n = pay.length - 1;
let humid = pay[n].last;
let loc = msg.payload[0];

var HIGH, LOW

if (loc == "true") {
   HIGH = 65
   LOW = 60
} else {
    HIGH = 67
    LOW = 62
}
node.log("")
node.log("In Gulen="+ loc + " Basement humidity=" + humid + " Low limit=" + LOW + " High limit=" + HIGH);

let msg1 = {};
let msg2 = {};
msg1.payload = {"operation":"GET","schema":true};
if (humid > HIGH ) {
    node.log("Humidity in basement high. Turning dehumidifier on.")
    msg2.payload = {"operation": "SET", "dps": 1, "set": true};
}
else if (humid < LOW) {
    node.log("Humidity in basement low. Turning dehumidifier off.")
    msg2.payload = {"operation": "SET", "dps": 1, "set": false};
} else {
    node.log("Humidity in basement within limits.")
    return msg1;
}
return [msg1,msg2];