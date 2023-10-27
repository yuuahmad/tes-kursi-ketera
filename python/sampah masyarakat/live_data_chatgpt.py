import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Fungsi untuk membaca data CSV
def read_csv_data(csv_file):
    data = pd.read_csv(csv_file)
    return data

# Fungsi untuk memvisualisasikan data
def visualize_data(data):
    fig, ax = plt.subplots()

    # Inisialisasi plot
    line, = ax.plot([], [], label='keadaan_relay')
    ax.set_xlim(data['waktu'].min(), data['waktu'].max())  # Ganti 'waktu' dengan nama kolom waktu di file CSV
    ax.set_ylim(data['keadaan_relay'].min(), data['keadaan_relay'].max())  # Ganti 'keadaan_relay' dengan nama kolom keadaan_relay di file CSV

    # Fungsi inisialisasi plot
    def init():
        line.set_data([], [])
        return line,

    # Fungsi animasi untuk memperbarui plot
    def update(frame):
        # Perbarui data yang akan ditampilkan
        line.set_data(data['waktu'][:frame], data['keadaan_relay'][:frame])
        return line,

    # Buat animasi
    ani = FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True)

    # Tambahkan label dan legenda
    ax.set_xlabel('waktu')
    ax.set_ylabel('keadaan_relay')
    ax.legend(loc='upper left')

    plt.show()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file

    def on_modified(self, event):
        if event.src_path.endswith(self.csv_file):
            data = read_csv_data(self.csv_file)
            visualize_data(data)

if __name__ == '__main__':
    csv_file = 'data_sensor.csv'  # Ganti dengan nama file CSV yang Anda miliki
    data = read_csv_data(csv_file)
    visualize_data(data)

    event_handler = FileChangeHandler(csv_file)
    observer = Observer()
    observer.schedule(event_handler, path='.')
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
