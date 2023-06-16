import hid
import time
import socket

LTCDevice = hid.Device(0x1dd2, 0x1033)

i = 8

max = 6733
min = 3218

mid = (max + min) / 2
haveHalfAOne = 0
bits = 0
while True:
	invalid = 0
	try:
		tcBytes =  LTCDevice.read(64)
	except:
		print(hid.enumerate())
		print("Device Unavailable")
		break
	txt = "{:08b} {:08b} {:08b} {:08b} {:08b} {:08b} {:08b} {:08b} {:08b} {:08b}"
	val = tcBytes[i+1] * 255 + tcBytes[i+0]
	#txt = "{:0d}"
	txt = txt.format(tcBytes[i+0], tcBytes[i+1], tcBytes[i+2],tcBytes[i+3],tcBytes[i+4],tcBytes[i+5],tcBytes[i+6],tcBytes[i+7],tcBytes[i+8],tcBytes[i+9])
	txt = txt.format(val)
	print(txt)
	continue
	if val > 4700:
		txt = "{:080b}"
		txt = txt.format(bits)
		print(txt)
		bits = bits >> 1
		bits = bits & 0xffffffffffffffffffff
		haveHalfAOne = 0
	else:
		if haveHalfAOne == 1:
			haveHalfAOne = 0
			txt = "{:080b}"
			txt = txt.format(bits)
			print(txt)
			bits = (bits >> 1) + 0x80000000000000000000
			bits = bits &        0xffffffffffffffffffff
		else:
			haveHalfAOne = 1
	if (bits >> 64) == 0xfcbc:
		print ("TC")
