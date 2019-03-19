#!/usr/bin/python3

import socket
import sys
import argparse
import miio.philips_bulb

ip = [] # list of known IPs
device = [] # list of known devices

def server():
	# init server
	host = socket.gethostname()
	port = 8181
	s = socket.socket()
	s.bind((host, port))
	s.listen(1)
	print("Miio server ready.")
	
	while True:
		i=0
		# get args
		client, addr = s.accept()
		argsString = client.recv(1024).decode('utf-8')

		if not argsString:
			break
		# passed args to sys.argv for analysis
		sys.argv = argsString.split(';') 

		print(sys.argv)

		parser = argparse.ArgumentParser(description='Script which comunicate with PhilipsBulb.')
		parser.add_argument('IPaddress', help='IP address of PhilipsBulb' )
		parser.add_argument('token', help='token to login to device')
		parser.add_argument('--level', type=int, help='choose level')
		parser.add_argument('--temp', type=int, help='choose White Temp')
		parser.add_argument('--power', help='power ON/OFF')
		parser.add_argument('--debug', action='store_true', help='if define more output is printed')
		parser.add_argument('--scene', type=int, help='choose scene')
		# --brightemp = set_brightness_and_color_temperature()
		parser.add_argument('--brightemp', type=str, help='choose Brightness and White Temp')
		parser.add_argument('--closeServer') #debug

		args = parser.parse_args()
		
		# DEBUG : add this arg to stop the server
		if args.closeServer:
			break

		# check if device is known, else create a new one
		try:
			deviceId = ip.index(args.IPaddress)
			
		except ValueError:
			deviceId = len(ip)
			device.append(miio.philips_bulb.PhilipsBulb(args.IPaddress, args.token))
			ip.append(args.IPaddress)
			print("New light added : " + args.IPaddress)

		# process existing args
		if args.level:
			try:
				device[deviceId].set_brightness(args.level)
			except:
				print("Cannot reach device : " + args.IPaddress)
		
		if args.temp:
			try:
				device[deviceId].set_color_temperature(args.temp)
			except:
				print("Cannot reach device : " + args.IPaddress)
		
		if args.brightemp:
			#print(args.brightemp)
			brightness = args.brightemp[:args.brightemp.find(",")]
			#print("brightness is " + brightness)
			cct = args.brightemp[args.brightemp.find(",") + 1 :]
			#print("cct is " + cct)
			try:
				device[deviceId].set_brightness_and_color_temperature(int(brightness), int(cct))
			except:
				print("Cannot reach device : " + args.IPaddress)
		
		if args.scene:
			try:
				device[deviceId].set_scene(args.scene)
			except:
				print("Cannot reach device : " + args.IPaddress)
		
		if args.power:
			if args.power == "ON":
				try:
					device[deviceId].on()
				except:
					print("Cannot reach device : " + args.IPaddress)
			elif args.power == "OFF":
				try:
					device[deviceId].off()
				except:
					print("Cannot reach device : " + args.IPaddress)


		# send device status to client
		try:
			deviceStatus = device[deviceId].status()
		except:
			deviceStatus = "Cannot reach device" + args.IPaddress

		client.send(str(deviceStatus).encode('utf-8'))

	client.close()

server()