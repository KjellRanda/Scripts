const light = ["Spot1", "Spot2", "Leselampe", "Taklampe", "Golvlampe",
               "Lampetter", "Gang", "Soverom nede", "Loft1", "Loft2"];
const tp = ["pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:15_1",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:16_1",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:10_11",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:11_11",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:2_1",
            "pt:j1/mt:cmd/rt:dev/rn:zw/ad:1/sv:out_lvl_switch/ad:12_0",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:12_11",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:3_1",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:13_11",
            "pt:j1/mt:cmd/rt:dev/rn:zigbee/ad:1/sv:out_lvl_switch/ad:14_11"];
const index = [0,6,7,8,10]

var outMsgs = [];
var value;

if (msg.payload.val == "on") {
    value = true;
} else if (msg.payload.val == "off") {
    value = false;
} else {
    return null;
}
let n = parseInt(msg.topic.slice(-1)) -1;
for (let i = index[n]; i < index[n+1]; i++ ) {
    var tmpMsg = {};
    tmpMsg.topic = tp[i]
    tmpMsg.payload = {
        "serv": "out_bin_switch",
        "type": "cmd.binary.set",
        "val_t": "bool",
        "val": value,
        "props": null,
        "tags": null,
        "src": "node-red",
        "ver": "1",
        "uid": crypto.randomUUID(),
        "topic": tp[i]
    }
    outMsgs.push(tmpMsg)
}
return [outMsgs];