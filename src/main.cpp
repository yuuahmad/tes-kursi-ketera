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
// const int RELAY_1 = 7;
const int RELAY_2 = 6;
bool nilai_relay = true;

// inisialisassi pin dan nilai2 LOADCELL
const int LOADCELL_1_SCK = 13; // ini loadcell dudukan
const int LOADCELL_1_DT = 12;
const int LOADCELL_2_SCK = 11; // ini loadcell sandaran
const int LOADCELL_2_DT = 10;
float calibration_factor1 = -86.80; // Kalibrasi sensor Load Cell 2
float calibration_factor2 = -43.80; // Kalibrasi sensor Load Cell 1
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
float nilai_ke = 0;
// inisialisasi nilai untuk user input
char userInput;
// bool untuk menyatakan sudah ada perintah dari komputer atau belum
bool mulai_program = false;
// inisialisasi pin tombol start
// const int tombol_start = 2;
// bool keadaan_tombol_start = false; // buat keadaannya false dulu

HX711 sensor_loadcell_1;
HX711 sensor_loadcell_2;

void setup()
{
  // debug_init();
  Serial.begin(38400);
  // delay(1000);
  // Serial.println("bersiap memulai program");
  pinMode(RELAY_2, OUTPUT);
  digitalWrite(RELAY_2, HIGH);
  // program eksekusi awal loadcell pertama
  sensor_loadcell_1.begin(LOADCELL_1_DT, LOADCELL_1_SCK);
  sensor_loadcell_2.begin(LOADCELL_2_DT, LOADCELL_2_SCK);
  sensor_loadcell_1.set_scale(calibration_factor1);
  sensor_loadcell_2.set_scale(calibration_factor2);
  sensor_loadcell_1.tare();
  sensor_loadcell_2.tare();
  // program eksekusi awal loadcell kedua

  // inisialisasi relay
  // pinMode(RELAY_1, OUTPUT);
  // pastikan nilai relay LOW saat inisialisasi
  // alasannya karena relay akan hidup ketika inputnya low
  // begitupula ketika keadaan default
  // dan karena itulah saya menggunakan output normal close
  // karena akan open saat active.
  // memang aneh, tapi begiilah kenyataannya
  // digitalWrite(RELAY_1, HIGH);
  // delay(10000); // delay untuk menunggu koneksi dengan komputer.
  // inisialisasi tombol start dan buat input pullup
  // pinMode(2, INPUT_PULLUP);
  mulai_program = true;
  delay(5000);
  // Serial.println("bantuan kedua");
}

void loop()
{
  // perintah ini gagal karena dapat menyebabkan loadcell mengganggu penerimaan karakter dari komputer
  // if (Serial.available() > 0)
  // {
  //   userInput = Serial.read(); // read user input
  //   if (userInput == 'g')
  //   { // if we get expected value
  //     mulai_program = true;
  //   } // if user input 'g'
  // }   // Serial.available
  // gunakan hanya satu arah, dan tidak akan kembali lagi
  // int keadaan_tombol_start = digitalRead(2);
  // if (keadaan_tombol_start == LOW)
  //     digitalWrite(13, LOW);
  // else
  // {
  //     digitalWrite(13, HIGH);
  // mulai_program = true;

  // reset nilai milis relay
  milis_relay = millis();

  // dapatkan nilai pembancaan sensor loadcell
  // loadcell pertama
  // GRAM1 = sensor_loadcell_1.get_units();                       // baca nilai loadcell
  // KG1 = GRAM1 / 1000;                                          // buat jadi kilogram
  // smoothedValue1 = alpha * KG1 + (1 - alpha) * smoothedValue1; // buat nilainya menjadi halus dengan memprosesnya dengan alpha
  // // loadcell kedua
  // GRAM2 = sensor_loadcell_2.get_units();                       // baca nilai loadcell
  // KG2 = GRAM2 / 1000;                                          // buat jadi kilogram
  // smoothedValue2 = alpha * KG2 + (1 - alpha) * smoothedValue2; // buat nilainya menjadi halus dengan memprosesnya dengan alpha

  // program untuk switching relay
  if ((milis_relay - milis_relay_sebelumnya) >= 1200 && mulai_program) // jangan gunakan delay, tapi milis dan karena 1hz maka nilai hidup dan nilai mati 1/2 detik
  {
    if (nilai_ke < 10000)
      nilai_relay = !nilai_relay; // program untuk melakukan switcing pada relay
    else
      nilai_relay = true; // ini artinya nilai relay akan mati (seperti diatas, karena saya pakai normal close dan false/LOW artinya hidup)
    nilai_ke = nilai_ke + 0.5;
    milis_relay_sebelumnya = milis_relay;
  }
  // digitalWrite(RELAY_1, nilai_relay);
  digitalWrite(RELAY_2, nilai_relay);

  // program untuk mengrimkan data ke komputer
  if (nilai_ke < 10000 && mulai_program) // tunggu maksimal 1 setik untuk memastikan sensor hadir/terpasang dengan benar
  {
    Serial.print(nilai_ke);
    Serial.print(",");
    Serial.print(sensor_loadcell_1.get_units(), 1);
    Serial.print(",");
    Serial.print(sensor_loadcell_2.get_units(), 1);
    Serial.print(",");
    Serial.println(nilai_relay);
  }
}