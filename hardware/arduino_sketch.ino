/*
  CLASSMATE Arduino Uno Physical Output Prototype Controller
  -----------------------------------------------------------
  Receives Serial Protocol Commands from CLASSMATE Python Engine:
  - DIRECT_ADDRESS  -> LCD: "YOU WERE ADDRESSED"  | LED: Double Blink Pattern
  - QUESTION        -> LCD: "QUESTION ASKED"     | LED: Short Pulse
  - ANNOUNCEMENT    -> LCD: "ANNOUNCEMENT"       | LED: Short Pulse
  - BELL            -> LCD: "CLASS BELL"         | LED: Pulse Pattern
  - EMERGENCY       -> LCD: "EMERGENCY"          | LED: Rapid Strobe Blink
  - NORMAL          -> LCD: "CLASSMATE ACTIVE"   | LED: OFF

  Hardware Wiring:
  - LCD 16x2 Pins: RS=12, EN=11, D4=5, D5=4, D6=3, D7=2
  - LED Pin: 13 (Built-in or external with resistor on Pin 13)
*/

#include <LiquidCrystal.h>

// Initialize LCD pins
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

const int ledPin = 13;
String inputString = "";
boolean stringComplete = false;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("  CLASSMATE AI  ");
  lcd.setCursor(0, 1);
  lcd.print("System Active...");
  delay(1500);
  lcd.clear();
  lcd.print("Status: Ready");
}

void loop() {
  // Read serial input
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else if (inChar != '\r') {
      inputString += inChar;
    }
  }

  if (stringComplete) {
    inputString.trim();
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void processCommand(String cmd) {
  lcd.clear();
  
  if (cmd == "DIRECT_ADDRESS") {
    lcd.print("YOU WERE");
    lcd.setCursor(0, 1);
    lcd.print("ADDRESSED!");
    // Double Blink
    digitalWrite(ledPin, HIGH); delay(200);
    digitalWrite(ledPin, LOW);  delay(150);
    digitalWrite(ledPin, HIGH); delay(200);
    digitalWrite(ledPin, LOW);
  } 
  else if (cmd == "QUESTION") {
    lcd.print("QUESTION ASKED");
    lcd.setCursor(0, 1);
    lcd.print("Check Dashboard");
    digitalWrite(ledPin, HIGH); delay(300);
    digitalWrite(ledPin, LOW);
  } 
  else if (cmd == "ANNOUNCEMENT") {
    lcd.print("ANNOUNCEMENT");
    lcd.setCursor(0, 1);
    lcd.print("Check Dashboard");
    digitalWrite(ledPin, HIGH); delay(300);
    digitalWrite(ledPin, LOW);
  } 
  else if (cmd == "BELL") {
    lcd.print("CLASS BELL");
    lcd.setCursor(0, 1);
    lcd.print("Period Ended");
    digitalWrite(ledPin, HIGH); delay(500);
    digitalWrite(ledPin, LOW);
  } 
  else if (cmd == "EMERGENCY") {
    lcd.print("!! EMERGENCY !!");
    lcd.setCursor(0, 1);
    lcd.print("EVACUATE / ALERT");
    // Rapid Strobe
    for(int i = 0; i < 8; i++) {
      digitalWrite(ledPin, HIGH); delay(100);
      digitalWrite(ledPin, LOW);  delay(100);
    }
  } 
  else { // NORMAL
    lcd.print("Status: Active");
    lcd.setCursor(0, 1);
    lcd.print("Listening...");
    digitalWrite(ledPin, LOW);
  }
}
