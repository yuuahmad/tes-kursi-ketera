
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('data_sensor.csv')
    # x = data['Waktu']
    x = data['langkah_ke']
    x_vals.append(x)
    x_vals = x_vals[-10:]
    y2 = data['keadaan_relay']
    y_vals.append(y2)
    # y_vals = y_vals[-10:]

    plt.cla()

    # plt.plot(x, y1, label='Channel 1')
    plt.plot(x_vals, label='keadaan relay')

    plt.legend(loc='upper left')
    # plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100, frames=100)

plt.tight_layout()
plt.show()