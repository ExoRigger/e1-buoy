from pymodbus.client import ModbusSerialClient as ModbusClient

def run():
    client = ModbusClient(method="rtu",port="COM9",baudrate=19200,bytes=8,parity="E",stopbits=1)
    client.connect()
    r = client.read_holding_registers(0,44)
    print(r)


    client.close()





if __name__ == '__main__':
    while True:
        run()
    pass

