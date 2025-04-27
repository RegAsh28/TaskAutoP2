import sys

# Needs the node_num parameter to prevent overwriting "output.txt" file.
def filter(node_txt, node_num) :
	
	# The project wants us to read in the .txt file for some reason even though the pcap file would be easier to use. Oh well.
	
	output = f"output{node_num}.txt"
		
	with open(node_txt, 'r') as f:
		packets = f.readlines()
	
	with open(output, 'w') as output:
		
		i = 0
		
		total_packets = len(packets)
		# Iterate for as many packets as node_txt contains.
		while i < total_packets:
		
			line = packets[i]
			if "ICMP"  in line:
				if "request" in line or "reply" in line:
					output.write(line)
					i += 1
					# This while loop gets the hex info, will be used later. Needed to do this as a loop to adapt to different packet sizes and increment 'i' accordingly.
					while i < total_packets and not packets[i].startswith("No."):
						output.write(packets[i])
						i += 1
				else:
					i += 1
			else:
				i += 1
				
				
		
	
def main():
	file = sys.argv[1]
	node_number = sys.argv[2]
	filter(file, node_number)
	
main()
