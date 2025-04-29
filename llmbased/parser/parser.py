import re
import json
import csv
import os
import sys
import argparse

def parse_simulation_data(folder_path, output_csv=None):
    """Parse simulation data from the specified folder"""
    # Construct paths to required files
    model_json_path = os.path.join(folder_path, "model.json")
    log_file_path = os.path.join(folder_path, "simulation.log")
    
    # Verify files exist
    if not os.path.exists(model_json_path):
        print(f"Error: model.json not found at {model_json_path}")
        return False
        
    if not os.path.exists(log_file_path):
        print(f"Error: simulation.log not found at {log_file_path}")
        return False
    
    # Set default output path if not specified
    if output_csv is None:
        output_csv = os.path.join(folder_path, "parsed_output.csv")
    
    # Load model.json and extract connections
    with open(model_json_path) as f:
        model = json.load(f)

    # Build connection map from model.jsonp
    connections = {}
    for conn in model["connections"]:
        from_comp, from_port = conn["from"].split(".")
        to_comp, to_port = conn["to"].split(".")
        connections[(from_comp, from_port)] = (to_comp, to_port)

    # Process simulation.log
    entries = []
    current_time = None
    current_model = None
    from_port = None

    with open(log_file_path) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        # Update current time
        time_match = re.match(r"__\s+Current Time:\s+([0-9.]+)", line)
        if time_match:
            current_time = time_match.group(1)

        # Detect internal transition model
        model_match = re.match(r"\s+INTERNAL TRANSITION in model <GeneratedModel\.(c\d)>", line)
        if model_match:
            current_model = model_match.group(1)

        # Detect output port
        port_match = re.match(r"\s+port <(out_\d+)>:", line)
        if port_match:
            from_port = port_match.group(1)

        # Match the next line with the value
        value_match = re.search(r"'con': 'c1, \d+, ([0-9.]+)'", line)
        if value_match and current_model and from_port and current_time:
            value = value_match.group(1)
            key = (current_model, from_port)
            if key in connections:
                to_comp, to_port = connections[key]
                entries.append([current_time, f"{current_model}.{from_port}", f"{to_comp}.{to_port}", value])

    # Save to CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "from", "to", "value"])
        writer.writerows(entries)

    print(f"{len(entries)} entries written to {output_csv}")
    return True

if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Parse PyDEVS simulation logs to CSV')
    parser.add_argument('folder_path', help='Path to the folder containing model.json and simulation.log')
    parser.add_argument('--output', '-o', help='Path to save the output CSV (default: <folder_path>/parsed_output.csv)')
    
    args = parser.parse_args()
    
    # Run the parser with the provided arguments
    parse_simulation_data(args.folder_path, args.output)