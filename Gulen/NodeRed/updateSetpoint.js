const room = ["Entrance", "Bathroom"];
const tp = ["pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:thermostat/ad:6_1",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:thermostat/ad:5_1"];
const tmp = [20.0, 21.0];
const tDiff = 2.0;

var outMsgs = [];
let state = msg.payload.price;
let reason = msg.payload.reason;

var temp;
for (let i = 0; i < room.length; i++) {
    if (state == "low") {
        temp = tmp[i];
    }
    else if (state == "high") {
        temp = tmp[i] - tDiff;
        if (reason == "usage") {
            temp = 10.0;
        }
    }
    else {
        node.log("");
        node.log("Unknown payload received. Exiting ....");
        node.log(state);
        return null;
    }

    msg = {};
    msg.topic = tp[i]
    msg.payload = {
        "serv": "thermostat",
        "type": "cmd.setpoint.set",
        "val_t": "str_map",
        "val": {
            "temp": String(temp),
            "type": "heat",
            "unit": "C"
        },
        "props": null,
        "tags": null,
        "src": "node-red",
        "ver": "1",
        "uid": crypto.randomUUID()
    }
    outMsgs.push(msg)

    if (i == 0) {node.log("");}
    switch (reason) {
        case "price":
            node.log("Power cost " + state + ". Setting setpoint to " + temp + "\xB0C" + " in " + room[i]);
            break;
        case "usage":
            node.log("Power usage " + state + ". Setting setpoint to " + temp + "\xB0C" + " in " + room[i]);
            break;
        case "reset":
            node.log("Daily reset to default. Setting setpoint to " + temp + "\xB0C" + " in " + room[i]);
            break;
        default:
            node.log("Unknown setpoint change reason: " + reason +" Exiting ...");
            return null;
    }
}

return [outMsgs];