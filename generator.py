import os
import sys
import xml.etree.ElementTree as ET
import datetime
import shutil
from parse_connections import parse_connections
import traceback

# Enable debug mode - set to True for detailed debug output
DEBUG = True

def debug_print(message):
    """Print debug messages when DEBUG is enabled"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def extract_components(saml_file_path=None, hwml_file_path=None):
    """Extract component information from both SAML and HWML files."""
    debug_print(f"Starting component extraction - SAML: {saml_file_path}, HWML: {hwml_file_path}")
    namespaces = {
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'components': 'components',
        'filesystem': 'filesystem'
    }
    
    components = []
    
    # Process SAML file if provided
    if saml_file_path and os.path.exists(saml_file_path):
        try:
            debug_print(f"Parsing SAML file: {saml_file_path}")
            tree = ET.parse(saml_file_path)
            root = tree.getroot()
            
            if root.find('./SAElements', namespaces) is not None:
                debug_print("Found SAElements in SAML file")
                
                # Count elements for debugging
                element_count = len(root.findall('./SAElements', namespaces))
                debug_print(f"Found {element_count} SAElements")
                
                for i, element in enumerate(root.findall('./SAElements', namespaces)):
                    element_type = element.get(f'{{{namespaces["xsi"]}}}type')
                    debug_print(f"Element {i} type: {element_type}")
                    
                    if element_type and 'Component' in element_type:
                        component_name = element.get('name')
                        debug_print(f"Found component: {component_name}")
                        
                        # Extract ports
                        in_ports = []
                        out_ports = []
                        for j, port in enumerate(element.findall('./ports', namespaces)):
                            port_type = port.get(f'{{{namespaces["xsi"]}}}type', '')
                            debug_print(f"  Port {j} type: {port_type}")
                            if "InMessagePort" in port_type:
                                in_ports.append(j)
                            elif "OutMessagePort" in port_type:
                                out_ports.append(j)
                        
                        debug_print(f"  In ports: {in_ports}, Out ports: {out_ports}")
                        
                        # Extract behavior if available
                        behaviors = []
                        for mode in element.findall('./modes', namespaces):
                            debug_print(f"  Found mode for {component_name}")
                            for behavior in mode.findall('./behaviouralElements', namespaces):
                                behavior_type = behavior.get(f'{{{namespaces["xsi"]}}}type', '')
                                behavior_name = behavior.get('name', '')
                                debug_print(f"    Behavior: {behavior_name} (Type: {behavior_type})")
                                if behavior_type:
                                    behaviors.append({
                                        'type': behavior_type.split(':')[-1],
                                        'name': behavior_name
                                    })
                        
                        component_type = 'sensor' if 'Sensor' in component_name else \
                                        'actuator' if 'Actuator' in component_name else \
                                        'interface' if 'Interface' in component_name else \
                                        'controller'
                        
                        debug_print(f"  Identified as: {component_type}")
                        
                        components.append({
                            'name': component_name,
                            'type': component_type,
                            'in_ports': in_ports,
                            'out_ports': out_ports,
                            'behaviors': behaviors,
                            'source': 'saml'
                        })
        except Exception as e:
            print(f"Error extracting components from SAML file: {str(e)}")
            debug_print(f"SAML parsing error details: {traceback.format_exc()}")
    
    # Process HWML file if provided
    if hwml_file_path and os.path.exists(hwml_file_path):
        try:
            debug_print(f"Parsing HWML file: {hwml_file_path}")
            tree = ET.parse(hwml_file_path)
            root = tree.getroot()
            
            if root.find('./nodes', namespaces) is not None:
                debug_print("Found nodes in HWML file")
                
                # Count nodes for debugging
                node_count = len(root.findall('./nodes', namespaces))
                debug_print(f"Found {node_count} nodes")
                
                for node in root.findall('./nodes', namespaces):
                    node_name = node.get('name')
                    protocol = node.get('macProtocol', 'Unknown')
                    routing = node.get('routingProtocol', 'Unknown')
                    debug_print(f"Found node: {node_name}, Protocol: {protocol}, Routing: {routing}")
                    
                    # Get hardware details
                    hw_details = {}
                    for processor in node.findall('./microcontroller/processors', namespaces):
                        hw_details['processor'] = processor.get('name', 'Unknown')
                        hw_details['frequency'] = processor.get('frequency', 'Unknown')
                        debug_print(f"  Processor: {hw_details['processor']}, Frequency: {hw_details['frequency']}")
                    
                    for memory in node.findall('./microcontroller/memory', namespaces):
                        hw_details['memory'] = memory.get('name', 'Unknown')
                        hw_details['memory_size'] = memory.get('size', 'Unknown')
                        debug_print(f"  Memory: {hw_details['memory']}, Size: {hw_details['memory_size']}")
                    
                    # Check if this component already exists in SAML components
                    existing_component = None
                    for comp in components:
                        comp_name = comp['name'].replace(' ', '')
                        node_name_clean = node_name.replace(' ', '')
                        
                        # Check if either name contains the other
                        if node_name_clean in comp_name or comp_name in node_name_clean:
                            existing_component = comp
                            debug_print(f"  Matched with existing component: {comp['name']}")
                            break
                    
                    if existing_component:
                        # Update existing component with hardware info
                        debug_print(f"  Updating existing component {existing_component['name']} with hardware details")
                        existing_component.update({
                            'protocol': protocol,
                            'routing': routing,
                            'hw_details': hw_details,
                            'source': 'both'
                        })
                    else:
                        # Create new component
                        debug_print(f"  Creating new component for {node_name}")
                        component_type = 'sensor' if 'Sensor' in node_name else \
                                       'actuator' if 'Actuator' in node_name else \
                                       'interface' if 'Interface' in node_name else \
                                       'controller'
                        
                        debug_print(f"  Identified as: {component_type}")
                        
                        components.append({
                            'name': node_name,
                            'type': component_type,
                            'protocol': protocol,
                            'routing': routing,
                            'hw_details': hw_details,
                            'in_ports': [0],  # Default ports
                            'out_ports': [0],
                            'source': 'hwml'
                        })
        except Exception as e:
            print(f"Error extracting components from HWML file: {str(e)}")
            debug_print(f"HWML parsing error details: {traceback.format_exc()}")
    
    # Check for reserved names and rename components that might cause conflicts
    reserved_names = ["Server", "Model", "Simulator"]
    for comp in components:
        if comp['name'] in reserved_names:
            original_name = comp['name']
            comp['name'] = f"Data{comp['name']}"
            debug_print(f"Renamed component '{original_name}' to '{comp['name']}' to avoid naming conflicts")
    
    debug_print(f"Component extraction complete. Found {len(components)} components.")
    return components

def generate_actuator_file(component, output_dir):
    """Generate PyDEVS code for an actuator component."""
    debug_print(f"Generating actuator file for: {component['name']}")
    filename = f"{component['name'].replace(' ', '_').lower()}.py"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(f"""from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class {component['name'].replace(' ', '')}State:
    def __init__(self):
        self.actuator_state = False
        self.processing_time = 0.0

class {component['name'].replace(' ', '')}(AtomicDEVS):
    def __init__(self, simulated_delay=0.1):
        AtomicDEVS.__init__(self, "{component['name']}")
        self.simulated_delay = simulated_delay
        self.state = {component['name'].replace(' ', '')}State()
        self.timeLast = 0.0""")
        
        # Add ports - fixed indentation
        for i in component['in_ports']:
            f.write(f"\n        self.inport{i} = self.addInPort(\"in{i}\")")
        
        for i in component['out_ports']:
            f.write(f"\n        self.outport{i} = self.addOutPort(\"out{i}\")")
        
        f.write("""

    def timeAdvance(self):
        return INFINITY  # Actuators are passive and wait for inputs

    def extTransition(self, inputs):""")
        
        # Use first input port by default
        if component['in_ports']:
            first_inport = component['in_ports'][0]
            f.write(f"""
        received_command = inputs[self.inport{first_inport}]
        print(f"[{{self.name}}] Received command: {{received_command}}")
        
        # Update actuator state based on command
        if isinstance(received_command, dict) and 'processed' in received_command:
            # Handle processed command
            self.state.actuator_state = not self.state.actuator_state
            print(f"[{{self.name}}] Actuator state changed to: {{self.state.actuator_state}}")
        else:
            # Handle direct command
            try:
                self.state.actuator_state = bool(received_command)
                print(f"[{{self.name}}] Actuator state set to: {{self.state.actuator_state}}")
            except:
                print(f"[{{self.name}}] Received invalid command format")
        
        self.state.processing_time = self.timeLast + self.simulated_delay""")
        else:
            f.write("\n        # No input ports defined")
        
        f.write("""
        return self.state

    def intTransition(self):
        self.timeLast = self.state.processing_time
        return self.state
""")
    
    debug_print(f"Generated actuator file: {filepath}")
    return filename

def generate_controller_file(component, output_dir):
    """Generate PyDEVS code for a controller component."""
    debug_print(f"Generating controller file for: {component['name']}")
    filename = f"{component['name'].replace(' ', '_').lower()}.py"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(f"""from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class {component['name'].replace(' ', '')}State:
    def __init__(self):
        self.last_data = None
        self.processing_time = 0.0
        self.threshold_high = 25.0  # Example threshold
        self.threshold_low = 18.0   # Example threshold
        self.decision = None

class {component['name'].replace(' ', '')}(AtomicDEVS):
    def __init__(self, simulated_delay=0.5):
        AtomicDEVS.__init__(self, "{component['name']}")
        self.simulated_delay = simulated_delay
        self.state = {component['name'].replace(' ', '')}State()
        self.timeLast = 0.0""")
        
        # Add ports - fixed indentation
        for i in component['in_ports']:
            f.write(f"\n        self.inport{i} = self.addInPort(\"in{i}\")")
        
        for i in component['out_ports']:
            f.write(f"\n        self.outport{i} = self.addOutPort(\"out{i}\")")
        
        f.write("""

    def timeAdvance(self):
        if self.state.decision is None:
            return INFINITY
        return self.state.processing_time - self.timeLast

    def extTransition(self, inputs):""")
        
        # Use first input port by default
        if component['in_ports']:
            first_inport = component['in_ports'][0]
            f.write(f"""
        self.state.last_data = inputs[self.inport{first_inport}]
        print(f"[{{self.name}}] Received data: {{self.state.last_data}}")
        
        # Process data and make decision
        if isinstance(self.state.last_data, dict):
            try:
                # Extract value for decision making
                data_value = 0
                if 'm2m:cin' in self.state.last_data and 'con' in self.state.last_data['m2m:cin']:
                    # Try to extract numeric value from content
                    content = self.state.last_data['m2m:cin']['con']
                    if isinstance(content, str) and ',' in content:
                        # Format might be: "SensorID, timestamp, value"
                        parts = content.split(',')
                        if len(parts) >= 3:
                            data_value = float(parts[2].strip())
                    elif isinstance(content, (int, float)):
                        data_value = float(content)
                
                # Make decision based on thresholds
                if data_value > self.state.threshold_high:
                    self.state.decision = "open"
                    print(f"[{{self.name}}] Decision: OPEN (value {{data_value}} > threshold {{self.state.threshold_high}})")
                elif data_value < self.state.threshold_low:
                    self.state.decision = "close"
                    print(f"[{{self.name}}] Decision: CLOSE (value {{data_value}} < threshold {{self.state.threshold_low}})")
                else:
                    self.state.decision = None
                    print(f"[{{self.name}}] Decision: No action needed ({{self.state.threshold_low}} <= {{data_value}} <= {{self.state.threshold_high}})")
            except Exception as e:
                print(f"[{{self.name}}] Error processing data: {{str(e)}}")
                self.state.decision = None""")
        else:
            f.write("\n        # No input ports defined")
        
        f.write("""
        self.state.processing_time = self.timeLast + self.simulated_delay
        return self.state

    def outputFnc(self):
        if self.state.decision is None:
            return {}
            
        output = {"command": self.state.decision, "timestamp": self.state.processing_time}
        print(f"[{self.name}] Sending command: {output}")""")
        
        # Determine which output port to use based on decision
        if len(component['out_ports']) >= 2:
            f.write(f"""
        
        # Send to appropriate output port based on decision
        if self.state.decision == "open":
            return {{self.outport{component['out_ports'][0]}: output}}
        elif self.state.decision == "close":
            return {{self.outport{component['out_ports'][1]}: output}}
        else:
            return {{}}
""")
        elif component['out_ports']:
            # If only one output port, use it for all decisions
            first_outport = component['out_ports'][0]
            f.write(f"\n        return {{self.outport{first_outport}: output}}")
        else:
            f.write("\n        return {}")
        
        f.write("""

    def intTransition(self):
        self.timeLast = self.state.processing_time
        self.state.decision = None
        return self.state
""")
    
    debug_print(f"Generated controller file: {filepath}")
    return filename

def generate_sensor_file(component, output_dir):
    """Generate PyDEVS code for a sensor component."""
    debug_print(f"Generating sensor file for: {component['name']}")
    filename = f"{component['name'].replace(' ', '_').lower()}.py"
    filepath = os.path.join(output_dir, filename)
    
    # Add hardware details if available
    hw_comment = ""
    if 'hw_details' in component:
        hw = component['hw_details']
        hw_comment = f"""
# Hardware specifications:
# Processor: {hw.get('processor', 'Unknown')}
# Frequency: {hw.get('frequency', 'Unknown')} MHz
# Memory: {hw.get('memory', 'Unknown')} {hw.get('memory_size', 'Unknown')} MB
# Protocol: {component.get('protocol', 'Unknown')}
# Routing: {component.get('routing', 'Unknown')}"""
        debug_print(f"Including hardware details for {component['name']}")
    
    with open(filepath, 'w') as f:
        f.write(f"""from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time
{hw_comment}

class {component['name'].replace(' ', '')}State:
    def __init__(self):
        self.next_reading_time = 1.0  
        self.sensor_id = "{component['name']}" 
        self.data_to_send = None  

class {component['name'].replace(' ', '')}(AtomicDEVS):
    def __init__(self, name, data_interval=1.0):
        AtomicDEVS.__init__(self, name)
        self.data_interval = data_interval
        self.state = {component['name'].replace(' ', '')}State()
        self.timeLast = 0.0""")
        
        # Add ports - fixed indentation
        for i in component['in_ports']:
            f.write(f"\n        self.inport{i} = self.addInPort(\"in{i}\")")
        
        for i in component['out_ports']:
            f.write(f"\n        self.outport{i} = self.addOutPort(\"out{i}\")")
        
        # Customize sensor based on sensor type
        sensor_type = "temperature" if "Temperature" in component['name'] else "generic"
        
        if sensor_type == "temperature":
            value_generator = "random.uniform(15.0, 30.0)"  # Temperature in Celsius
            unit = "C"
        else:
            value_generator = "random.uniform(0, 100)"
            unit = ""
        
        f.write(f"""

        self.state.data_to_send = {{
            "m2m:cin" :{{
                 "lbl":[
                    "Device-Type",
                    f"{{self.name}}",
                    "V1.0.0"
                 ],
                 "con": f"{{self.state.sensor_id}}, {{int(time.time())}}, {{{value_generator}}}{unit}",
            }}
        }}

    def timeAdvance(self):
        print(f"[{{self.name}}] timeAdvance called. Next reading time: {{self.state.next_reading_time}}, timeLast: {{self.timeLast}}")
        return self.state.next_reading_time - self.timeLast if self.state.data_to_send else INFINITY

    def intTransition(self):
        print(f"[{{self.name}}] intTransition called.")
        self.timeLast = self.state.next_reading_time 
        self.state.next_reading_time = self.timeLast + self.data_interval 
        
        self.state.data_to_send = {{
            "m2m:cin" :{{
                 "lbl":[
                    "Device-Type",
                    f"{{self.name}}",
                    "V1.0.0"
                 ],
                 "con": f"{{self.state.sensor_id}}, {{int(time.time())}}, {{{value_generator}}}{unit}",
            }}
        }}
        return self.state

    def extTransition(self, inputs):
        print(f"[{{self.name}}] extTransition called with inputs: {{inputs}}")
        # Process inputs if needed
        self.state.next_reading_time = self.timeLast + self.data_interval
        return self.state

    def outputFnc(self):
        data = {{
            "m2m:cin" :{{
                 "lbl":[
                    "Device-Type",
                    f"{{self.name}}",
                    "V1.0.0"
                 ],
                 "con": f"{{self.state.sensor_id}}, {{int(time.time())}}, {{{value_generator}}}{unit}",
            }}
        }}
        print(f"[{{self.name}}] outputFnc called. Sending data: {{data}}")""")
        
        # Return data on first outport by default
        if component['out_ports']:
            first_outport = component['out_ports'][0]
            f.write(f"\n        return {{self.outport{first_outport}: data}}")
        else:
            f.write("\n        return {}")
    
    debug_print(f"Generated sensor file: {filepath}")
    return filename

def generate_interface_file(component, output_dir):
    """Generate PyDEVS code for an interface component."""
    debug_print(f"Generating interface file for: {component['name']}")
    filename = f"{component['name'].replace(' ', '_').lower()}.py"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(f"""from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class {component['name'].replace(' ', '')}State:
    def __init__(self):
        self.processing_time = 0.0 
        self.data_to_send = None

class {component['name'].replace(' ', '')}(AtomicDEVS):
    def __init__(self, simulated_delay=1.0):
        AtomicDEVS.__init__(self, "{component['name']}")
        self.simulated_delay = simulated_delay
        self.state = {component['name'].replace(' ', '')}State()
        self.timeLast = 0.0""")
        
        # Add ports - fixed indentation
        for i in component['in_ports']:
            f.write(f"\n        self.inport{i} = self.addInPort(\"in{i}\")")
        
        for i in component['out_ports']:
            f.write(f"\n        self.outport{i} = self.addOutPort(\"out{i}\")")
        
        f.write("""

    def timeAdvance(self):
        if self.state.data_to_send is None:
            return INFINITY
        return self.state.processing_time - self.timeLast

    def extTransition(self, inputs):""")
        
        # Use first input port by default
        if component['in_ports']:
            first_inport = component['in_ports'][0]
            f.write(f"\n        self.state.data_to_send = inputs[self.inport{first_inport}]")
        else:
            f.write("\n        # No input ports defined")
        
        f.write("""
        self.state.processing_time = self.timeLast + self.simulated_delay
        return self.state

    def outputFnc(self):
        sensor_data = self.state.data_to_send
        processed_data = {
            "processed": True,
            "original": sensor_data,
            "timestamp": f"processed-{sensor_data['m2m:cin']['con'] if 'm2m:cin' in sensor_data else 'unknown'}"
        }
        self.state.data_to_send = None
        print(f"{self.name} processed data: {processed_data}")""")
        
        # Return data on first outport by default
        if component['out_ports']:
            first_outport = component['out_ports'][0]
            f.write(f"\n        return {{self.outport{first_outport}: processed_data}}")
        else:
            f.write("\n        return {}")
        
        f.write("""

    def intTransition(self):
        self.timeLast = self.state.processing_time
        self.state.processing_time = INFINITY
        return self.state
""")
    
    debug_print(f"Generated interface file: {filepath}")
    return filename

def generate_sink_file(output_dir):
    """Generate PyDEVS code for a sink component."""
    debug_print("Generating sink file")
    filename = "sink.py"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write("""from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class Sink(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Sink")
        self.inport = self.addInPort("in")

    def extTransition(self, inputs):
        received_data = inputs[self.inport]
        print(f"Sink received: {received_data}")
        return self
        
    def timeAdvance(self):
        return INFINITY
""")
    
    debug_print(f"Generated sink file: {filepath}")
    return filename

def generate_model_file(components, connections, output_dir):
    """Generate PyDEVS model file that connects components."""
    debug_print("Generating model file")
    filename = "model.py"
    filepath = os.path.join(output_dir, filename)
    
    # Fix connections to use the renamed components
    fixed_connections = []
    for conn in connections:
        source_comp = conn['source_component']
        target_comp = conn['target_component']
        
        # Check if source or target was a reserved name
        if source_comp in ["Server", "Model", "Simulator"]:
            source_comp = f"Data{source_comp}"
        if target_comp in ["Server", "Model", "Simulator"]:
            target_comp = f"Data{target_comp}"
            
        fixed_conn = conn.copy()
        fixed_conn['source_component'] = source_comp
        fixed_conn['target_component'] = target_comp
        fixed_connections.append(fixed_conn)
    
    # Use the fixed connections
    connections = fixed_connections
    
    # Debug connections
    debug_print(f"Connections to process: {len(connections)}")
    for i, conn in enumerate(connections):
        debug_print(f"Connection {i+1}: {conn['source_component']} -> {conn['target_component']}")
    
    with open(filepath, 'w') as f:
        f.write("from pypdevs.DEVS import CoupledDEVS\n")
        
        # Import components
        for component in components:
            module_name = component['name'].replace(' ', '_').lower()
            class_name = component['name'].replace(' ', '')
            f.write(f"from {module_name} import {class_name}\n")
        
        f.write("from sink import Sink\n\n")
        
        f.write("class SystemModel(CoupledDEVS):\n")
        f.write("    def __init__(self):\n")
        f.write("        CoupledDEVS.__init__(self, \"SystemModel\")\n")
        f.write("        print(\"Model Loaded\")\n\n")
        
        # Initialize components
        for component in components:
            var_name = component['name'].replace(' ', '_').lower()
            class_name = component['name'].replace(' ', '')
            
            if component['type'] == 'sensor':
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(\"{component['name']}\", data_interval=10))\n\n")
            elif component['type'] == 'actuator':
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(simulated_delay=0.1))\n\n")
            elif component['type'] == 'controller':
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(simulated_delay=0.5))\n\n")
            else:
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(simulated_delay=1.0))\n\n")
        
        # Add sink
        f.write("        print(\"Initializing Sink\")\n")
        f.write("        self.sink = self.addSubModel(Sink())\n\n")
        
        # Connect components
        f.write("        # Connect components\n")
        for conn in connections:
            source = conn['source_component'].replace(' ', '_').lower()
            source_port = f"outport{conn['source_port']}" if conn['source_port_type'] == 'output' else f"inport{conn['source_port']}"
            
            target = conn['target_component'].replace(' ', '_').lower()
            target_port = f"inport{conn['target_port']}" if conn['target_port_type'] == 'input' else f"outport{conn['target_port']}"
            
            f.write(f"        print(\"Connecting {conn['source_component']} to {conn['target_component']}\")\n")
            f.write(f"        try:\n")
            f.write(f"            self.connectPorts(self.{source}.{source_port}, self.{target}.{target_port})\n")
            f.write(f"            print(\"  Connection successful\")\n")
            f.write(f"        except Exception as e:\n")
            f.write(f"            print(f\"  Error connecting {source}.{source_port} to {target}.{target_port}: {{str(e)}}\")\n\n")
        
        # Connect unconnected outputs to sink if needed
        connected_outputs = set()
        for conn in connections:
            source = conn['source_component']
            source_port = conn['source_port']
            if conn['source_port_type'] == 'output':
                connected_outputs.add((source, source_port))
        
        f.write("        # Connect unconnected outputs to sink\n")
        for component in components:
            comp_name = component['name']
            for port_idx in component['out_ports']:
                if (comp_name, port_idx) not in connected_outputs:
                    var_name = comp_name.replace(' ', '_').lower()
                    f.write(f"        try:\n")
                    f.write(f"            print(f\"Connecting {comp_name} output {port_idx} to sink\")\n")
                    f.write(f"            self.connectPorts(self.{var_name}.outport{port_idx}, self.sink.inport)\n")
                    f.write(f"            print(\"  Connection successful\")\n")
                    f.write(f"        except Exception as e:\n")
                    f.write(f"            print(f\"  Error connecting {var_name}.outport{port_idx} to sink: {{str(e)}}\")\n\n")
            
        f.write("\n        print(\"Model initialization complete\")\n")
    
    debug_print(f"Generated model file: {filepath}")
    return filename

def generate_experiment_file(output_dir):
    """Generate PyDEVS experiment file to run the simulation."""
    debug_print("Generating experiment file")
    filename = "experiment.py"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write("""from pypdevs.simulator import Simulator
from model import SystemModel
import logging
import sys
import traceback

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("simulation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("PyDEVS-Simulation")

if __name__ == '__main__':
    try:
        logger.info("Starting the model")
        
        model = SystemModel()
        logger.info("Model Loaded")
        
        sim = Simulator(model)
        logger.info("Simulator Loaded")
        
        sim.setClassicDEVS()
        logger.info("Classic DEVS set")
        
        sim.setVerbose()
        logger.info("Verbose mode set")
        
        sim.setTerminationTime(3600) # 1 hour simulation
        logger.info("Termination time set to 3600")
        
        logger.info("Starting simulation")
        sim.simulate()
        logger.info("Simulation finished")
        
    except Exception as e:
        logger.error(f"Error during simulation: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
""")
    
    debug_print(f"Generated experiment file: {filepath}")
    return filename

def generate_readme_file(components, connections, saml_file=None, hwml_file=None, output_dir=None):
    """Generate a README file documenting the generated system."""
    debug_print("Generating README file")
    filename = "README.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(f"""# PyDEVS IoT System Model

## Overview
This PyDEVS model was automatically generated from CAPS model files.

### Input Files
""")
        if saml_file:
            f.write(f"- SAML: `{os.path.basename(saml_file)}`\n")
        if hwml_file:
            f.write(f"- HWML: `{os.path.basename(hwml_file)}`\n")
        
        f.write(f"""
## Components
The system consists of {len(components)} components:

""")
        for comp in components:
            f.write(f"### {comp['name']} ({comp['type'].title()})\n")
            f.write(f"- Input Ports: {len(comp['in_ports'])}\n")
            f.write(f"- Output Ports: {len(comp['out_ports'])}\n")
            
            if 'hw_details' in comp:
                hw = comp['hw_details']
                f.write("- Hardware:\n")
                f.write(f"  - Processor: {hw.get('processor', 'Unknown')}\n")
                f.write(f"  - Frequency: {hw.get('frequency', 'Unknown')} MHz\n")
                f.write(f"  - Memory: {hw.get('memory', 'Unknown')} {hw.get('memory_size', 'Unknown')} MB\n")
                
            if 'protocol' in comp:
                f.write(f"- Protocol: {comp.get('protocol', 'Unknown')}\n")
                f.write(f"- Routing: {comp.get('routing', 'Unknown')}\n")
            
            f.write("\n")
        
        f.write(f"""
## Connections
The system has {len(connections)} connections between components:

""")
        for i, conn in enumerate(connections, 1):
            f.write(f"{i}. From **{conn['source_component']}** (Port {conn['source_port']}, {conn['source_port_type']}) → " 
                   f"To **{conn['target_component']}** (Port {conn['target_port']}, {conn['target_port_type']})\n")
        
        f.write("""
## Running the Simulation
To run the simulation:

```bash
python experiment.py
```

The simulation will run for 1 hour (simulation time) by default.

## Troubleshooting
If the simulation fails, check the following:

1. Look at the simulation.log file for detailed error messages
2. Verify that all components are connected correctly
3. Check that all imported modules are available in your Python environment
4. Make sure you have the PyPDEVS library installed
""")
    
    debug_print(f"Generated README file: {filepath}")
    return filename

def generate_pydevs_files(saml_file_path=None, hwml_file_path=None):
    """Main function to generate PyDEVS files from XML input."""
    debug_print(f"Starting PyDEVS file generation - SAML: {saml_file_path}, HWML: {hwml_file_path}")
    try:
        # Extract components and connections
        components = extract_components(saml_file_path, hwml_file_path)
        debug_print(f"Extracted {len(components)} components")
        
        # Get connections from both files if available
        connections = []
        if saml_file_path:
            debug_print(f"Parsing connections from SAML file: {saml_file_path}")
            saml_connections = parse_connections(saml_file_path)
            debug_print(f"Found {len(saml_connections)} connections in SAML file")
            connections.extend(saml_connections)
        
        if hwml_file_path:
            debug_print(f"Parsing connections from HWML file: {hwml_file_path}")
            hwml_connections = parse_connections(hwml_file_path)
            debug_print(f"Found {len(hwml_connections)} connections in HWML file")
            connections.extend(hwml_connections)
        
        debug_print(f"Total connections: {len(connections)}")
        
        if not components:
            print("No components found in the XML files.")
            return False
        
        # Create timestamped output directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"/Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/generated_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        debug_print(f"Created output directory: {output_dir}")
        
        # Generate files for each component
        generated_files = []
        for component in components:
            debug_print(f"Processing component: {component['name']} (Type: {component['type']})")
            try:
                if component['type'] == 'sensor':
                    filename = generate_sensor_file(component, output_dir)
                elif component['type'] == 'actuator':
                    filename = generate_actuator_file(component, output_dir)
                elif component['type'] == 'controller':
                    filename = generate_controller_file(component, output_dir)
                else:
                    filename = generate_interface_file(component, output_dir)
                generated_files.append(filename)
            except Exception as e:
                print(f"Error generating file for {component['name']}: {str(e)}")
                debug_print(f"Error details: {traceback.format_exc()}")
        
        # Generate sink
        try:
            sink_file = generate_sink_file(output_dir)
            generated_files.append(sink_file)
        except Exception as e:
            print(f"Error generating sink file: {str(e)}")
            debug_print(f"Error details: {traceback.format_exc()}")
        
        # Generate model
        try:
            model_file = generate_model_file(components, connections, output_dir)
            generated_files.append(model_file)
        except Exception as e:
            print(f"Error generating model file: {str(e)}")
            debug_print(f"Error details: {traceback.format_exc()}")
        
        # Generate experiment
        try:
            exp_file = generate_experiment_file(output_dir)
            generated_files.append(exp_file)
        except Exception as e:
            print(f"Error generating experiment file: {str(e)}")
            debug_print(f"Error details: {traceback.format_exc()}")
        
        # Generate README
        try:
            readme_file = generate_readme_file(components, connections, saml_file_path, hwml_file_path, output_dir)
            generated_files.append(readme_file)
        except Exception as e:
            print(f"Error generating README file: {str(e)}")
            debug_print(f"Error details: {traceback.format_exc()}")
        
        # Copy input files for reference
        if saml_file_path:
            try:
                shutil.copy(saml_file_path, os.path.join(output_dir, os.path.basename(saml_file_path)))
                generated_files.append(os.path.basename(saml_file_path))
                debug_print(f"Copied SAML file to output directory")
            except Exception as e:
                print(f"Error copying SAML file: {str(e)}")
        
        if hwml_file_path:
            try:
                shutil.copy(hwml_file_path, os.path.join(output_dir, os.path.basename(hwml_file_path)))
                generated_files.append(os.path.basename(hwml_file_path))
                debug_print(f"Copied HWML file to output directory")
            except Exception as e:
                print(f"Error copying HWML file: {str(e)}")
        
        print(f"Successfully generated PyDEVS files in {output_dir}:")
        for file in generated_files:
            print(f" - {file}")
        
        debug_print("PyDEVS file generation complete")
        return True
    
    except Exception as e:
        print(f"Error generating PyDEVS files: {str(e)}")
        debug_print(f"Error details: {traceback.format_exc()}")
        return False

def main():
    debug_print("Starting generator script")
    if len(sys.argv) < 2:
        print("Usage: python generator.py <saml_file> [hwml_file]")
        print("You must provide at least a SAML file, and optionally a HWML file")
        sys.exit(1)
    
    saml_file_path = sys.argv[1]
    hwml_file_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    debug_print(f"Input arguments - SAML: {saml_file_path}, HWML: {hwml_file_path}")
    
    if not os.path.exists(saml_file_path):
        print(f"Error: SAML file {saml_file_path} does not exist")
        sys.exit(1)
    
    if hwml_file_path and not os.path.exists(hwml_file_path):
        print(f"Error: HWML file {hwml_file_path} does not exist")
        sys.exit(1)
    
    success = generate_pydevs_files(saml_file_path, hwml_file_path)
    if success:
        print("PyDEVS code generation completed successfully.")
    else:
        print("PyDEVS code generation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
