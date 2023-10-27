import csv
import matplotlib.pyplot as plt
import threading
import time


def read_csv(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def update_plot(data):
    plt.clf()
    plt.plot([x[1] for x in data], [x[4] for x in data])
    plt.show()


def main():
    # Baca data dari file CSV
    data = read_csv("data_sensor.csv")

    # Buat list untuk menyimpan data terbaru
    latest_data = []

    # Buat thread untuk membaca data secara real time
    t = threading.Thread(target=read_csv, args=["data_sensor.csv"])
    t.daemon = True
    t.start()

    # Tampilkan plot data
    update_plot(data)

    while True:
        # Tambahkan data terbaru ke list
        latest_data.append(data[-1])

        # Hapus data yang paling lama
        if len(latest_data) > 50:
            latest_data.pop(0)

        # Perbarui plot data
        update_plot(latest_data)

        time.sleep(1)


if __name__ == "__main__":
    main()