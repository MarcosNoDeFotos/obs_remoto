
// Botones
#include <ezButton.h>

#define BUTTON_PIN_1 2  
#define BUTTON_PIN_2 3  
#define BUTTON_PIN_3 4  
#define BUTTON_PIN_4 5  
#define BUTTON_PIN_5 6  
#define BUTTON_PIN_6 7
#define BUTTON_PIN_7 8  
#define BUTTON_PIN_8 9  
#define BUTTON_PIN_9 10  
#define BUTTON_PIN_10 11 
#define BUTTON_PIN_11 12 
#define BUTTON_PIN_12 A0 
#define BUTTON_PIN_13 A1 
#define BUTTON_PIN_14 A2 
#define BUTTON_PIN_15 A3 
#define DELAY_DETECCION_BOTON 20
ezButton button1(BUTTON_PIN_1);  
ezButton button2(BUTTON_PIN_2);  
ezButton button3(BUTTON_PIN_3);  
ezButton button4(BUTTON_PIN_4);  
ezButton button5(BUTTON_PIN_5);  
ezButton button6(BUTTON_PIN_6);  
ezButton button7(BUTTON_PIN_7);  
ezButton button8(BUTTON_PIN_8);  
ezButton button9(BUTTON_PIN_9);  
ezButton button10(BUTTON_PIN_10);  
ezButton button11(BUTTON_PIN_11);  
ezButton button12(BUTTON_PIN_12);  
ezButton button13(BUTTON_PIN_13);  
ezButton button14(BUTTON_PIN_14);  
ezButton button15(BUTTON_PIN_15);  

// !Botones

// Potenciómetros
const int potentiometerPIN = A0;  // select the input pin for the potentiometer

int potentiometerValue = 0;  // variable to store the value coming from the sensor
int potentiometerMaxValue = 255;
int A0lastValue = 0;
int A1lastValue = 0;
int A2lastValue = 0;
int A3lastValue = 0;

// !Potenciómetros


struct Tuple {
  char* pin;
  int value;
};


void setup() {
  Serial.begin(9600);

  button1.setDebounceTime(DELAY_DETECCION_BOTON);  
  button2.setDebounceTime(DELAY_DETECCION_BOTON);  
  button3.setDebounceTime(DELAY_DETECCION_BOTON);  
  button4.setDebounceTime(DELAY_DETECCION_BOTON);  
  button5.setDebounceTime(DELAY_DETECCION_BOTON);  
  button6.setDebounceTime(DELAY_DETECCION_BOTON);
  button7.setDebounceTime(DELAY_DETECCION_BOTON);
  button8.setDebounceTime(DELAY_DETECCION_BOTON);
  button9.setDebounceTime(DELAY_DETECCION_BOTON);
  button10.setDebounceTime(DELAY_DETECCION_BOTON);
  button11.setDebounceTime(DELAY_DETECCION_BOTON);
  button12.setDebounceTime(DELAY_DETECCION_BOTON);
  button13.setDebounceTime(DELAY_DETECCION_BOTON);
  button14.setDebounceTime(DELAY_DETECCION_BOTON);
  button15.setDebounceTime(DELAY_DETECCION_BOTON);
}

void loop() {

  // struct Tuple a0Value = readPotentiometer(A0);
  // struct Tuple a1Value = readPotentiometer(A1);
  // struct Tuple a2Value = readPotentiometer(A2);
  // struct Tuple a3Value = readPotentiometer(A3);


  // printPinValue(a0Value);
  // printPinValue(a1Value);
  // printPinValue(a2Value);
  // printPinValue(a3Value);
  button1.loop();  
  button2.loop();  
  button3.loop();  
  button4.loop();  
  button5.loop();  
  button6.loop();  
  button7.loop();  
  button8.loop();  
  button9.loop();  
  button10.loop();  
  button11.loop();  
  button12.loop();  
  button13.loop();  
  button14.loop();  
  button15.loop();  

  int button1_state = button1.getState();  
  int button2_state = button2.getState();  
  int button3_state = button3.getState();  
  int button4_state = button4.getState();  
  int button5_state = button5.getState();  
  int button6_state = button6.getState();  
  int button7_state = button7.getState();  
  int button8_state = button8.getState();  
  int button9_state = button9.getState();  
  int button10_state = button10.getState();  
  int button11_state = button11.getState();  
  int button12_state = button12.getState();  
  int button13_state = button13.getState();  
  int button14_state = button14.getState();  
  int button15_state = button15.getState();  

  if (button1.isPressed())
    Serial.println("B1");
  if (button2.isPressed())
    Serial.println("B2");
  if (button3.isPressed())
    Serial.println("B3");
  if (button4.isPressed())
    Serial.println("B4");  
  if (button5.isPressed())
    Serial.println("B5");
  if (button6.isPressed())
    Serial.println("B6");
  if (button7.isPressed())
    Serial.println("B7");
  if (button8.isPressed())
    Serial.println("B8");
  if (button9.isPressed())
    Serial.println("B9");
  if (button10.isPressed())
    Serial.println("B10");
  if (button11.isPressed())
    Serial.println("B11");
  if (button12.isPressed())
    Serial.println("B12");
  if (button13.isPressed())
    Serial.println("B13");
  if (button14.isPressed())
    Serial.println("B14");
  if (button15.isPressed())
    Serial.println("B15");
  
  
}

void printPinValue(struct Tuple value){
  if (value.value != -1) {
    Serial.print(value.pin);
    Serial.print("|");
    Serial.println(value.value);
  }
}



struct Tuple readPotentiometer(int pin) {
  int sensorValue = analogRead(pin);
  int lastValue = A0lastValue;
  char* pinText = "A0";
  
  int outputValue = map(sensorValue, 0, 1010, -2, 105);
  if (outputValue > 100) {
    outputValue = 100;
  }
  if (outputValue < 0) {
    outputValue = 0;
  }
  switch (pin) {
    case A1:
      pinText = "A1";
      lastValue = A1lastValue;
      break;
    case A2:
      pinText = "A2";
      lastValue = A2lastValue;
      break;
    case A3:
      pinText = "A3";
      lastValue = A3lastValue;
      break;
  }

  if (outputValue != lastValue) {
    setLastValue(pin, outputValue);
    Tuple r = { pinText, outputValue };
    return r;
  } else {
    setLastValue(pin, outputValue);
    Tuple r = { pinText, -1 };
    return r;
  }
}

void setLastValue(int pin, int lastValue){
  switch (pin) {
    case A0:
      A0lastValue = lastValue;
      break;
    case A1:
      A1lastValue = lastValue;
      break;
    case A2:
      A2lastValue = lastValue;
      break;
    case A3:
      A3lastValue = lastValue;
      break;

  }
}

