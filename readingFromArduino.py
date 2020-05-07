import serial
ser = serial.Serial("COM4", 9600);

t = ser.read()
t = ser.read()

print(int.from_bytes(t, 'big') - 48)

ser.close()
