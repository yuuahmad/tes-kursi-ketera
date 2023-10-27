#include <Arduino.h>

bool mulai_program = false;
void setup()
{

    // start serial connection

    Serial.begin(115200);

    // configure pin 2 as an input and enable the internal pull-up resistor

    pinMode(2, INPUT_PULLUP);

    pinMode(13, OUTPUT);
}

void loop()
{

    // read the pushbutton value into a variable

    int sensorVal = digitalRead(2);

    // print out the value of the pushbutton

    // Keep in mind the pull-up means the pushbutton's logic is inverted. It goes

    // HIGH when it's open, and LOW when it's pressed. Turn on pin 13 when the

    // button's pressed, and off when it's not:

    if (sensorVal == HIGH)
    {
        digitalWrite(13, LOW);
    }
    else
    {
        digitalWrite(13, HIGH);
        mulai_program = true;
    }
    Serial.print(mulai_program);
    Serial.print(" : ");
    Serial.println(sensorVal);
}