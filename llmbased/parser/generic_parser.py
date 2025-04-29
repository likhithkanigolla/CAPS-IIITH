# generic_parser.py
import re
import json
from collections import defaultdict

class PyDEVSSimulationParser:
    def __init__(self, log_path):
        self.log_path = log_path
        self.components = defaultdict(lambda: {"type": None, "transitions": [], "connections": set()})
        self.current_time = 0.0
        self.current_component = None

    def parse(self):
        with open(self.log_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            self.extract_time(line)
            self.extract_initialization(line)
            self.extract_transition(line)
            self.extract_data_flow(line)
            self.extract_connection(line)

        # Convert sets to lists for JSON serialization
        for comp in self.components.values():
            comp['connections'] = list(comp['connections'])

        return dict(self.components)

    def extract_time(self, line):
        time_match = re.search(r"Current Time:\s+(\d+\.\d+)", line)
        if time_match:
            self.current_time = float(time_match.group(1))

    def extract_initialization(self, line):
        init_match = re.search(r"INITIAL CONDITIONS in model <(.+?)>", line)
        if init_match:
            component = init_match.group(1).split('.')[-1]
            self.components[component]['type'] = 'model'

    def extract_transition(self, line):
        if "INTERNAL TRANSITION" in line or "EXTERNAL TRANSITION" in line:
            transition_type = "internal" if "INTERNAL" in line else "external"
            comp_match = re.search(r"model <(.+?)>", line)
            if comp_match:
                self.current_component = comp_match.group(1).split('.')[-1]
                self.components[self.current_component]['transitions'].append({
                    "type": transition_type,
                    "time": self.current_time
                })

    def extract_data_flow(self, line):
        # Match multiple types of data output
        if "Sending data:" in line or "Sending command:" in line or "outputFnc called. Sending data:" in line:
            data_match = re.search(r"Sending (data|command): (\{.*\})", line)
            if not data_match:
                data_match = re.search(r"Sending data: (\{.*\})", line)
            if not data_match:
                data_match = re.search(r"outputFnc called\. Sending data: (\{.*\})", line)
            if data_match:
                raw = data_match.group(2)
                try:
                    data = json.loads(raw.replace("'", '"'))
                except json.JSONDecodeError:
                    data = raw

                if self.current_component:
                    self.components[self.current_component]['transitions'].append({
                        "type": "send",
                        "time": self.current_time,
                        "data": data
                    })

        if "Received data:" in line:
            data_match = re.search(r"Received data: (\{.*\})", line)
            if data_match:
                raw = data_match.group(1)
                try:
                    data = json.loads(raw.replace("'", '"'))
                except json.JSONDecodeError:
                    data = raw
                if self.current_component:
                    self.components[self.current_component]['transitions'].append({
                        "type": "receive",
                        "time": self.current_time,
                        "data": data
                    })

    def extract_connection(self, line):
        connection_match = re.search(r"Connecting (\w+) to (\w+)", line)
        if connection_match:
            source, target = connection_match.groups()
            self.components[source]['connections'].add(target)
            self.components[target]['connections'].add(source)

if __name__ == '__main__':
    import sys
    parser = PyDEVSSimulationParser(sys.argv[1])
    output = parser.parse()
    print(json.dumps(output, indent=2))