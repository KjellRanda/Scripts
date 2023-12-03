let text = msg.payload;
let lines = text.split(/\r?\n|\r|\n/g);
let prc = [];
const nVal = 4;
const freePrice = 0.8;

const date = new Date();
let today = date.getFullYear() + '-' + String(date.getMonth()+1).padStart(2,'0') + '-' + String(date.getDate()).padStart(2,'0');
let hour = date.getHours();

var tDay, tHour, field, arr;
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
prc.sort(function (a, b) { return b - a });
let limitVal = prc[nVal - 1];

if (prc[0] < freePrice) {
    node.log("");
    node.log("Max power price " + prc[0] + " to low for setpoint modification");
    return null;
}

if (tVal >= limitVal) {
    arr = "Expensive hour: " + tDay + " " + tHour + " Price = " + tVal + " Limit = " + limitVal;
    msg.payload = "high";
} else {
    arr = "Cheap hour: " + tDay + " " + tHour + " Price = " + tVal + " Limit = " + limitVal;
    msg.payload = "low"
}

node.log("")
node.log(arr)

return msg;