#include "FspTimer.h"
FspTimer sampleTimer;

#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h>

PulseSensorPlayground pulseSensor;

const int OUTPUT_TYPE = SERIAL_PLOTTER;

const int PULSE_INPUT = A0;
const int PULSE_BLINK = LED_BUILTIN;
const int PULSE_FADE = 5;
const int THRESHOLD = 550;

const int maxY = 7;
const int minY = 0;

int pulseSignal;

#include "Arduino_LED_Matrix.h"
ArduinoLEDMatrix plotter;
int maxX = 11;
byte frame[8][12] = {
  { 0,0,0,0,0,0,0,0,0,0,0,0 },
  { 0,0,0,0,0,0,0,0,0,0,0,0 },
  { 0,0,0,0,0,0,0,0,0,0,0,0 },
  { 0,0,0,0,0,0,0,0,0,0,0,0 },
  { 0,0,0,0,0,0,0,0,0,0,0,0 },
  { 0,0,0,0,0,0,0,0,0,0,0,0 },
  { 0,0,0,0,0,0,0,0,0,0,0,0 },
  { 0,0,0,0,0,0,0,0,0,0,0,0 }
};

void sampleTimerISR(timer_callback_args_t __attribute((unused)) *p_args) {
  pulseSensor.onSampleTime();
}

void setup() {
  Serial.begin(115200);

  pulseSensor.analogInput(PULSE_INPUT);
  pulseSensor.blinkOnPulse(PULSE_BLINK);
  pulseSensor.fadeOnPulse(PULSE_FADE);

  pulseSensor.setSerial(Serial);
  pulseSensor.setOutputType(OUTPUT_TYPE);
  pulseSensor.setThreshold(THRESHOLD);

  if (!pulseSensor.begin()) {
    Serial.println("PulseSensor initialization failed!");
    while (1);
  }

  uint8_t timer_type = GPT_TIMER;
  int8_t tindex = FspTimer::get_available_timer(timer_type);
  if (tindex == 0) {
    FspTimer::force_use_of_pwm_reserved_timer();
    tindex = FspTimer::get_available_timer(timer_type);
  }

  sampleTimer.begin(TIMER_MODE_PERIODIC, timer_type, tindex, SAMPLE_RATE_500HZ, 0.0f, sampleTimerISR);
  sampleTimer.setup_overflow_irq();
  sampleTimer.open();
  sampleTimer.start();

  plotter.begin();
}

void loop() {
  pulseSensor.outputSample();

  if (pulseSensor.sawStartOfBeat()) {
    int beatsPerMinute = pulseSensor.getBeatsPerMinute();

    Serial.print("bpm: ");
    Serial.println(beatsPerMinute);

  }

  pulseSignal = pulseSensor.getLatestSample();
  pulseSignal = 1023 - pulseSignal;
  pulseSignal = pulseSignal / 128;
  pulseSignal = constrain(pulseSignal, minY, maxY);
  

  advanceLEDplotter();
  plotter.renderBitmap(frame, 8, 12);

  delay(100);
}
