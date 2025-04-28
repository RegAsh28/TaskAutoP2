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

    sent_request_times = []  # For Goodput and Throughput (only Echo Requests Sent)
    request_times = {}       # For RTT matching
    rtts = []
    hop_counts = []          # List to collect hop counts

    received_request_times = {}  # NEW 
    reply_delays = []            # NEW 

    print(f"Using Node IP: {node_ip}")

    for packet in all_packets:
        print(f"TYPE: {packet.get('type')} | SRC: {packet.get('source')} | DST: {packet.get('destination')}")

        if packet["type"] == 8:  # Echo Request
            if packet["source"] == node_ip:
                total_requests_sent += 1
                total_req_bytes_sent += packet["length"]
                total_req_data_sent += (packet["length"] - 28)  # Correct: 28 header bytes
                request_times[packet["seq_num"]] = packet["time"]
                sent_request_times.append(packet["time"])
                if "ttl" in packet and packet["ttl"] is not None:
                    hop_counts.append(129.67 - packet["ttl"])
            elif packet["destination"] == node_ip:
                total_requests_received += 1
                total_req_bytes_received += packet["length"]
                total_req_data_received += (packet["length"] - 28)
                if "ttl" in packet and packet["ttl"] is not None:
                    hop_counts.append(129.67 - packet["ttl"])
                received_request_times[packet["seq_num"]] = packet["time"]  # FIXED indent and name NEW

        elif packet["type"] == 0:  # Echo Reply
            if packet["destination"] == node_ip:
                total_reply_received += 1
                if packet["seq_num"] in request_times:
                    rtt = (packet["time"] - request_times[packet["seq_num"]])
                    rtts.append(rtt)
            if packet["source"] == node_ip:
                total_reply_sent += 1
                if packet["seq_num"] in received_request_times:  #NEW 
                    delay = (packet["time"] - received_request_times[packet["seq_num"]]) #NEW
                    reply_delays.append(delay) #NEW

    # ---- Final Metrics ----
    print("\n---- Final Metrics ----")
    print(f"Total Requests Sent: {total_requests_sent}")
    print(f"Total Requests Received: {total_requests_received}")
    print(f"Total Replies Sent: {total_reply_sent}")
    print(f"Total Replies Received: {total_reply_received}")
    print(f"Echo Request Bytes Sent: {total_req_bytes_sent}")
    print(f"Echo Request Bytes Received: {total_req_bytes_received}")
    print(f"Echo Request Data Sent: {total_req_data_sent}")
    print(f"Echo Request Data Received: {total_req_data_received}")

    print(f"Number of Echo Requests Sent Recorded: {len(sent_request_times)}")

    # Average RTT
    if rtts:
        average_rtt = (sum(rtts) / len(rtts)) * 1000  # Convert to milliseconds
    else:
        average_rtt = 0
    print(f"Average RTT (ms): {average_rtt:.2f}")

    # Average Hop Count
    if hop_counts:
        avg_hop_count = sum(hop_counts) / len(hop_counts)
        print(f"Average Echo Request Hop Count: {avg_hop_count:.2f}")
    else:
        print("Average Echo Request Hop Count: N/A (no hop count data)")

    # Goodput and Throughput Calculation
    if sent_request_times:
        first_request_time = min(sent_request_times)
        last_request_time = max(sent_request_times)
        total_request_time = last_request_time - first_request_time
        print(f"First Sent Request Time: {first_request_time}")
        print(f"Last Sent Request Time: {last_request_time}")
        print(f"Total Request Time (seconds): {total_request_time}")
    else:
        total_request_time = 1  # prevent divide-by-zero

    goodput = (total_req_data_sent / total_request_time) / 1000  # kB/sec
    throughput = (total_req_bytes_sent / total_request_time) / 1000  # kB/sec

    print(f"Echo Request Goodput (kB/sec): {goodput:.1f}")
    print(f"Echo Request Throughput (kB/sec): {throughput:.1f}")

    # Average Reply Delay (microseconds) NEW
    if reply_delays:
        average_reply_delay = (sum(reply_delays) / len(reply_delays)) * 1_000_000  # convert to microseconds
    else:
        average_reply_delay = 0
    print(f"Average Reply Delay (microseconds): {average_reply_delay:.2f}") #NEW, End of reply delay

    print("------------------------\n")

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
