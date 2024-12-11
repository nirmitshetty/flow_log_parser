import os

# Mapping of protocol numbers to protocol names
protocol_map = {
    "1": "icmp",
    "6": "tcp",
    "17": "udp",
    "41": "ipv6",
    "58": "icmpv6",
    "89": "ospf",
    "132": "sctp",
    "133": "fgs",
    "136": "pmtp",
    "255": "reserved"
}

# Path to the lookup table file
lookup_table_file_name = "sample_lookup_table.txt"
lookup_table_path = os.path.join(os.path.dirname(__file__), "input", lookup_table_file_name)
