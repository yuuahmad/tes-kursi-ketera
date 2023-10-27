import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class AnimationPlot:
    def animate(self, i, dataList, ser):
        ser.write(b"g")  # Transmit the char 'g' to receive the Arduino data point
        arduinoData_string = (
            ser.readline().decode("utf-8").strip()
        )  # Decode received Arduino data as a formatted string

        try:
            arduinoData_list = arduinoData_string.split(
                ","
            )  # Pisahkan data berdasarkan koma
            if len(arduinoData_list) == 4:
                # data1 = float(arduinoData_list[0])
                # data2 = float(arduinoData_list[1])
                # data3 = float(arduinoData_list[2])
                data4 = float(arduinoData_list[0])  # data keadaan relay
                print(data4)

                dataList.append((data4))
            else:
                print("Data tidak sesuai format: " + arduinoData_string)
        except:  # Tangani jika data tidak valid
            pass

        dataList = dataList[-50:]  # Batasi jumlah data yang ditampilkan

        ax.clear()  # Bersihkan frame plot sebelum menggambar yang baru

        self.getPlotFormat()
        # data4 = zip(*dataList)
        # ax.plot(data1,data2, label="nilai ke")
        # ax.plot(data1, data2, label="beban dudukan")
        # ax.plot(data1, data3, label="beban sandaran")
        ax.plot(data4)

    def getPlotFormat(self):
        ax.set_ylim([0, 2])  # Atur batas sumbu Y pada plot
        ax.set_title("Arduino Data")  # Atur judul plot
        ax.set_ylabel("Value")  # Atur label sumbu Y


dataList = []  # Buat list kosong untuk menyimpan data

fig = plt.figure()  # Buat objek gambar Matplotlib
ax = fig.add_subplot(111)  # Tambahkan subplot ke objek gambar

realTimePlot = AnimationPlot()

ser = serial.Serial("COM3", 9600)  # Buka koneksi serial ke Arduino
time.sleep(2)  # Tunda selama 2 detik untuk inisialisasi koneksi serial

ani = animation.FuncAnimation(
    fig, realTimePlot.animate, frames=1000, fargs=(dataList, ser), interval=100
)

plt.show()  # Tampilkan plot Matplotlib
ser.close()  # Tutup koneksi serial ketika plot ditutup
