import argparse
import os
import sys
from collections import Counter

from config import protocol_map, lookup_table_path


def parse_lookup_table(lookup_file_path: str) -> dict:
    """
    Parse lookup table from a txt file and create a dictionary mapping
    """
    lookup_table = {}
    try:
        with open(lookup_file_path, mode='r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                columns = line.split()
                if len(columns) < 3:
                    continue

                dstport = columns[0].strip()
                protocol = columns[1].strip().lower()
                tag = columns[2].strip()
                lookup_table[(dstport, protocol)] = tag

    except FileNotFoundError:
        print(f"Error: The file {lookup_file_path} was not found.")
        sys.exit(1)
    return lookup_table


def validate_flow_log_row(row: list[str]) -> bool:
    """
    Validates a single row of the flow log data.
    """
    if len(row) < 14:
        return False
    version = row[0].strip()
    if version != "2":
        return False
    action = row[12].strip().lower()
    if action != "accept":
        return False
    status = row[13].strip().lower()
    if status != "ok":
        return False
    protocol_num = row[7].strip()
    if protocol_num not in protocol_map:
        return False

    return True


def parse_flow_log_file(flow_log_file_path: str, lookup_table: dict) -> tuple[dict, dict]:
    tag_count_map = Counter()
    port_protocol_count_map = Counter()
    try:
        with open(flow_log_file_path, 'r') as file:
            for line in file:
                row = line.split()
                if not validate_flow_log_row(row):
                    continue

                dstport = row[6].strip()
                protocol_num = row[7].strip()
                protocol = protocol_map.get(protocol_num)
                tag = lookup_table.get((dstport, protocol), "Untagged")

                tag_count_map[tag] += 1
                port_protocol_count_map[(dstport, protocol)] += 1

    except FileNotFoundError:
        print(f"Error: The file {flow_log_file_path} was not found.")
        sys.exit(1)
    return tag_count_map, port_protocol_count_map


def write_output(output_file_path: str, tag_counts: dict, port_protocol_counts: dict) -> None:
    """
    Write the tag counts and port/protocol combination counts to an output file.
    """
    with open(output_file_path, 'w') as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")
        file.write("\n")

        file.write("Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("flow_log_file")
    args = parser.parse_args()
    flow_log_file = args.flow_log_file
    flow_log_file_path = os.path.join(os.path.dirname(__file__), flow_log_file)

    lookup_table = parse_lookup_table(lookup_table_path)
    tag_counts_map, port_protocol_counts_map = parse_flow_log_file(flow_log_file_path, lookup_table)

    output_file_name = f"output_{flow_log_file.replace("/", "_")}"
    output_file_path = os.path.join(os.path.dirname(__file__), "output", output_file_name)
    write_output(output_file_path, tag_counts_map, port_protocol_counts_map)
    print(f"Output written to {output_file_path}")


if __name__ == "__main__":
    main()
