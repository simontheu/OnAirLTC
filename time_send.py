import socket
from time import sleep

UDP_IP = "127.0.0.1"
UDP_PORT = 3310
#MESSAGE = b"10:30:00:00"

hours = 11
minutes = 59
seconds = 30
frames = 0

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

while 1:
	sleep(0.04)
	frames += 1
	if frames == 25:
		frames = 0
		seconds += 1
		if seconds == 60:
			seconds = 0
			minutes +=1
			if minutes == 60:
				minutes = 0
				hours += 1
				if hours == 24:
					hours = 0
	txt = "LTC_TIME:{:02d}:{:02d}:{:02d}:{:02d}"
	txt = txt.format(hours, minutes, seconds, frames)
	print(txt)
	sock.sendto(txt.encode('utf-8'), (UDP_IP, UDP_PORT))