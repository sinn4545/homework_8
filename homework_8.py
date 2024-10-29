import threading
import serial
import RPi.GPIO as GPIO


PWM = [ 18, 23 ]
AIN = [ 22, 27 ]
BIN = [ 25, 24 ]

#cmd = ["go", "back", "left", "right", "stop"]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

gData = ""
for i in range(0, 2) :
    GPIO.setup(PWM[i], GPIO.OUT)
    GPIO.setup(AIN[i], GPIO.OUT)
    GPIO.setup(BIN[i], GPIO.OUT)


L_Motor = GPIO.PWM(PWM[0], 500)
L_Motor.start(0)
R_Motor = GPIO.PWM(PWM[1], 500)
R_Motor.start(0)

def serial_thread() :
    global gData
    while True :
        data = bleSerial.readline()
        data = data.decode()
        gData = data

def motor_direction(data) :
    if data != 4 :
        L_Motor.ChangeDutyCycle(50)
        R_Motor.ChangeDutyCycle(50)

        for j in range(0, 2) :
            GPIO.output(AIN[j], j if data in [0, 1] else 1 - j)
            GPIO.output(BIN[j], j if data in [0, 2] else 1 - j)
    
    else :
        L_Motor.ChangeDutyCycle(0)
        R_Motor.ChangeDutyCycle(0)
    

def main() :
    global gData
    dirNum = 4
    try :
        while True :
            if gData.find("go") >= 0 :
                gData = ""
                dirNum = 0
                print("ok go")

            elif gData.find("right") >= 0 :
                gData = ""
                dirNum = 1
                print("ok right")

            elif gData.find("left") >= 0 :
                gData = ""
                dirNum = 2
                print("ok left")

            elif gData.find("back") >= 0 :
                gData = ""
                dirNum = 3
                print("ok back")
            
            elif gData.find("stop") >= 0 :
                gData = ""
                dirNum = 4
                print("ok stop")
            
            motor_direction(dirNum)
            
    except KeyboardInterrupt :
        pass

if __name__ == '__main__' :
    task1 = threading.Thread(target=serial_thread)
    task1.start()
    main()
    bleSerial.close()

GPIO.cleanup()