import serial
import time
import numpy as np

def test_checkfun():
    testmessage=b"\xFF\x40\x14\x03\xC8\x00\x22\x00\x78\x00\x37\x00\x18\x00\x20\x07\xD0\x02\xA2\x01\x65\xF7"
    #the line below implements the  FucCheckSum function from the manual in Python
    cvaltest=((((sum(testmessage[1:-1]))%256)^0b11111111)+1)%256
    #alternative implementation using numpy
    # cval=~np.uint8((sum(message[1:-1])+1)%256)+1
    if cvaltest != testmessage[-1]:
        print("Error Checkbyte does not match")
        return False
    return True

def get_temp_celsius(message):
    return (message[17]*256+message[18]-500)/10


def get_rel_humid(message):
    return (message[19]*256+message[20])/10


gas_order=["CO","SO2","O3","NO2","PM2.5","PM10"]

def get_gas_ug_pm3(message,startbyte):
    return message[startbyte]*256+message[startbyte+1]


def get_data(message,strict=True):
    ln=22
    if message[0] != 0xff:
        print("Error First message byte is not 0xff")
        return {}
    
    #the line below implements the  FucCheckSum function from the manual in Python
    cval=((((sum(message[1:-1]))%256)^0b11111111)+1)%256
    checkbyte=message[ln-1]
    if cval != checkbyte:
        if strict:
            print(f"Error: Checkbyte does not match {hex(cval)}")
            return {}
        checkfail=True
    else:
        checkfail=False
        # else:
            # print(f"Warning: possible data corruption: checksum {hex(cval)} does not match {hex(checkbyte)}")
    data={"temp_celsius":get_temp_celsius(message), "humidity_rel":get_rel_humid(message)}
    for i,gas in enumerate(gas_order):
        data[gas]=get_gas_ug_pm3(message,i*2+3)
    data['checkfail']=checkfail

    return data 

def test_readfromfile():
    test_checkfun() #just for testing purposes
    nlog=30
    messagelen=22
    flog=f"testserialdata_{messagelen}.bin"
    with open(flog,'rb') as fid:
        for i in range(nlog):
            message=fid.read(messagelen)
            print(message.hex())
            data=get_data(message,False)
            print(data)

def open_serial(dev="/dev/serial",baud=9600):
    ser=serial.Serial(dev,baud)
    return ser

def test_log_to_file():
    ser=open_serial()
    nlog=30
    messagelen=22
    flog=f"testserialdata_{messagelen}.bin"
    with open(flog,'wb') as fid:
        i=0
        while True:
            i+=1
            if i > nlog:
                break
            message=ser.read(messagelen)
            fid.write(message)


def main():
    ser=open_serial()
    messagelen=22
    while True:
        message=ser.read(messagelen)
        data=get_data(message)
        print(data)


if __name__ == "__main__":
    #test_log_to_file()
    #test_readfromfile()

    #actual main function reads from serial port
    main()

