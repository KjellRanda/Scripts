let topic = "heater/VVB Gulen";
var os = global.get('os');
var hostname = os.hostname();
var CurrentTemprature;

if (msg.topic == "heater/VVB Gulen/EnergiStored") {
   context.set("EnergyStored", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/EnergyTotal") {
   context.set("EnergyTotal", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/EstimatedPower") {
   context.set("EstimatedPower", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/FillLevel") {
   context.set("FillLevel", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/TargetTemprature") {
   context.set("TargetTemprature", msg.payload);
}

if (msg.topic == "heater/VVB Gulen/CurrentTemprature") {
   CurrentTemprature = msg.payload;
   let dt = new Date();

   msg = {}
   msg.payload = [{
      "EnergyStored": context.get("EnergyStored"),
      "EnergyTotal": context.get("EnergyTotal"),
      "EstimatedPower": context.get("EstimatedPower"),
      "FillLevel": context.get("FillLevel"),
      "TargetTemprature": context.get("TargetTemprature"),
      "CurrentTemprature": CurrentTemprature,
      "time": dt.getTime()*1000000
   },
   {
      "host": hostname,
      "topic": topic
   }];

   node.log("")
   node.log(dt + " Host - " + hostname)
   node.log("Topic - " + topic)
   node.log("EnergyStored = " + msg.payload[0].EnergyStored + "kWh")
   node.log("EnergyTotal = " + msg.payload[0].EnergyTotal + "kWh")
   node.log("EstimatedPower = " + msg.payload[0].EstimatedPower + "W")
   node.log("FillLevel = " + msg.payload[0].FillLevel + "%")
   node.log("TargetTemprature = " + msg.payload[0].TargetTemprature + "\xB0C")
   node.log("CurrentTemprature = " + msg.payload[0].CurrentTemprature + "\xB0C")

   return msg;
} else {
   return null;
}