import serial


class Sensor:
    def __init__(self, device, baudrate=9600):
        self.ser = serial.Serial(device, baudrate)
        self.temperature = 0
        self.update()

    def update(self):
        text = self.ser.readline()
        if not text.isspace():
            self.temperature = float(text)

    def __str__(self):
        return str(self.temperature)
