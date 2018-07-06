import serial
import sqlite3
import json

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None,parity=serial.PARITY_NONE,rtscts=0,stopbits=1,writeTimeout=None)

conn = sqlite3.connect('test.db')
c = conn.cursor()
temperature = 0
humidity = 0
light = 0

while 1:
    info = ser.read(16)
    # 温湿度传感器
    if (info[2] == 1) and (info[3] == 3) and (info[4] == 1):
        temperature = (int(info[5])*256 + int(info[6]))/100
        humidity = ((int(info[7])*256 + int(info[8]))/100)
        
    # 光照传感器
    elif (info[2] == 1) and (info[3] == 2) and (info[4] == 1):
        light = (int(info[5]))*256 + int(info[6])

    else:
        continue

    print("温度"+str(temperature),end='\t')
    print("湿度"+str(humidity),end='\t')
    print("光强"+str(light))
    
    if(temperature>30):
        # 温度高，电机开始转
        ser.write(b'\xcc\xee\x01\x09\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff')
    else:
        # 温度低，电机停止
        ser.write(b'\xcc\xee\x01\x09\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff')

    if(light < 300):
        ser.write(b'\xcc\xee\x01\x09\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff')
    else:
        ser.write(b'\xcc\xee\x01\x09\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff')

    sql = "insert into TH(TEMPERATURE,HUMIDITY,LIGHT) values ("+str(temperature)+","+str(humidity)+","+str(light)+")"
    print(sql)
    c.execute(sql)
    conn.commit()
    data = {
        'temperature' : temperature,
        'humidity' : humidity,
        'light': light
    }
    with open('thInfo.json', 'w') as f:
        json.dump(data, f)
