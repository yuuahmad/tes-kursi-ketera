import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import csv

ser = serial.Serial(
    "COM4", 9600
)  # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
time.sleep(2)  # Time delay for Arduino Serial initialization

dataList = []  # Create empty list variable for later use

class AnimationPlot:
    def animate(self, dataList, ser):
        ser.write(b"g")  # Transmit the char 'g' to receive the Arduino data point
        data = ser.readline().decode(
            "utf-8").strip()
        # Decode receive Arduino data as a formatted string
        print(data)                                           # 'i' is a incrementing variable based upon frames = x argument
        data_list = data.split(",")

        if len(data_list) == 4:
            # Ambil timestamp waktu sekarang
            waktu_sekarang = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_dict = {
                'Waktu': waktu_sekarang,
                'Data1': data_list[0],
                'Data2': data_list[1],
                'Data3': data_list[2],
                'Data4': data_list[3]
            }
            # Simpan data ke file CSV
            # writer.writerow(data_dict)
        else:
            print("Data tidak sesuai format: " + data)

        try:
            arduinoData_float = float(data_list[4])  # Convert to float
            dataList.append(
                arduinoData_float
            )  # Add to the list holding the fixed number of points to animate

        except:  # Pass if data point is bad
            pass

        dataList = dataList[
            -50:
        ]  # Fix the list size so that the animation plot 'window' is x number of points

        ax.clear()  # Clear last data frame

        self.getPlotFormat()
        ax.plot(dataList)  # Plot new data frame

    def getPlotFormat(self):
        ax.set_ylim([0, 3])  # Set Y axis limit of plot
        ax.set_title("Arduino Data")  # Set title of figure
        ax.set_ylabel("keadaan_relay")  # Set title of y axis


fig = plt.figure()  # Create Matplotlib plots fig is the 'higher level' plot window
ax = fig.add_subplot(111)  # Add subplot to main fig window

realTimePlot = AnimationPlot()

# Matplotlib Animation Fuction that takes takes care of real time plot.
# Note that 'fargs' parameter is where we pass in our dataList and Serial object.
ani = animation.FuncAnimation(
    fig, realTimePlot.animate, frames=100, fargs=(dataList, ser), interval=100
)

plt.show()  # Keep Matplotlib plot persistent on screen until it is closed
ser.close()  # Close Serial connection when plot is closed
