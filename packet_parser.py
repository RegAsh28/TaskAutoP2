import sys

# Helper funtion for main filtered_file function.
def parse_fields(line):
	
	# Interact with the individual fields
	split_fields = line.split()
	
	fields = {}
	
	# Note: split_fields[0] is just packet no. so we don't need it.
	fields["time"] = float(split_fields[1])
	fields["source"] = split_fields[2]
	fields["destination"] = split_fields[3]
	# Note: split_fields[4] is ICMP...we know this already.
	fields["length"] = int(split_fields[5])
	
	# Check if this is request or reply (determines type #)
	lower_line = line.lower()
	if "request" in lower_line:
		fields["type"] = 8
	else:
		fields["type"] = 0
		
	# Get sequence num
	if "seq" in line:
		# This breaks the line into two parts, and index[1] gets us the second part (the seq info).
		only_seq_part = line.split("seq=")[1]
		seq_num = only_seq_part.split("/")[0]
		fields["seq_num"] = int(seq_num)
	
	return fields
	
	

def parse(filtered_file) :
	
	# The approach for this is to read in the filtered file from Phase 1 and then store each packet as a dictionary, and then store all dictionarires (packets) in a list. 
	# We are using dictionaries because that will let us match field names to value (e.g. the key is time Source IP and the value is 192.168.#.#). Easier to extract info that way.
	
	all_packets = []
	
	with open(filtered_file, 'r') as f:
		lines = f.readlines()
	
	i = 0
	total_packets = len(lines)
	# This is saying "While we have lines to look at, let's look at each one individually.
	while i < total_packets:
	
		line = lines[i]	
		line = line.strip() # Needed to add strip() bc some of the hex lines have weird white spacing.
		
		# Now let's make each packet.
		# This tells us if it is a header
		if "ICMP" in line:
			#print(line)
			packet = {}
			packet.update(parse_fields(line))
			
			hex_lines = []	
			# Go to next line (first hex line)
			i += 1
		
			# This while loop prepares all the hex lines to be added (since we have to cover multiple lines)
			while i < total_packets and "ICMP" not in lines[i]:
				hex_line = lines[i].strip()
				if hex_line != "":
					hex_lines.append(hex_line)
				i+=1
				
			packet["hex_lines"] = hex_lines
			
			all_packets.append(packet)
			
		else:
			i += 1
	
	# Keeping this here as reference of how this stuff will be interacted with.
	# print(all_packets[44])
	# for packet in all_packets:
	#	print(packet["source"])
	return all_packets
			
		
		
		
		
def main():

	filtered_output_file = sys.argv[1]
	parse(filtered_output_file)
	
main()

	
