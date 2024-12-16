#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi credentials
const char* ssid = "M-TECH";          // Your Wi-Fi SSID
const char* password = "123456789";  // Your Wi-Fi password

// MQTT Broker details
const char* mqtt_server = "164.90.230.152";
const int mqtt_port = 1883;

// Unique device topic
const char* device_id = "mydevicecontrol";            // Unique ID for this ESP8266
char mqtt_topic[50];                          // To store topic dynamically
const int doorone = 15;
const int doortwo = 12;
const int doorthree = 13;
const int doorfour = 14;
const int doorfive = 2;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  pinMode(doorone, OUTPUT);
  pinMode(doortwo, OUTPUT);
  pinMode(doorthree, OUTPUT);
  pinMode(doorfour, OUTPUT);
  pinMode(doorfive, OUTPUT);
  

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // Configure MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqtt_callback);

  // Generate the unique topic
  sprintf(mqtt_topic, "home/esp8266/%s/control", device_id);

  // Connect to MQTT broker
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect(device_id)) {
      Serial.println("Connected to MQTT Broker");
      client.subscribe(mqtt_topic);
      Serial.println(mqtt_topic);
    } else {
      Serial.print("Failed to connect, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }


  // Read saved state from EEPROM doorone
  int savedStatedoorone = EEPROM.read(0);
  if (savedStatedoorone == 1) {
    digitalWrite(doorone, HIGH);
    Serial.println("Pin set to HIGH from EEPROM.");
  } else {
    digitalWrite(doorone, LOW);
    Serial.println("Pin set to LOW from EEPROM.");
  }

  // Read saved state from EEPROM doortwo
  int savedStatedoortwo = EEPROM.read(0);
  if (savedStatedoortwo == 1) {
    digitalWrite(doortwo, HIGH);
    Serial.println("Pin set to HIGH from EEPROM.");
  } else {
    digitalWrite(doortwo, LOW);
    Serial.println("Pin set to LOW from EEPROM.");
  }

  // Read saved state from EEPROM doorthree
  int savedStatedoorthree = EEPROM.read(0);
  if (savedStatedoorthree == 1) {
    digitalWrite(doorthree, HIGH);
    Serial.println("Pin set to HIGH from EEPROM.");
  } else {
    digitalWrite(doorthree, LOW);
    Serial.println("Pin set to LOW from EEPROM.");
  }

  // Read saved state from EEPROM doorfour
  int savedStatedoorfour = EEPROM.read(0);
  if (savedStatedoorfour == 1) {
    digitalWrite(doorfour, HIGH);
    Serial.println("Pin set to HIGH from EEPROM.");
  } else {
    digitalWrite(doorfour, LOW);
    Serial.println("Pin set to LOW from EEPROM.");
  }

  // Read saved state from EEPROM doorfive
  int savedStatedoorfive = EEPROM.read(0);
  if (savedStatedoorfive == 1) {
    digitalWrite(doorfive, HIGH);
    Serial.println("Pin set to HIGH from EEPROM.");
  } else {
    digitalWrite(doorfive, LOW);
    Serial.println("Pin set to LOW from EEPROM.");
  }
  
}

void loop() {
  client.loop();
}

// Callback function for MQTT messages
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0'; // Null-terminate payload
  String message = String((char*)payload);

  if (message == "highdoorone") {
    digitalWrite(doorone, HIGH);
    EEPROM.write(0, 1); // Save HIGH state to EEPROM
    EEPROM.commit();
    Serial.println("doorone turned ON");
  } else if (message == "lowdoorone") {
    digitalWrite(doorone, LOW);
    EEPROM.write(0, 0); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doorone turned OFF");
  }
  else if (message == "highdoortwo") {
    digitalWrite(doortwo, HIGH);
    EEPROM.write(0, 1); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doortwo turned on");
  }
  else if (message == "lowdoortwo") {
    digitalWrite(doortwo, LOW);
    EEPROM.write(0, 0); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doortwo turned OFF");
  }
  else if (message == "highdoorthree") {
    digitalWrite(doorthree, HIGH);
    EEPROM.write(0, 1); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doorthree turned on");
  }
  else if (message == "lowdoorthree") {
    digitalWrite(doorthree, LOW);
    EEPROM.write(0, 0); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doorthree turned OFF");
  }
  else if (message == "highdoorfour") {
    digitalWrite(doorfour, HIGH);
    EEPROM.write(0, 1); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doorfour turned on");
  }
  else if (message == "lowdoorfour") {
    digitalWrite(doorfour, LOW);
    EEPROM.write(0, 0); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doorfour turned OFF");
  }
  else if (message == "highdoorfive") {
    digitalWrite(doorfive, HIGH);
    EEPROM.write(0, 1); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doorfive turned on");
  }
  else if (message == "lowdoorfive") {
    digitalWrite(doorfive, LOW);
    EEPROM.write(0, 0); // Save HIGH state to 
    EEPROM.commit();
    Serial.println("doorfive turned OFF");
  }
}
