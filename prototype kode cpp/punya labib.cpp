#include <Arduino.h>
#include <SPI.h>
#include <SD.h>
#include <HX711.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
// #include <EEPROM.h>

#define I2C_ADDR 0x27
#define LCD_COLUMNS 20
#define LCD_LINES 4

RTC_DS3231 rtc;
HX711 scale1; // Sensor Load Cell 1
HX711 scale2; // Sensor Load Cell 2

// Pin yang terhubung ke relay
#define relay1 6
#define relay2 7
#define button1 8
#define button2 9
#define button3 5

float calibration_factor1 = -43.80; // Kalibrasi sensor Load Cell 1
float calibration_factor2 = -86.80; // Kalibrasi sensor Load Cell 2
float GRAM1;
float GRAM2;
float KG1;
float KG2;

unsigned long previousMillis = 0;
const long interval = 800;
const float alpha = 0.75; // Rasio 80/20
float smoothedValue1 = 0;
float smoothedValue2 = 0;

bool button1State = LOW;     // State awal tombol 1
bool lastButton1State = LOW; // State sebelumnya tombol 1
bool button2State = LOW;     // State awal tombol 2
bool lastButton2State = LOW; // State sebelumnya tombol 2
bool button3State = LOW;     // State awal tombol 2
bool lastButton3State = LOW;

int loopCounter = 0;        // Hitungan loop
bool isLoopRunning = false; // Status loop berjalan
bool LCD = true;

File dataFile;
LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLUMNS, LCD_LINES);

bool isRecordingData = false; // Status pencatatan data
int recordingCounter = 0;
bool isNewFile = true;
bool tbl2 = false;

void setup()
{

    Serial.begin(9600);
    Serial.println("Initializing the scale");
    pinMode(relay1, OUTPUT);
    pinMode(relay2, OUTPUT);
    pinMode(button1, INPUT_PULLUP);
    pinMode(button2, INPUT_PULLUP);
    pinMode(button3, INPUT_PULLUP);
    scale1.begin(A2, A1);
    scale2.begin(3, 2);
    scale1.set_scale(calibration_factor1);
    scale2.set_scale(calibration_factor2);
    scale1.tare();
    scale2.tare();
    lcd.init();
    lcd.backlight();
    rtc.begin();
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    //  loopCounter = EEPROM.read(0);
}

void loop()
{

    if (!SD.begin(10))
    {
        Serial.println("Gagal inisialisasi SD Card.");
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.println("Masukan SD Card");
        return;
    }
    else
    {
        Serial.print("aman");
    }
    DateTime now = rtc.now();
    int btn1 = digitalRead(button1);
    int btn2 = digitalRead(button2);
    int btn3 = digitalRead(button3);
    GRAM1 = scale1.get_units(), 4;
    KG1 = GRAM1 / 1000;

    GRAM2 = scale2.get_units(), 4;
    KG2 = GRAM2 / 1000;

    smoothedValue1 = alpha * KG1 + (1 - alpha) * smoothedValue1;
    smoothedValue2 = alpha * KG2 + (1 - alpha) * smoothedValue2;

    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval && LCD)
    {
        previousMillis = currentMillis;

        if (smoothedValue1 < 0)
        {
            smoothedValue1 = 0;
        }
        if (smoothedValue2 < 0)
        {
            smoothedValue2 = 0;
        }

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("B1:");
        lcd.print(smoothedValue1, 1);
        lcd.print(" Kg");
        lcd.print(" ");

        lcd.setCursor(0, 1);
        lcd.print("B2:");
        lcd.print(smoothedValue2, 1);
        lcd.print(" Kg");
        lcd.print(" ");
    }

    if (btn1 == HIGH && lastButton1State == LOW && isNewFile)
    {
        if (!isLoopRunning)
        {
            isLoopRunning = true;
            digitalWrite(relay2, HIGH);
            digitalWrite(relay1, HIGH);
            tbl2 = true;
            isNewFile = false;
            char fileName[13];
            sprintf(fileName, "data%03d.csv", recordingCounter);
            dataFile = SD.open(fileName, FILE_WRITE);
            recordingCounter++;
            if (dataFile)
            {
                dataFile.println("Tanggal, Berat 1 (Kg), Berat 2 (Kg)");
            }
        }
        else
        {
        }
    }
    if (btn2 == HIGH && lastButton2State == LOW && tbl2)
    {
        if (!isLoopRunning)
        {
            isLoopRunning = true;
            digitalWrite(relay2, HIGH);
            digitalWrite(relay1, HIGH);
        }
        else
        {
            isLoopRunning = false;
            digitalWrite(relay2, LOW);
            digitalWrite(relay1, LOW);
            // Data saat ini akan disimpan saat loop berikutnya dimulai
        }
    }

    if (btn3 == HIGH && lastButton3State == LOW)
    {
        loopCounter = 0;
        isLoopRunning = false;
        LCD = true;
        isNewFile = true;
        tbl2 = false;
        digitalWrite(relay2, LOW);
        digitalWrite(relay1, LOW);
        if (dataFile)
        {
            dataFile.close();
            isRecordingData = false;
        }
    }

    if (isLoopRunning)
    {
        if (loopCounter < 10000)
        {
            if (currentMillis - previousMillis >= interval)
            {
                previousMillis = currentMillis;
                if (digitalRead(relay1) == LOW && digitalRead(relay2) == LOW)
                {
                    digitalWrite(relay2, HIGH);
                    digitalWrite(relay1, HIGH);
                    loopCounter++;
                }
                else
                {
                    digitalWrite(relay2, LOW);
                    digitalWrite(relay1, LOW);
                    if (dataFile)
                    {
                        //            dataFile.print(millis());
                        dataFile.print(now.year(), DEC);
                        dataFile.print('/');
                        dataFile.print(now.month(), DEC);
                        dataFile.print('/');
                        dataFile.print(now.day(), DEC);
                        dataFile.print(' ');
                        dataFile.print(now.hour(), DEC);
                        dataFile.print(':');
                        dataFile.print(now.minute(), DEC);
                        dataFile.print(':');
                        dataFile.print(now.second(), DEC);
                        dataFile.print(",");
                        dataFile.print(smoothedValue1);
                        dataFile.print(",");
                        dataFile.println(smoothedValue2);
                        if (!isRecordingData)
                        {
                            isRecordingData = true;
                        }
                    }
                }
            }

            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("count: ");
            lcd.print(loopCounter);
            lcd.setCursor(0, 1);
            // lcd.print(now.year(), DEC);
            // lcd.print('/');
            lcd.print(now.month(), DEC);
            lcd.print('/');
            lcd.print(now.day(), DEC);
            lcd.print(' ');
            lcd.print(now.hour(), DEC);
            lcd.print(':');
            lcd.print(now.minute(), DEC);
            lcd.print(':');
            lcd.print(now.second(), DEC);
            lcd.print(",");
            LCD = false;
        }
        else
        {
            isLoopRunning = false;
            digitalWrite(relay2, LOW);
            digitalWrite(relay1, LOW);
            loopCounter = 0;
            tbl2 = false;
            LCD = true;
            if (dataFile)
            {
                dataFile.close();
            }
            isRecordingData = false;
            isNewFile = true;
        }
    }

    lastButton1State = btn1;
    lastButton2State = btn2;
    lastButton3State = btn3;

    //  EEPROM.write(0, loopCounter);
}
