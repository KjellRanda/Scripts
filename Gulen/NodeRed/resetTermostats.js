msg = {};
msg.payload = {
    "price": "low",
    "reason": "reset"
}

node.log("");
node.log("Midnight termostat reset to default setpoints");

return msg;