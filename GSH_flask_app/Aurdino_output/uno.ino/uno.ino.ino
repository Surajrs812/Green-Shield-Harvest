// Define the pin for the IR sensor
const int irSensorPin = 2; // Pin connected to OUT of the IR sensor
int sensorValue = 0; // Variable to hold the sensor reading

void setup() {
  // Start serial communication for debugging
  Serial.begin(9600);
  
  // Set the IR sensor pin as input
  pinMode(irSensorPin, INPUT);
}

void loop() {
  // Read the value from the IR sensor
  sensorValue = digitalRead(irSensorPin);
  
  // Check if the sensor detects an obstacle
  if (sensorValue == HIGH) {
    Serial.println("Obstacle detected!");
  } else {
    Serial.println("Clear path.");
  }
  
  // Wait a bit before the next reading
  delay(500);
}
