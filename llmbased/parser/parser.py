import re
import json
import csv

# Load model.json and extract connections
with open("model.json") as f:
    model = json.load(f)

# Build connection map from model.json
connections = {}
for conn in model["connections"]:
    from_comp, from_port = conn["from"].split(".")
    to_comp, to_port = conn["to"].split(".")
    connections[(from_comp, from_port)] = (to_comp, to_port)

# Process simulation1.log
log_file = "simulation1.log"
entries = []
current_time = None
current_model = None
from_port = None

with open(log_file) as f:
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
csv_path = "parsed_output.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "from", "to", "value"])
    writer.writerows(entries)

print(f"{len(entries)} entries written to {csv_path}")
