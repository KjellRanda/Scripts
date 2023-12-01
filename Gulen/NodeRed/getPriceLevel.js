let text = msg.payload;
let lines = text.split(/\r?\n|\r|\n/g);
let prc = [];
const nVal = 4;

const date = new Date();
let today = date.getFullYear() + '-' + String(date.getMonth()+1).padStart(2,'0') + '-' + String(date.getDate()).padStart(2,'0');
let hour = date.getHours();

let field = "";
let n = 0
for (let i = 0; i < lines.length; i++) {
    field = lines[i].trim().split(/\s+/);
    if (field[0] == today) {
        prc[n] = parseFloat(field[8]);
        n = n + 1;
    }
}
prc.sort(function (a, b) { return b - a });
let limitVal = prc[nVal-1];

let tVal = 0.0;
for (let i = 0; i < lines.length; i++) {
    field = lines[i].trim().split(/\s+/);
    let dt = field[1]?.split(':')
    if (field[0] == today && parseInt(dt[0]) >= parseInt(hour)  ) {
        tVal = parseFloat(field[8]);
        break;
    }
}

let arr = "";
if (prc[0] < 1.0) {
    node.log("");
    node.log("Max power price " + prc[0] + " to low for setpoint modification");
    msg.payload = "free";
    return msg;
}

if (tVal >= limitVal) {
    arr = "Expensive hour: " + field[0] + " " + field[1] + " Price = " + tVal + " Limit = " + limitVal;
    msg.payload = "high";
} else {
    arr = "Cheap hour: " + field[0] + " " + field[1] + " Price = " + tVal + " Limit = " + limitVal;
    msg.payload = "low"
}

node.log("")
node.log(arr)

return msg;