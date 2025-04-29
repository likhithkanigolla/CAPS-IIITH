import os
import random
import time
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from .debug_utils import debug_print

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
        
        for i in component['in_ports']:
            f.write(f"\n        self.inport{i} = self.addInPort(\"in{i}\")")
        
        for i in component['out_ports']:
            f.write(f"\n        self.outport{i} = self.addOutPort(\"out{i}\")")
        
        f.write("""

    def timeAdvance(self):
        return INFINITY  # Actuators are passive and wait for inputs

    def extTransition(self, inputs):""")
        
        if component['in_ports']:
            first_inport = component['in_ports'][0]
            f.write(f"""
        received_command = inputs[self.inport{first_inport}]
        #print(f"[{{self.name}}] Received command: {{received_command}}")
        
        if isinstance(received_command, dict) and 'processed' in received_command:
            self.state.actuator_state = not self.state.actuator_state
            #print(f"[{{self.name}}] Actuator state changed to: {{self.state.actuator_state}}")
        else:
            try:
                self.state.actuator_state = bool(received_command)
                #print(f"[{{self.name}}] Actuator state set to: {{self.state.actuator_state}}")
            except:
                print("Received invalid command format")
        
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
        
        if component['in_ports']:
            first_inport = component['in_ports'][0]
            f.write(f"""
        self.state.last_data = inputs[self.inport{first_inport}]
        #print(f"[{{self.name}}] Received data: {{self.state.last_data}}")
        
        if isinstance(self.state.last_data, dict):
            try:
                data_value = 0
                if 'm2m:cin' in self.state.last_data and 'con' in self.state.last_data['m2m:cin']:
                    content = self.state.last_data['m2m:cin']['con']
                    if isinstance(content, str) and ',' in content:
                        parts = content.split(',')
                        if len(parts) >= 3:
                            data_value = float(parts[2].strip())
                    elif isinstance(content, (int, float)):
                        data_value = float(content)
                
                if data_value > self.state.threshold_high:
                    self.state.decision = "open"
                    #print(f"[{{self.name}}] Decision: OPEN (value {{data_value}} > threshold {{self.state.threshold_high}})")
                elif data_value < self.state.threshold_low:
                    self.state.decision = "close"
                    #print(f"[{{self.name}}] Decision: CLOSE (value {{data_value}} < threshold {{self.state.threshold_low}})")
                else:
                    self.state.decision = None
                    #print(f"[{{self.name}}] Decision: No action needed ({{self.state.threshold_low}} <= {{data_value}} <= {{self.state.threshold_high}})")
            except Exception as e:
                #print(f"[{{self.name}}] Error processing data: {{str(e)}}")
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
        
        if len(component['out_ports']) >= 2:
            f.write(f"""
        
        if self.state.decision == "open":
            return {{self.outport{component['out_ports'][0]}: output}}
        elif self.state.decision == "close":
            return {{self.outport{component['out_ports'][1]}: output}}
        else:
            return {{}}
""")
        elif component['out_ports']:
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
    
    # Use the data_interval from the component, default to 1.0 if not provided
    data_interval = component.get('data_interval', 1.0)
    debug_print(f"Using data_interval: {data_interval} seconds for {component['name']}")
    
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
    def __init__(self, name, data_interval={data_interval}):
        AtomicDEVS.__init__(self, name)
        self.data_interval = data_interval
        self.state = {component['name'].replace(' ', '')}State()
        self.timeLast = 0.0""")
        
        for i in component['in_ports']:
            f.write(f"\n        self.inport{i} = self.addInPort(\"in{i}\")")
        
        for i in component['out_ports']:
            f.write(f"\n        self.outport{i} = self.addOutPort(\"out{i}\")")
        
        sensor_type = "temperature" if "Temperature" in component['name'] else "generic"
        
        if sensor_type == "temperature":
            value_generator = "random.uniform(15.0, 30.0)"
        else:
            value_generator = "random.uniform(0, 100)"
        
        f.write(f"""

        self.state.data_to_send = {{
            "m2m:cin" :{{
                 "lbl":[
                    "Device-Type",
                    f"{{self.name}}",
                    "V1.0.0"
                 ],
                 "con": f"{{self.state.sensor_id}}, {{int(time.time())}}, {{{value_generator}}}",
            }}
        }}

    def timeAdvance(self):
        #print(f"[{{self.name}}] timeAdvance called. Next reading time: {{self.state.next_reading_time}}, timeLast: {{self.timeLast}}")
        return self.state.next_reading_time - self.timeLast if self.state.data_to_send else INFINITY

    def intTransition(self):
        #print(f"[{{self.name}}] intTransition called.")
        self.timeLast = self.state.next_reading_time 
        self.state.next_reading_time = self.timeLast + self.data_interval 
        
        self.state.data_to_send = {{
            "m2m:cin" :{{
                 "lbl":[
                    "Device-Type",
                    f"{{self.name}}",
                    "V1.0.0"
                 ],
                 "con": f"{{self.state.sensor_id}}, {{int(time.time())}}, {{{value_generator}}}",
            }}
        }}
        return self.state

    def extTransition(self, inputs):
        #print(f"[{{self.name}}] extTransition called with inputs: {{inputs}}")
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
                 "con": f"{{self.state.sensor_id}}, {{int(time.time())}}, {{{value_generator}}}",
            }}
        }}
        #print(f"[{{self.name}}] outputFnc called. Sending data: {{data}}")""")
        
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
    
    fixed_connections = []
    for conn in connections:
        source_comp = conn['source_component']
        target_comp = conn['target_component']
        
        if source_comp in ["Server", "Model", "Simulator"]:
            source_comp = f"Data{source_comp}"
        if target_comp in ["Server", "Model", "Simulator"]:
            target_comp = f"Data{target_comp}"
            
        fixed_conn = conn.copy()
        fixed_conn['source_component'] = source_comp
        fixed_conn['target_component'] = target_comp
        fixed_connections.append(fixed_conn)
    
    connections = fixed_connections
    
    debug_print(f"Connections to process: {len(connections)}")
    for i, conn in enumerate(connections):
        debug_print(f"Connection {i+1}: {conn['source_component']} -> {conn['target_component']}")
    
    with open(filepath, 'w') as f:
        f.write("from pypdevs.DEVS import CoupledDEVS\n")
        
        for component in components:
            module_name = component['name'].replace(' ', '_').lower()
            class_name = component['name'].replace(' ', '')
            f.write(f"from {module_name} import {class_name}\n")
        
        f.write("from sink import Sink\n\n")
        
        f.write("class SystemModel(CoupledDEVS):\n")
        f.write("    def __init__(self):\n")
        f.write("        CoupledDEVS.__init__(self, \"SystemModel\")\n")
        f.write("        print(\"Model Loaded\")\n\n")
        
        for component in components:
            var_name = component['name'].replace(' ', '_').lower()
            class_name = component['name'].replace(' ', '')
            
            if component['type'] == 'sensor':
                data_interval = component.get('data_interval', 5.0)  # Default to 10 if not provided
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(\"{component['name']}\", data_interval={data_interval}))\n\n")
            elif component['type'] == 'actuator':
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(simulated_delay=0.1))\n\n")
            elif component['type'] == 'controller':
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(simulated_delay=0.5))\n\n")
            else:
                f.write(f"        print(\"Initializing {component['name']}\")\n")
                f.write(f"        self.{var_name} = self.addSubModel({class_name}(simulated_delay=1.0))\n\n")
        
        f.write("        print(\"Initializing Sink\")\n")
        f.write("        self.sink = self.addSubModel(Sink())\n\n")
        
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
        
        sim.setTerminationTime(3600)
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

def generate_hwml_details(hwml_file):
    """Extract hardware details from HWML file if provided."""
    if not hwml_file or not os.path.exists(hwml_file):
        return {}
    
    try:
        from .saml_parser import parse_hwml_file
        return parse_hwml_file(hwml_file)
    except Exception as e:
        debug_print(f"Error parsing HWML file: {str(e)}")
        return {}

def generate_pydevs_from_saml(saml_file, hwml_file=None, output_dir=None):
    """Generate PyDEVS files from SAML and optional HWML file."""
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(saml_file), "generated_pydevs")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    debug_print(f"Generating PyDEVS files from SAML: {saml_file}")
    debug_print(f"Output directory: {output_dir}")
    
    # Parse SAML file to extract components and connections
    from .saml_parser import parse_saml_file
    components, connections = parse_saml_file(saml_file)
    
    # Extract hardware details if HWML file is provided
    hw_details = generate_hwml_details(hwml_file)
    
    # Add hardware details to components if available
    for component in components:
        if component['name'] in hw_details:
            component['hw_details'] = hw_details[component['name']]
    
    # Generate files based on component types
    generated_files = []
    for component in components:
        debug_print(f"Generating files for component: {component['name']} (Type: {component['type']})")
        
        if component['type'] == 'sensor':
            filename = generate_sensor_file(component, output_dir)
            generated_files.append(filename)
        elif component['type'] == 'actuator':
            filename = generate_actuator_file(component, output_dir)
            generated_files.append(filename)
        elif component['type'] == 'controller':
            filename = generate_controller_file(component, output_dir)
            generated_files.append(filename)
        elif component['type'] == 'interface':
            filename = generate_interface_file(component, output_dir)
            generated_files.append(filename)
    
    # Generate the sink file
    sink_file = generate_sink_file(output_dir)
    generated_files.append(sink_file)
    
    # Generate the model file
    model_file = generate_model_file(components, connections, output_dir)
    generated_files.append(model_file)
    
    # Generate the experiment file
    experiment_file = generate_experiment_file(output_dir)
    generated_files.append(experiment_file)
    
    # Generate the README file
    readme_file = generate_readme_file(components, connections, saml_file, hwml_file, output_dir)
    generated_files.append(readme_file)
    
    debug_print(f"Successfully generated {len(generated_files)} files in {output_dir}")
    return generated_files