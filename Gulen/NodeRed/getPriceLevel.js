let text = msg.payload;
let lines = text.split(/\r?\n|\r|\n/g);
let prc = [];
const nVal = 4;
const freePrice = 0.8;

const date = new Date();
let today = date.getFullYear() + '-' + String(date.getMonth()+1).padStart(2,'0') + '-' + String(date.getDate()).padStart(2,'0');
let hour = date.getHours();

var tDay, tHour, field;
let tVal = 0.0;
let tFound = false;
let n = 0;
for (let i = 0; i < lines.length; i++) {
    field = lines[i].trim().split(/\s+/);
    if (field[0] == today) {
        prc[n] = parseFloat(field[8]);
        let dt = field[1]?.split(':');
        if (parseInt(dt[0]) >= parseInt(hour) && !tFound) {
            tVal = prc[n];
            tDay = field[0];
            tHour = field[1];
            tFound = true;
        }
        n = n + 1;
    }
}

if ( n != 24) {
    node.log("");
    node.log("Incompleate price information. Only " + n + " valuse found for " + today + ". Exiting ....");
    return null;
}
if (!tFound) {
    node.log("");
    node.log("Price for current hour " + hour + " not found. Exiting ....");
    return null;
}

prc.sort(function (a, b) { return b - a });
let limitVal = prc[nVal - 1];
let maxPrice = prc[0];

let unit = " NOK/KWh"
if (maxPrice < freePrice) {
    node.log("");
    node.log("Max power price " + maxPrice + unit + " to low for setpoint modification");
    return null;
}

msg = {};
msg.payload = {
    "price": "",
    "reason": "price"
}
node.log("")
if (tVal >= limitVal) {
    node.log("Expensive hour: " + tDay + " " + tHour + " Price = " + tVal + unit + ". Limit = " + limitVal + unit + ". Max price = " + maxPrice + unit + ".");
    msg.payload.price = "high";
} else {
    node.log("Cheap hour: " + tDay + " " + tHour + " Price = " + tVal + unit + ". Limit = " + limitVal + unit + ". Max price = " + maxPrice + unit + ".");
    msg.payload.price = "low"
}

return msg;