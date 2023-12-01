let stat = false;
if (msg.payload.type == "evt.binary.report") {
    stat = msg.payload.val;
}
msg.payload = stat;

node.log("")
node.log("In Gulen - " + msg.payload)

return msg;