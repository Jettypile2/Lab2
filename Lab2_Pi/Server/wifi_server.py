import socket
import time
import subprocess

from Motor import *            
from Ultrasonic import *
from servo import *

ultrasonic=Ultrasonic() 
PWM=Motor()  
HOST = "192.168.10.7" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
direction = "Stopped"
ultrasonicData = 0
cpu_temperature = 32
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    try:
        while 1:
            client, clientInfo = s.accept()
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                if data == b'forward\r\n':
                    PWM.setMotorModel(700,700,700,700)
                    print("forward")
                    direction = "Forward"
                elif data == b'reverse\r\n':
                    if( direction == "Forward" ):
                        PWM.setMotorModel(0,0,0,0)
                        direction = "Stopped"
                        print("Stopped")
                    else:
                        PWM.setMotorModel(-700,-700,-700,-700)
                        direction = "Reverse"
                        print("Reverse")
                elif data == b'left\r\n':
                    direction = "Turning Left"
                    PWM.setMotorModel(-2000, -2000, 2000, 2000)
                    print("Left")
                elif data == b'right\r\n':
                    PWM.setMotorModel(2000, 2000, -2000, -2000)
                    print("Right")
                    direction = "Turning Right"
                elif data == b'update\r\n':
                    
                    raw_cpu_temperature = subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp")
                    cpu_temperature = str(round(float(raw_cpu_temperature)/1000,2))
                    ultrasonicData = str(ultrasonic.get_distance())
            
                    dataToSend = f"{direction}-{ultrasonicData}-{cpu_temperature}"
                    client.sendall(dataToSend.encode())
    except Exception as e:
        print(e) 
        #print("Closing socket")
        #client.close()
        #s.close()
    finally:
        pass
