import sys
from packet_parser import parse

def compute(all_packets, node_ip):
	total_requests = 0
	
	for packet in all_packets:
		if packet["type"] == 8:
			if packet["source"] == node_ip:
				total_requests += 1
	
	print(f"Total requests: {total_requests}")
	

def main():
	
	filtered_file = sys.argv[1]
	all_packets = parse(filtered_file)
	
	# Get the IP for the node:
	node_num = sys.argv[2]
	
	if node_num < 3:
		other_node_num = 1
	else:
		other_node_num = 2
	node_ip = "192.168." + other_node_num + "00." + node_num
	
	compute(all_packets, node_ip)

	
main()
	 
