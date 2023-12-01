// Entre, Bad
const tp = ["pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:thermostat/ad:6_1",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:thermostat/ad:5_1"];
const tmp = [20.0, 21.0];
const tDiff = 2.0;

var outMsgs = [];
let state = msg.payload;

var temp;
for (let i = 0; i < tp.length; i++) {
    temp = tmp[i]
    if (state == "low") {
        temp = tmp[i];
    }
    else if (state == "high") {
        temp = tmp[i] - tDiff;
    }
    else {
        node.log("");
        node.log("Unknown payload received. Exitong ....");
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

    let arr = "";
    arr = "Power cost " + state + " Setting setpoint to " + temp + "\xB0C";
    node.log("");
    node.log(msg.topic);
    node.log(arr);
}

return [outMsgs];