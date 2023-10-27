#include <Arduino.h>
#include "HX711.h"
// #include "avr_debugger.h"
// #include <app_api.h>
/*
ini adalah projek untuk alat tes destruksi / dulability kursi kereta d-tech
kode ini diupload ke arduino nano dan dengan komunikasi serialnya, arduino ini akan mengirimkan data
ke laptop untuk selanjutnya diolah, divisualisasi, dan disimpan

anda dapat melihat kode ini di github saya (masih publik) di
https://github.com/yuuahmad/tes-kursi-ketera
*/

// inisialisassi pin RELAY
const int RELAY_1 = 7;
const int RELAY_2 = 6;
bool nilai_relay = false;

// inisialisassi pin dan nilai2 LOADCELL
const int LOADCELL_1_SCK = A1;
const int LOADCELL_1_DT = A2;
const int LOADCELL_2_SCK = 2;
const int LOADCELL_2_DT = 3;
float calibration_factor1 = -43.80; // Kalibrasi sensor Load Cell 1
float calibration_factor2 = -86.80; // Kalibrasi sensor Load Cell 2
float GRAM1;
float GRAM2;
float KG1;
float KG2;
const float alpha = 0.75; // Rasio 80/20
float smoothedValue1 = 0;
float smoothedValue2 = 0;

// inisialisasi nilai milis loadcell (untuk store data agar milis berjalan)
unsigned long milis_relay;
unsigned long milis_relay_sebelumnya;
unsigned long milis_loadcell;

// inisialisasi nilai untuk counter mundur
float nilai_ke = 1000;

HX711 sensor_loadcell_1;
HX711 sensor_loadcell_2;

void setup()
{
    // debug_init();
    Serial.begin(9600);
    // program eksekusi awal loadcell pertama
    sensor_loadcell_1.begin(LOADCELL_1_DT, LOADCELL_1_SCK);
    sensor_loadcell_1.set_scale(calibration_factor1);
    sensor_loadcell_1.tare();
    // program eksekusi awal loadcell kedua
    sensor_loadcell_2.begin(LOADCELL_2_DT, LOADCELL_2_SCK);
    sensor_loadcell_2.set_scale(calibration_factor2);
    sensor_loadcell_2.tare();

    // inisialisasi relay
    pinMode(RELAY_1, OUTPUT);
    pinMode(RELAY_2, OUTPUT);
}

void loop()
{
    // reset nilai milis relay
    milis_relay = millis();

    // dapatkan nilai pembancaan sensor loadcell
    // loadcell pertama
    GRAM2 = sensor_loadcell_2.get_units();                       // baca nilai loadcell
    KG2 = GRAM2 / 1000;                                          // buat jadi kilogram
    smoothedValue2 = alpha * KG2 + (1 - alpha) * smoothedValue2; // buat nilainya menjadi halus dengan memprosesnya dengan alpha
    // loadcell kedua
    GRAM2 = sensor_loadcell_2.get_units();                       // baca nilai loadcell
    KG2 = GRAM2 / 1000;                                          // buat jadi kilogram
    smoothedValue2 = alpha * KG2 + (1 - alpha) * smoothedValue2; // buat nilainya menjadi halus dengan memprosesnya dengan alpha
                                                                 // if (smoothedValue2 < 0)                                      // buat nilainya selalu positif dan tak pernah negatif
                                                                 //   smoothedValue2 = 0;

    // program untuk switching relay
    if ((milis_relay - milis_relay_sebelumnya) >= 1200) // jangan gunakan delay, tapi milis dan karena 1hz maka nilai hidup dan nilai mati 1/2 detik
    {
        if (nilai_ke > 0)
            nilai_relay = !nilai_relay; // program untuk melakukan switcing pada relay
        else
            nilai_relay = false;
        nilai_ke = nilai_ke - 0.5;
        milis_relay_sebelumnya = milis_relay;
    }
    digitalWrite(RELAY_1, nilai_relay);
    digitalWrite(RELAY_2, nilai_relay);

    // program untuk mengrimkan data ke komputer
    if (nilai_ke > 0) // tunggu maksimal 1 setik untuk memastikan sensor hadir/terpasang dengan benar
    {
        Serial.print(nilai_ke);
        Serial.print(",");
        Serial.print(smoothedValue1);
        Serial.print(",");
        Serial.print(smoothedValue2);
        Serial.print(",");
        Serial.println(nilai_relay);
    }
    else
        Serial.println("Error / cycle telah habis");
}