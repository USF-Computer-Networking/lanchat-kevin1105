import sys
import socket
import select
from sys import argv
from scapy.all import *
import builtins


def help():
	print("LAN requires the user to enter a network interface and an IP. " +
		"The UDP Chat supports broadcast." + " q is to quit" + " h is for help " + "L is for LAN " + " u is for UDP \n")

def getLine():
	m, x, y = select.select([sys.stdin],[],[], 0.0001)
	for s in m:
		if s == sys.stdin:
			inputs = sys.stdin.readline()
			return inputs
	return False
		
def lan():
	print("\n**********")
	print("\n   LAN")
	print("\n**********")
	
	# if error keep going
	while (True):
		try:
			interface = raw_input("Interface: ")
			ip = raw_input("Ip: ")

			if interface == "q":
				return
			if ip == "q":
				return
			
			print("\n Scanning*** ")

			# to start scanning
			conf.verb = 0

			ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ip), timeout = 2, iface = interface, inter = 0.1)

			# print results
			print("\n MAC Address - IP Address")
			for send, recv in ans:
				print(recv.sprintf(r"%Ether.src% - %ARP.psrc%"))
			print("\n Scan Completed")

		# Interface not found
		except IOError:
			print("Interface Not Found\n")
			continue

		# Delete or crtl + c
		except KeyboardInterrupt:
			print("\nLAN is shutting down ")
			break

	print("End of scan")


def udp():
	print("\n*********")
	print("\n   UDP")
	print("\n*********")
	
	print("\nSpace Enter for default port" )
	number = raw_input("\nConnect to Port Number: ")
	if number == " ":
		number = "1027"

	port = int(number, 16)
	send_Address = ('<broadcast>', port)
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.setblocking(False)
	sock.bind(('', port))

	print("\nPress 'ctrl + c' to exit")
	print("Connecting to port", hex(port))
	print("You can start typing\n")

	while (True):
		try:
			message, address = sock.recvfrom(5000)
			message = message.strip("\n")
			if message:
				print(address, "->", message)
		except:
			pass
	 	
		message = getLine();
		if message != False:
			sock.sendto(message, send_Address)

def main():
	while True:
		try:
			choice = raw_input("LAN (L), UDP (u), Help (h), Quit(q) : ").lower().strip()
			if choice == "l":
				lan()
			elif choice == "u":
				udp()
			elif choice == "h":
				help()
			elif choice == "q":
				break
			else:
				print("Invalid input")

		except:
			break

	print("\nProgram is shutting down ")
	
main()