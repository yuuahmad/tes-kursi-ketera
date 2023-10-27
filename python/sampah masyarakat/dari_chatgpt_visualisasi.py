import serial
import csv
import datetime
import matplotlib.pyplot as plt

# Inisialisasi list untuk menyimpan data
timestamps = []
data1_values = []
data2_values = []
data3_values = []

# Konfigurasi port serial
ser = serial.Serial("COM3", 9600)  # Ganti 'COM3' dengan nama port Arduino Anda
ser.flushInput()

# Dapatkan waktu saat ini
waktu_nama_file = datetime.datetime.now()

# Formatkan waktu sesuai dengan yang Anda inginkan (misalnya, YYYYMMDD_HHMMSS)
format_waktu = waktu_nama_file.strftime("%Y%m%d_%H%M%S")

# Buat file CSV untuk menyimpan data
csv_filename = "data_sensor_" + format_waktu + ".csv"

# Inisialisasi file CSV
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = [
        "Waktu",
        "Data1",
        "Data2",
        "Data3",
        "Data4",
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

                    # Simpan data ke list
                    timestamps.append(waktu_sekarang)
                    data1_values.append(float(data_list[0]))
                    data2_values.append(float(data_list[1]))
                    data3_values.append(float(data_list[2]))
                    data3_values.append(float(data_list[3]))

                    data_dict = {
                        "Waktu": waktu_sekarang,
                        "Data1": data_list[0],
                        "Data2": data_list[1],
                        "Data3": data_list[2],
                        "Data4": data_list[3],
                    }

                    # Simpan data ke file CSV
                    writer.writerow(data_dict)
                else:
                    print("Data tidak sesuai format: " + data)

            # Visualisasi data
            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, data1_values, label="Data1")
            plt.plot(timestamps, data2_values, label="Data2")
            # plt.plot(timestamps, data3_values, label="Data3")
            plt.xlabel("Waktu")
            plt.ylabel("Nilai Data")
            plt.title("Visualisasi Data")
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    except KeyboardInterrupt:
        print("Menghentikan program...")
        ser.close()

# Pastikan Anda menutup koneksi serial setelah selesai
ser.close()
