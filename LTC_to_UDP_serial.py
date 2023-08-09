
import serial
import time
import socket


UDP_IP = "127.0.0.1" #Self
UDP_PORT = 3310 # OnAirScreen API Port

lastHours = 0;
lastMins = 0;
lastSeconds = 0;
lastFrames = 0;
frameRate = 10;#Stops a div by zero error
ticksAtFrameRate = 0;
ticks = 0;
firstRun = 1;

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #IP and UDP

try:
	serialDevice = serial.Serial('/dev/ttyACM0', timeout=10)
	#serialDevice = serial.Serial('/dev/tty.usbmodem11101', timeout=10)

except:
	print ("Unable to connect to serial device")
	quit()


print ("Connected to: " + serialDevice.name)

tcBytesRead = 0
currentByte = 0
tcBytes = [0,0,0,0,0,0,0]

goodFrames = 0

def decodeTC(hours, mins, seconds, frames, FPS):
	global frameRate
	global lastMins
	global lastHours
	global lastSeconds
	global lastHours
	global goodFrames
	global firstRun
	invalid = 0
	if firstRun != 1:
		if (frames >= frameRate):
			frameRate = frames + 1
		if (hours > 23 or mins > 59 or seconds > 59):
			print ("invalid time")		

		if (frames == frameRate):
			ticksAtFrameRate += 1

		if (hours != lastHours and ((hours != (lastHours + 1) % 24) and mins != 0)):
			print ("invalid time hours")
			invalid = 1
			goodFrames  = 0
		if (mins != lastMins and ((hours != (lastMins + 1) % 60) and seconds != 0)):
			print ("invalid time mins")
			invalid = 1
			goodFrames = 0
		if (seconds != lastSeconds and ((seconds != (lastSeconds + 1) % 60) and frames != 0)):
			print ("invalid time seconds", seconds)
			invalid = 1
			goodFrame = 0


	lastHours = hours
	lastMins = mins
	lastSeconds = seconds

<<<<<<< Updated upstream
	if (invalid != 1): 
=======
	if (invalid != 1) and frames == 0: #Send only seconds
>>>>>>> Stashed changes
		lastSeconds = seconds
		#Send Time Out
		txt = "LTC_TIME:{:02d}:{:02d}:{:02d}:{:02d}"
		txt = txt.format(hours, mins, seconds, frames)
		print(txt, goodFrames)
		sock.sendto(txt.encode('utf-8'), (UDP_IP, UDP_PORT))

	if (invalid != 1):
		goodFrames += 1
	time.sleep((1/frameRate)/2)
	firstrun = 0



#build bytes
sync_state = 0

while True:
	tcByte = serialDevice.read()
#	print(currentByte, tcByte.hex())

	if sync_state == 2:
		tcBytes[currentByte] = tcByte
		currentByte += 1
		
	if sync_state == 2 and currentByte == 5:
		decodeTC(int.from_bytes(tcBytes[0],"little"),int.from_bytes(tcBytes[1],"little"),int.from_bytes(tcBytes[2],"little"),int.from_bytes(tcBytes[3],"little"),int.from_bytes(tcBytes[4],"little"))
		currentByte = 0;

	if (sync_state == 0 and int.from_bytes(tcByte,"little") == 0x55):
		sync_state = 1
		currentByte = 0
	elif (sync_state == 1 and int.from_bytes(tcByte,"little") == 0xaa):
		sync_state = 2
		currentByte = 0
	elif sync_state == 2 and (int.from_bytes(tcByte,"little") == 0x55 or int.from_bytes(tcByte, "little") == 0xaa):
		currentByte = 0
#	print(tcBytes, sync_state)
	if currentByte == 5:
		currentByte = 0

