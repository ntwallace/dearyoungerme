#include <FastLED.h>

#define NUM_LEDS_MAILBOX 34
#define NUM_LEDS_KIDS 20

#define DATA_PIN_MAILBOX 3
#define DATA_PIN_KIDS 4

#define KIDS_BRIGHTNESS 64
#define MAILBOX_BRIGHTNESS 192

bool messageLights = false;
unsigned long startMillis;
unsigned long currentMillis;
unsigned long interval;

// define LED arrays
CRGB mailboxLeds[NUM_LEDS_MAILBOX];
CRGB kidsLeds[NUM_LEDS_KIDS];

void setup() {
  Serial.begin(9600);
  while (!Serial) {
  }

  // setup LED matrices for lights
  FastLED.addLeds<WS2812B, DATA_PIN_MAILBOX, GRB>(mailboxLeds, NUM_LEDS_MAILBOX);
  FastLED.addLeds<WS2812B, DATA_PIN_KIDS, GRB>(kidsLeds, NUM_LEDS_KIDS);
  FastLED.setBrightness(MAILBOX_BRIGHTNESS);
  //FastLED.setBrightness(KIDS_BRIGHTNESS);
}

void normalLights() {
  // turn backlight for kids on, mailbox breathe
  fill_solid(kidsLeds, NUM_LEDS_KIDS, CRGB::White);
  mailboxGlow();
}

// oscilatng white glow for mailbox
void mailboxGlow() {
  int pos = beatsin16(10, 96, 192); // generate sinwave (bpm, min, max)
  fill_solid(mailboxLeds, NUM_LEDS_MAILBOX, CHSV(0, 255, pos)); // CHSV (hue, saturation, value);
  FastLED.show();
}

// mailboxs & kids glow brightly when message comes in
int messageReceived(int len) {
  FastLED.setBrightness(255);
  FastLED.show();

  Serial.println(len);

  // Length of lights on based on num lines in message, where:
  // 1 line = 10 sec on, each additional line += 6 sec
  int lengthOn = 10 + ((len - 1) * 6);

  startMillis = millis();
  return lengthOn;
}

void loop() {
  byte inByte = Serial.read();
  
  if (inByte != 255) {      // received an SMS
    messageLights = true;
    int intVal = int(inByte) - 48;  // subtract byte val from ascii table val to get int
    Serial.println(intVal);
    interval = (messageReceived(intVal) * 1000);    // interval period in ms
  }


  if (messageLights) {
    currentMillis = millis();

    if (currentMillis - startMillis >= interval) {
      FastLED.setBrightness(MAILBOX_BRIGHTNESS);
      //FastLED.setBrightness(KIDS_BRIGHTNESS);

      startMillis = currentMillis;
      messageLights = false;
    }
  } else {  // normal lights = mailbox breathing, kids on low
    normalLights();
  }
}
