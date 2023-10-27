import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

# konstanta
SERIAL_PORT = "COM3"
BAUD_RATE = 9600

# hanya untuk testing lib
# print("hai dunia apa kabar anda")

# inisialisasi komunikasi serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# inisialisasi list kosong untuk store data
langkah_ke = []
beban_dudukan = []
beban_sandaran = []
kondisi_relay = []


# buat fungsi untuk baca dan proses data dari arduino
def baca_dan_proses_data():
    # ser.write(b"g")  # Transmit the char 'g' to receive the Arduino data point
    line = ser.readline().decode("utf-8").strip
    nilai_sensor = line.split(",")

    langkah_ke.append(float(nilai_sensor[0]))
    beban_dudukan.append(float(nilai_sensor[1]))
    beban_sandaran.append(float(nilai_sensor[2]))
    kondisi_relay.append(float(nilai_sensor[3]))

    # tampilkan data yang diterima
    print(
        f"langkah_ke {nilai_sensor[0]}, beban dudukan {nilai_sensor[1]}, beban sandaran {nilai_sensor[2]}, kondisi relay {nilai_sensor[3]}"
    )


# buat fungsi untuk update plot
def update_plot():
    baca_dan_proses_data()
    plt.cla()
    plt.plot(langkah_ke, beban_dudukan, label="beban dudukan")
    plt.plot(langkah_ke, beban_sandaran, label="beban sandaran")
    plt.xlabel("langkah_ke")
    plt.ylabel("nilai beban")
    plt.legend()


# buat fungsi simpan ke csv ketika plot ditutup
def ketika_ditutup():
    with open("nilai_tes_destruksi.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow("langkah_ke", "beban_dudukan", "beban_sandaran")
        for x, s1, s2 in zip(langkah_ke, beban_dudukan, beban_sandaran):
            writer.writerow([x, s1, s2])


# daftarkan fungsi "callback" ketika fungsi update plot ditutup
fig, ax = plt.subplots()
fig.canvas.mpl_connect("close_event", ketika_ditutup)

ani = FuncAnimation(fig, update_plot, interval=10)
plt.show()
