from netaddr import *

infile = 'netblocks_from_ripe.txt'


with open(infile,'r') as inf:
	for line in inf:
		line = line.replace(' ','')
		if('-') in line:
			ips = line.split('-')
			ip_list = list(iter_iprange(ips[0], ips[1]))
		else:
			ip_list = IPNetwork(line)
		for addr in ip_list:
			print(addr)
