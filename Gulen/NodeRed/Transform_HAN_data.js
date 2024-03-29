let dt = new Date(msg.payload.ctime);
let topic = msg.topic;
var os = global.get('os');
var hostname = os.hostname();

node.log("")
node.log(dt + " Host - " + hostname)
node.log("Topic - " + msg.topic)

let vfac = 10
let afac = 1000

if (msg.payload.type == "evt.meter.report") {
    let power = msg.payload.val;
    let unit = msg.payload.props.unit
    
    let title = "Power"
    if (unit == "kWh") {
        title = "Energy"
    }

    node.log(title + " usage=" + power + unit)
    
    msg = {}
    msg.payload = [{
        "val": power,
        "unit": unit,
        "time": dt.getTime()*1000000
    },
    {
        "host": hostname,
        "topic": topic
    }];
} else if (msg.payload.type == "evt.meter_ext.report") {
    let i1 = msg.payload.val.i1/afac;
    let i2 = msg.payload.val.i2/afac;
    let i3 = msg.payload.val.i3/afac;
    let u1 = msg.payload.val.u1/vfac;
    let u2 = msg.payload.val.u2/vfac;
    let u3 = msg.payload.val.u3/vfac;

    let p_export_react = msg.payload.val.p_export_react;
    let p_import_react = msg.payload.val.p_import_react;

    node.log("I1=" + i1 + "A I2=" + i2 + "A I3=" + i3 + "A U1=" + u1 + "V U2=" + u2 + "V U3=" + u3 + "V")
    
    msg = {}
    msg.payload = [{
        "val_i1": i1,
        "val_i2": i2,
        "val_i3": i3,
        "val_u1": u1,
        "val_u2": u2,
        "val_u3": u3,
        "val_p_export_react": p_export_react,
        "val_p_import_react": p_import_react,
        "time": dt.getTime()*1000000
    },
    {
        "host": hostname,
        "topic": topic
    }];
}
return msg;