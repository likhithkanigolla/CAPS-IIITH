def generate_int_transition(behaviors, timers):
    """Generate intTransition method"""
    int_code = []
    
    # Handle timer updates
    for timer in timers:
        period = timer.get('period', 1000) / 1000.0
        int_code.append(f"if hasattr(self.state, '{timer['name']}_next') and self.state.{timer['name']}_next <= self.timeLast:")
        if timer.get('cyclic', False):
            int_code.append(f"    self.state.{timer['name']}_next = self.timeLast + {period}")
        else:
            int_code.append(f"    self.state.{timer['name']}_next = INFINITY")
    
    # Reset data after sending
    int_code.append("self.state.data_to_send = None")
    int_code.append("return self.state")
    
    return chr(10).join(["        " + line for line in int_code])

def generate_time_advance(timers, behaviors):
    """Generate timeAdvance method"""
    if not timers:
        return "return INFINITY if self.state.data_to_send is None else 0.0"
    
    time_advance_code = []
    time_advance_code.append("# Check if there's data to send immediately")
    time_advance_code.append("if self.state.data_to_send is not None:")
    time_advance_code.append("    return 0.0")
    time_advance_code.append("")
    time_advance_code.append("next_time = INFINITY")
    
    for timer in timers:
        time_advance_code.append(f"if hasattr(self.state, '{timer['name']}_next'):")
        time_advance_code.append(f"    next_time = min(next_time, self.state.{timer['name']}_next - self.timeLast)")
    
    time_advance_code.append("return next_time")
    
    return chr(10).join(["        " + line for line in time_advance_code])

def generate_output_function(behaviors, role):
    """Generate outputFnc method"""
    output_code = ["result = {}"]
    
    if role == "sensor":
        # For sensors, generate sensor data
        output_code.append("# Generate sensor data")
        output_code.append("sensor_data = {")
        output_code.append('    "m2m:cin": {')
        output_code.append('        "lbl": [')
        output_code.append('            f"{self.name}"')
        output_code.append('        ],')
        output_code.append('        "con": f"{self.name}, {int(time.time())}, {random.uniform(0, 100)}"')
        output_code.append('    }')
        output_code.append('}')
        output_code.append("# Send to all output ports")
        output_code.append("for port_name in dir(self):")
        output_code.append("    if port_name.startswith('out_'):")
        output_code.append("        port = getattr(self, port_name)")
        output_code.append("        result[port] = sensor_data")
    
    elif role == "controller":
        # For controllers, process and forward data
        output_code.append("# Process and forward data")
        output_code.append("if hasattr(self.state, 'data_to_send') and self.state.data_to_send is not None:")
        output_code.append("    data = self.state.data_to_send")
        output_code.append("    # Process data based on behavior rules")
        output_code.append("    for port_name in dir(self):")
        output_code.append("        if port_name.startswith('out_'):")
        output_code.append("            port = getattr(self, port_name)")
        output_code.append("            result[port] = data")
    
    output_code.append("return result")
    
    return chr(10).join(["        " + line for line in output_code])

def generate_component_class(component):
    """Generate PyDEVS AtomicDEVS class for a component"""
    component_name = component['name']
    component_id = component['id']
    component_role = component['role']
    in_ports = component['ports']['in']
    out_ports = component['ports']['out']
    parameters = component.get('parameters', {})
    timers = component.get('timers', [])
    behaviors = component.get('behaviour', [])
    
    # Generate the state class
    state_class = generate_state_class(component_name, parameters, timers)
    
    # Generate each method separately to avoid f-string nesting issues
    time_advance_method = f"""    def timeAdvance(self):
        \"\"\"Return time until next internal transition\"\"\"
        {generate_time_advance(timers, behaviors)}
        """
    
    int_transition_method = f"""    def intTransition(self):
        \"\"\"Handle internal transition\"\"\"
{generate_int_transition(behaviors, timers)}
"""
    
    ext_transition_method = f"""    def extTransition(self, inputs):
        \"\"\"Handle external transition\"\"\"
{generate_ext_transition(behaviors, component_role)}
"""
    
    output_function_method = f"""    def outputFnc(self):
        \"\"\"Generate output\"\"\"
{generate_output_function(behaviors, component_role)}
"""
    
    # Add comparison method for sorting
    comparison_method = """    def __lt__(self, other):
        \"\"\"Comparison method required for sorting during simulation\"\"\"
        return self.name < other.name
"""
    
    # Generate the DEVS class
    devs_class = f"""from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

{state_class}

class {component_name}(AtomicDEVS):
    def __init__(self, name="{component_name}", **kwargs):
        AtomicDEVS.__init__(self, name)
        self.state = {component_name}State()
        self.timeLast = 0.0
        
        # Initialize ports
{generate_ports(in_ports, out_ports)}
        
        # Initialize parameters
{generate_parameters_init(parameters)}

        # Initialize timers
{generate_timers_init(timers)}

{time_advance_method}
{int_transition_method}
{ext_transition_method}
{output_function_method}
{comparison_method}
"""
    
    return devs_class

def generate_state_class(component_name, parameters, timers):
    """Generate state class for a component"""
    state_attrs = []
    
    # Add parameters to state
    for param_name, param_info in parameters.items():
        initial_value = param_info.get('initialValue', 'None')
        if param_info.get('type') == 'boolean':
            # Convert JSON-style booleans to Python-style booleans
            if isinstance(initial_value, bool):
                initial_value = str(initial_value).capitalize()
            elif isinstance(initial_value, str) and initial_value.lower() in ['true', 'false']:
                initial_value = initial_value.capitalize()
        state_attrs.append(f"        self.{param_name} = {initial_value}")
    
    # Add timer attributes to state
    for timer in timers:
        state_attrs.append(f"        self.{timer['name']}_next = 0.0")
    
    # Add data to send attribute
    state_attrs.append("        self.data_to_send = None")
    
    # If no attributes, add a pass
    if not state_attrs:
        state_attrs = ["        pass"]
    
    state_class = f"""class {component_name}State:
    def __init__(self):
{chr(10).join(state_attrs)}
"""
    
    return state_class

def generate_ports(in_ports, out_ports):
    """Generate port initialization code"""
    port_code = []
    
    for port in in_ports:
        port_code.append(f"        self.{port} = self.addInPort(\"{port}\")")
    
    for port in out_ports:
        port_code.append(f"        self.{port} = self.addOutPort(\"{port}\")")
    
    if not port_code:
        return "        pass"
    
    return chr(10).join(port_code)

def generate_parameters_init(parameters):
    """Generate parameter initialization code"""
    if not parameters:
        return "        pass"
    
    param_code = []
    for param_name, param_info in parameters.items():
        param_code.append(f"        self.state.{param_name} = kwargs.get('{param_name}', {param_info.get('initialValue', 'None')})")
    
    return chr(10).join(param_code)

def generate_timers_init(timers):
    """Generate timer initialization code"""
    if not timers:
        return "        pass"
    
    timer_code = []
    for timer in timers:
        period = timer.get('period', 1000) / 1000.0  # Convert ms to seconds
        timer_code.append(f"        self.state.{timer['name']}_next = {period}")
    
    return chr(10).join(timer_code)

def generate_ext_transition(behaviors, role):
    """Generate extTransition method"""
    if role == "sensor":
        return "        print(f\"[{self.name}] extTransition called with inputs: {inputs}\")\n        return self.state"
    
    ext_code = ["        received_data = None"]
    
    # Process received data
    ext_code.append("        for port_name, port_value in inputs.items():")
    ext_code.append("            print(f\"[{self.name}] Received data on {port_name}: {port_value}\")")
    ext_code.append("            received_data = port_value")
    
    # Store the received data
    ext_code.append("        self.state.data_to_send = received_data")
    
    # Prepare a response if needed (for controllers)
    if role == "controller":
        ext_code.append("        # Process data for controller")
        ext_code.append("        if received_data is not None:")
        ext_code.append("            # Extract temperature or other relevant data")
        ext_code.append("            if isinstance(received_data, dict) and 'm2m:cin' in received_data:")
        ext_code.append("                content = received_data['m2m:cin'].get('con', '')")
        ext_code.append("                parts = content.split(',')")
        ext_code.append("                if len(parts) > 2:")  # Expecting format "sensor_id, timestamp, value"
        ext_code.append("                    try:")
        ext_code.append("                        temperature = float(parts[2].strip())")
        ext_code.append("                        # Decide based on temperature")
        ext_code.append("                        if temperature > 25:")
        ext_code.append("                            self.state.Open = True")
        ext_code.append("                            self.state.Close = False")
        ext_code.append("                        elif temperature < 18:")
        ext_code.append("                            self.state.Open = False")
        ext_code.append("                            self.state.Close = True")
        ext_code.append("                    except (ValueError, IndexError):")
        ext_code.append("                        pass")
    
    ext_code.append("        return self.state")
    
    return "\n".join(ext_code)

def generate_coupled_model(config, component_files):
    """Generate PyDEVS CoupledDEVS model that connects components"""
    model_name = "GeneratedModel"
    components = config['components']
    connections = config['connections']
    
    # Start with imports
    imports = ["from pypdevs.DEVS import CoupledDEVS"]
    for component_file in component_files:
        # Import the class from the component file
        component_name = next((c['name'] for c in components if c['name'].lower().replace(' ', '_') == component_file), None)
        if component_name:
            imports.append(f"from {component_file} import {component_name}")
    
    # Create the model class
    model_class = f"""
class {model_name}(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "{model_name}")
        print("Model Loading...")
        
        # Initialize components
"""
    
    # Add component initialization
    for component in components:
        component_var = component['id'].lower()
        component_class = component['name']
        model_class += f"        self.{component_var} = self.addSubModel({component_class}(\"{component_var}\"))\n"
        model_class += f"        print(\"Initialized {component_class} as {component_var}\")\n"
    
    model_class += "\n        # Connect components\n"
    
    # Add connections
    for connection in connections:
        source_parts = connection['from'].split('.')
        target_parts = connection['to'].split('.')
        
        source_component = source_parts[0].lower()
        source_port = source_parts[1]
        
        target_component = target_parts[0].lower()
        target_port = target_parts[1]
        
        model_class += f"        self.connectPorts(self.{source_component}.{source_port}, self.{target_component}.{target_port})\n"
        model_class += f"        print(\"Connected {source_component}.{source_port} to {target_component}.{target_port}\")\n"
    
    model_class += "\n        print(\"Model initialization complete\")\n"
    
    # Combine everything
    return "\n".join(imports) + model_class
