import serial
import time
global DEBUG
import math
DEBUG=True

def generate_checksum(message):
	lrc = 0xFF
	for b in message:
		lrc ^= ord(b)
	return lrc

class Manager():
	def __init__(self):
		self.ser=serial.Serial()
		self.ser.port="/dev/tty.SLAB_USBtoUART"
		self.ser.baudrate=115200
		self.ser.open()
		if DEBUG:
			print self.ser
	def send(self, message):
		chksum = generate_checksum("".join(message))
		message="".join(message)
		message="\x01"+message+chr(chksum)
		if DEBUG:
			self.print_message(message, "-->")
		assert self.ser.write(message) == len(message)
		assert self.read_ack() == chr(6)
		self.read_msg()
		self.send_ack()
		time.sleep(0.02)
	def print_message(self, msg, prefix):
		print prefix + ":".join("{0:x}".format(ord(c)) for c in msg)
	def read_msg(self):
		som = self.ser.read()
		length = ord(self.ser.read())
		msg = self.ser.read(length)
	   	if DEBUG:
			self.print_message(msg, "<--")
		return msg
	def read_ack(self):
		ack = self.ser.read()
		if DEBUG:
	   		self.print_message(ack, "<--")
		return ack
	def send_ack(self):
		ack = chr(6)
		self.ser.write(ack)
		if DEBUG:
			self.print_message(ack, "-->")
	def setNode(self, node, value):
		assert value<=100 or value>=0
		value=value*2.56
		value=int(value)
		if value>255: value=255
		self.send(["\x09","\x00", "\x13", chr(node),"\x03","\x20","\x01",chr(value),"\x05"])
if __name__=="__main__":
	m = Manager()
	m.setNode(5, 255)