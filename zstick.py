import serial
import time

ser = serial.Serial()
ser.port="/dev/tty.SLAB_USBtoUART" # "/dev/ttyUSB0"
ser.baudrate=115200
ser.open()

print ser

def generate_checksum(message):
    lrc = 0xFF
    for b in message:
        lrc ^= ord(b)
    return lrc

def print_message(msg, prefix):
    print prefix + ":".join("{0:x}".format(ord(c)) for c in msg)

def read_ack(ser):
    ack = ser.read()
    print_message(ack, "<--")
    return ack

def send_ack(ser):
    ack = chr(6)
    ser.write(ack)
    print_message(ack, "-->")

def read_msg(ser):
    som = ser.read()
    len = ord(ser.read())
    msg = ser.read(len)
    print_message(msg, "<--")
    return msg

def send(ser, message):
    chksum = generate_checksum(message)
    message = chr(1) + message + chr(chksum)
    print_message(message, "-->")
    assert ser.write(message) == len(message)
    assert read_ack(ser) == chr(6)
    read_msg(ser)
    send_ack(ser)
    time.sleep(0.02)

def send_node_on_off(ser, node_id, on_off):
    message = "\x09\x00\0x13"
    message += chr(node_id)
    message += "\x03\x20\x01"
    message += chr(0xFF if on_off else 0x00)
    message += chr(1 | 4)  # ACK | AUTO_ROUTE
    send(ser, message)

send(ser, "\x09\x00\x13\x04\x03\x20\x01\xFF\x05")
send(ser, "\x09\x00\x13\x02\x03\x20\x01\x00\x05")
send(ser, "\x09\x00\x13\x05\x03\x20\x01\x00\x05")

time.sleep(3)

send(ser, "\x09\x00\x13\x04\x03\x20\x01\x00\x05")
send(ser, "\x09\x00\x13\x02\x03\x20\x01\xFF\x05")
send(ser, "\x09\x00\x13\x05\x03\x20\x01\xFF\x05")
