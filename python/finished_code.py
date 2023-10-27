import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("fivethirtyeight")


index = count()


def animate(i):
    # x_vals = []
    # y_vals = []
    data = pd.read_csv("data_sensor.csv")
    x = data["langkah_ke"]
    y1 = data["beban_dudukan"]
    y2 = data["beban_sandaran"]
    x = x[-100:]
    # y_vals.append(y)
    # print(y)
    # Menampilkan hanya 100 data terakhir
    # if len(x) > 100:
    # y1 = y1[-100:]
    y1 = y1[-100:]
    y2 = y2[-100:]

    plt.cla()

    plt.plot(y1, label="beban_dudukan")
    plt.plot(y2, label="beban_sandaran")

    plt.legend(loc="upper left")
    # plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=50)

plt.tight_layout()
plt.show()
