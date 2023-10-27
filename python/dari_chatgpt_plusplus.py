import serial
import csv
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

# import matplotlib

# Konfigurasi port serial
ser = serial.Serial("COM4", 38400)  # Ganti 'COM3' dengan nama port Arduino Anda
ser.flushInput()
# ser.open()
# time.sleep(3)  # tunggu untuk inisialisasi data
print("siap menerima dan menulis data")

# Kirim karakter 'g' ke Arduino
# ser.write(b"g")
# time.sleep(3)

# Dapatkan waktu saat ini
waktu_nama_file = datetime.datetime.now()
# Formatkan waktu sesuai dengan yang Anda inginkan (misalnya, YYYYMMDD_HHMMSS)
format_waktu = waktu_nama_file.strftime("%Y%m%d_%H%M%S")
# Buat file CSV untuk menyimpan data
# csv_filename = "data_sensor_" + format_waktu + ".csv"
csv_filename = "data_sensor.csv"


# variabel2 untuk mengumpulkan data
var_langkah_ke = []
var_beban_dudukan = []
var_beban_sandaran = []
var_keadaan_relay = []

# Inisialisasi file CSV
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = [
        "waktu",
        "langkah_ke",
        "beban_dudukan",
        "beban_sandaran",
        "keadaan_relay",
    ]  # Sesuaikan dengan jumlah data yang Anda kirimkan
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    try:
        while True:
            if ser.inWaiting() > 0:
                data = (
                    ser.readline().decode("utf-8").strip()
                )  # Membaca data dari Arduino
                print(data)  # Tampilkan data ke layar

                # Pisahkan data berdasarkan koma
                data_list = data.split(",")

                if len(data_list) == 4:
                    # Ambil timestamp waktu sekarang
                    waktu_sekarang = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    data_dict = {
                        "waktu": waktu_sekarang,
                        "langkah_ke": data_list[0],
                        "beban_dudukan": data_list[1],
                        "beban_sandaran": data_list[2],
                        "keadaan_relay": data_list[3],
                    }
                    # var_keadaan_relay.append(float(data_list[3]))
                    # var_langkah_ke.append(float(data_list[0]))

                    # var_keadaan_relay = var_keadaan_relay[-50:]
                    # var_langkah_ke = var_langkah_ke[-50:]

                    # ax.clear()                                          # Clear last data frame
                    # ax.plot(dataList)                                   # Plot new data f
                    # ax.set_ylim([0, 1200])                              # Set Y axis limit of plot
                    # ax.set_title("Arduino Data")                        # Set title of figure
                    # ax.set_ylabel("Value")                              # Set title of y axis

                    # Simpan data ke file CSV
                    writer.writerow(data_dict)
                else:
                    print("Data tidak sesuai format: " + data)

    except KeyboardInterrupt:
        print("Menghentikan program...")
        ser.close()

ser.close()
# Pastikan Anda menutup koneksi serial setelah selesai
