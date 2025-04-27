import sys
from packet_parser import parse

def compute(all_packets, node_ip):
	total_requests_sent = 0
	total_reply_received = 0
	
	print(f"Node IP: {node_ip}")
	for packet in all_packets:
		print(f"TYPE: {packet.get('type')} | SRC: {packet.get('source')} | DST: {packet.get('destination')}") 
		if packet["type"] == 8:
			if packet["source"] == node_ip:
				total_requests_sent += 1
		elif packet["type"] == 0:
			if packet["destination"] == node_ip:
				total_reply_received += 1
	
	print(f"Total requests sent: {total_requests_sent}")
	print(f"Total replies received: {total_reply_received}")
	

def main():
	
	filtered_file = sys.argv[1]
	all_packets = parse(filtered_file)
	
	# Get the IP for the node:
	node_num = sys.argv[2]
	
	int_node_num = int(node_num)
	if int_node_num < 3:
		other_node_num = "1"
	else:
		other_node_num = "2"
	node_ip = "192.168." + other_node_num + "00." + node_num
	
	
	compute(all_packets, node_ip)

	
main()
	 
