#include <Wire.h>
#include "replay.h"

const int lcd_addr = 0x27;

/*
 * Wiring:
 * LCD SCREEN (I2C 0x27) ----- ARDUINO (MICRO)
 *                   GND ----- GND
 *                   VCC ----- 5V
 *                   SDA ----- SDA (2)
 *                   SCL ----- SDA (3)
 */

void setup() {
  // Set up debugging serial channel
  Serial.begin(9600);
  // Set up I2C communication
  Wire.begin();
}

void loop() {
  delay(3000);
  Serial.println("Begin");
  delay(3000);
  for (int i = 0; i < msg_len; i++) {
    // Get data from PROGMEM because the tiny microcontroller doesn't have enough space in RAM
    uint8_t msg = pgm_read_byte_near(msgs + i);
    uint16_t delay_u = pgm_read_word_near(delay_us + i);
    uint16_t delay_m = pgm_read_word_near(delay_ms + i);
    
    // Log the current packet sent
    Serial.print("Packet #");
    Serial.print(i);
    Serial.print(": ");
    Serial.print((int) msg);

    // Send one packet over the I2C bus
    Wire.beginTransmission(lcd_addr);
    Wire.write(msg);
    Wire.endTransmission();

    // Delay microseconds
    Serial.print(" delay ");
    Serial.print(delay_u);
    Serial.print("us ");
    delayMicroseconds(delay_u);

    // Delay miliseconds
    if (delay_m) {
      Serial.print(delay_m);
      Serial.print("ms ");
      delay(delay_m);
    } 
    
    Serial.println();
  }
}
