let topic = "heater/VVB Gulen";
var os = global.get('os');
var hostname = os.hostname();
var Temperature;

if (msg.topic == "heater/VVB Gulen/StoredEnergy") {
   context.set("StoredEnergy", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/TotalEnergyUsed") {
   context.set("TotalEnergyUsed", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/EstimatedPower") {
   context.set("EstimatedPower", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/FillLevel") {
   context.set("FillLevel", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/Setpoint") {
   context.set("Setpoint", msg.payload);
}
if (msg.topic == "heater/VVB Gulen/CurrentProgram") {
   context.set("CurrentProgram", msg.payload);
}

if (msg.topic == "heater/VVB Gulen/Temperature") {
   Temperature = msg.payload;
   let dt = new Date();

   msg = {}
   msg.payload = [{
      "CurrentProgram": context.get("CurrentProgram"),
      "EnergyStored": context.get("StoredEnergy"),
      "EnergyTotal": context.get("TotalEnergyUsed"),
      "EstimatedPower": context.get("EstimatedPower"),
      "FillLevel": context.get("FillLevel"),
      "TargetTemprature": context.get("Setpoint"),
      "CurrentTemprature": Temperature,
      "time": dt.getTime()*1000000
   },
   {
      "host": hostname,
      "topic": topic
   }];

   node.log("")
   node.log(dt + " Host - " + hostname)
   node.log("Topic - " + topic)
   node.log("CurrentProgram = " + msg.payload[0].CurrentProgram)
   node.log("StoredEnergy = " + msg.payload[0].EnergyStored + "kWh")
   node.log("TotalEnergyUsed = " + msg.payload[0].EnergyTotal + "kWh")
   node.log("EstimatedPower = " + msg.payload[0].EstimatedPower + "W")
   node.log("FillLevel = " + msg.payload[0].FillLevel + "%")
   node.log("Setpoint = " + msg.payload[0].TargetTemprature + "\xB0C")
   node.log("Temprature = " + msg.payload[0].CurrentTemprature + "\xB0C")

   return msg;
} else {
   return null;
}