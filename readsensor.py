import serial
import time

def checkfunc(n):
    return (1 << 8)-n

def messageok(message):
    ln=len(message)
    checkbyte=message[ln-1]
    valbyte=checkfunc(sum(message[1:-1]))
    
    breakpoint()



def main():
    #dev="/dev/ttyAMA0"
    dev="/dev/serial0"
    baud=9600
    ser=serial.Serial(dev,baud)
    nlog=30
    messagelen=20
    flog=f"testserialdata_{messagelen}.bin"
    with open(flog,'wb') as fid:
        i=0
        while True:
            i+=1
            if i > nlog:
                break
            message=ser.read(messagelen)
            fid.write(message)
            time.sleep(0.9)
            #if not messageok(message):
            #breakpoint()

    print(message)



if __name__ == "__main__":
    main()

