int sensor1_pin = A0;  // Sensor 1 on A0
int sensor2_pin = A1;  // Sensor 2 on A1
int relay1_pin = 7;    // Relay channel 1 on pin 7
int relay2_pin = 8;    // Relay channel 2 on pin 8

void setup() {
  Serial.begin(9600);   // Start serial communication at baud rate 9600
  pinMode(sensor1_pin, INPUT);
  pinMode(sensor2_pin, INPUT);
  pinMode(relay1_pin, OUTPUT);
  pinMode(relay2_pin, OUTPUT);

  // Turn relays off initially
  digitalWrite(relay1_pin, LOW); 
  digitalWrite(relay2_pin, LOW);
}

void loop() {
  int sensor1_data = analogRead(sensor1_pin);
  int sensor2_data = analogRead(sensor2_pin);

  // Create variables to hold the status for each sensor
  String sensor1_status;
  String sensor2_status;

  // Check for Sensor 1 Moisture Levels
  if (sensor1_data > 700) {
    sensor1_status = "No Moisture";
    digitalWrite(relay1_pin, HIGH);  // Turn on relay 1
  } else if (sensor1_data > 400) {
    sensor1_status = "Some Moisture";
  } else {
    sensor1_status = "Wet";
    digitalWrite(relay1_pin, LOW);  // Turn off relay 1
  }

  // Check for Sensor 2 Moisture Levels
  if (sensor2_data > 700) {
    sensor2_status = "No Moisture";
    digitalWrite(relay2_pin, HIGH);  // Turn on relay 2
  } else if (sensor2_data > 400) {
    sensor2_status = "Some Moisture";
  } else {
    sensor2_status = "Wet";
    digitalWrite(relay2_pin, LOW);  // Turn off relay 2
  }

  // Send data in a structured format that can be easily parsed by Python
  Serial.print("SENSOR1_STATUS:");
  Serial.println(sensor1_status);

  Serial.print("SENSOR1_VALUE:");
  Serial.println(sensor1_data);

  Serial.print("SENSOR2_STATUS:");
  Serial.println(sensor2_status);

  Serial.print("SENSOR2_VALUE:");
  Serial.println(sensor2_data);

  delay(1000);  // Delay to slow down readings
}
