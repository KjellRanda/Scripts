let retmsg = {};
retmsg.payload = {};

let dps = msg.payload.data.dps;

if (dps[4] === "low") {
    retmsg.payload.speed = 1;
} else if (dps[4] === "mid") {
    retmsg.payload.speed = 2;
} else if (dps[4] === "high") {
    retmsg.payload.speed = 3;
}

if (dps[1] === true) {
    retmsg.payload.power = "Powered on";
} else {
    retmsg.payload.power = "Powered off";
    retmsg.payload.speed = 0;
}

node.log("")
node.log("Dehumidifier status=" + retmsg.payload.power + ". Speed=" + dps[4]);

return retmsg;