import sys
from packet_parser import parse

def compute(all_packets, node_ip):
    total_req_bytes_sent = 0
    total_req_bytes_received = 0 
    
    total_req_data_sent = 0 
    total_req_data_received = 0 

    total_requests_sent = 0
    total_requests_received = 0
	
    total_reply_sent = 0
    total_reply_received = 0
    
    request_times = {} #rtt
    rtts = []
    hop_counts = []  # List to collect hop counts
    
    
    print(f"Node IP: {node_ip}")
    for packet in all_packets:
        print(f"TYPE: {packet.get('type')} | SRC: {packet.get('source')} | DST: {packet.get('destination')}") 
        
        if packet["type"] == 8:  # Echo Request
            if packet["source"] == node_ip:
                total_requests_sent += 1
                total_req_bytes_sent += packet["length"]
                total_req_data_sent += (packet["length"] - 28)
                request_times[packet["seq_num"]] = packet["time"]   #save time
		if "ttl" in packet and packet["ttl"] is not None:
                #Used the value of 129.67 because the TTL for all the packets are ~128-130
                    hop_counts.append(129.67 - packet["ttl"])
            elif packet["destination"] == node_ip:
                total_requests_received += 1
                total_req_bytes_received += packet["length"]
                total_req_data_received += (packet["length"] - 28)
		if "ttl" in packet and packet["ttl"] is not None:
                #Used the value of 129.67 because the TTL for all the packets are ~128-130
                    hop_counts.append(129.67 - packet["ttl"])

        elif packet["type"] == 0:  # Echo Reply
            if packet["destination"] == node_ip:
                total_reply_received += 1
                if packet["seq_num"] in request_times:
                	rtt = (packet["time"] - request_times[packet["seq_num"]]) #add to the list
                	rtts.append(rtt)
            if packet["source"] == node_ip:
                total_reply_sent += 1

    print(f"Total requests sent: {total_requests_sent}")
    print(f"Total requests received: {total_requests_received}")
    print(f"Total replies sent: {total_reply_sent}")
    print(f"Total replies received: {total_reply_received}")
    print(f"Echo Request Bytes sent: {total_req_bytes_sent}")
    print(f"Echo Request Bytes received: {total_req_bytes_received}")
    print(f"Echo Request Data sent: {total_req_data_sent}")
    print(f"Echo Request Data received: {total_req_data_received}")
    
    if rtts:
    	average_rtt = (sum(rtts) / len(rtts)) * 1000
    else:
    	average_rtt = 0
    print(f"Average RTT (ms): {average_rtt:.2f}")
    # Calculates the average echo request hop counts 
    if hop_counts:
        avg_hop_count = sum(hop_counts) / len(hop_counts)
        print(f"Average Echo Request Hop Count: {avg_hop_count:.2f}")
    else:
        print("Average Echo Request Hop Count: N/A (no hop count data)")

def main():
    filtered_file = sys.argv[1]
    all_packets = parse(filtered_file)
	
    # Get the node number from command-line
    node_num = sys.argv[2]
    int_node_num = int(node_num)

    # Determine which 192.168.X00.X IP address block
    if int_node_num < 3:
        other_node_num = "1"
    else:
        other_node_num = "2"

    node_ip = "192.168." + other_node_num + "00." + node_num
    compute(all_packets, node_ip)

if __name__ == "__main__":
    main()
