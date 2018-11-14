#include <FastLED.h>

#define NUM_LEDS_MAILBOX 58
#define NUM_LEDS_GIRL 65
#define NUM_LEDS_BOY 65

#define DATA_PIN_MAILBOX 3
#define DATA_PIN_GIRL 4
#define DATA_PIN_BOY 5

int kidsBrightness = 196;

bool messageLights = false;
unsigned long startMillis;
unsigned long currentMillis;
unsigned long interval;

// define LED arrays
CRGB mailboxLeds[NUM_LEDS_MAILBOX];
CRGB girlLeds[NUM_LEDS_GIRL];
CRGB boyLeds[NUM_LEDS_BOY];

void setup() {
  Serial.begin(115200);
  while (!Serial) {
  }

  // setup LED matrices for lights
  FastLED.addLeds<WS2812B, DATA_PIN_MAILBOX, GRB>(mailboxLeds, NUM_LEDS_MAILBOX);
  FastLED.addLeds<WS2812B, DATA_PIN_GIRL, GRB>(girlLeds, NUM_LEDS_GIRL);
  FastLED.addLeds<WS2812B, DATA_PIN_BOY, GRB>(boyLeds, NUM_LEDS_BOY);
}

void normalLights() {
  // turn backlight for kids on, mailbox breathe
  fill_solid(girlLeds, NUM_LEDS_GIRL, CHSV(50, 64, kidsBrightness));
  fill_solid(boyLeds, NUM_LEDS_BOY, CHSV(50, 64, kidsBrightness));
  mailboxGlow();
}

// oscilatng white glow for mailbox
void mailboxGlow() {
  int pos = beatsin16(10, 96, 192); // generate sinwave (bpm, min, max)
  fill_solid(mailboxLeds, NUM_LEDS_MAILBOX, CHSV(50, 64, pos)); // CHSV (hue, saturation, value);
  FastLED.show();
}

// mailboxs & kids glow brightly when message comes in
int messageReceived(int len) {
  fill_solid(mailboxLeds, NUM_LEDS_MAILBOX, CHSV(50, 64, 255));
  fill_solid(girlLeds, NUM_LEDS_GIRL, CHSV(50, 64, 255));
  fill_solid(boyLeds, NUM_LEDS_BOY, CHSV(50, 64, 255));
  FastLED.show();

  // Length of lights on based on num lines in message, where:
  // 1 line = 10 sec on, each additional line += 6 sec
  int lengthOn = 10 + ((len - 1) * 6);

  startMillis = millis();
  return lengthOn;
}

void loop() {
  byte inByte = Serial.read();
  //Serial.println(inByte);

  if (inByte != 255) {      // received an SMS
    messageLights = true;
    Serial.println("Got length");
    int intVal = int(inByte) - 48;  // subtract byte val from ascii table val to get int
    interval = (messageReceived(intVal) * 1000);    // interval period in ms
  }

  if (messageLights) {
    currentMillis = millis();

    Serial.print("timer: ");
    Serial.println((currentMillis - startMillis));

    if (currentMillis - startMillis >= interval) {
      startMillis = currentMillis;
      messageLights = false;
      Serial.println("timer off");
    }
  } else {  // normal lights = mailbox breathing, kids on low
    normalLights();
  }
}
