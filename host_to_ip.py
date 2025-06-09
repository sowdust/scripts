# takes a list of hosts and prints out their ip addresses
import socket, sys

print_errors = False
infile = input('Hosts file: ')

with open(infile,'r') as inf:
	for line in inf:
		host = line.strip()
		try:
			print(socket.gethostbyname(host))
		except:
			if print_errors:
				print('[!] %s' % host)

