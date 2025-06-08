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

def generate_output_function(behaviors, role, component=None):
    """Generate outputFnc method with type-aware random value generation"""
    output_code = ["result = {}"]
    
    if role == "sensor":
        # Default to real number as fallback
        sensor_type = "real"
        output_value = "random.uniform(0, 100)"
        
        # Extract parameter information if component is provided
        if component and 'parameters' in component:
            for param_name, param_info in component['parameters'].items():
                if 'type' in param_info:
                    sensor_type = param_info['type'].lower()
                    print(f"Using parameter '{param_name}' with type '{sensor_type}' for sensor data generation")
                    break  # Use the first typed parameter we find
        
        # Generate appropriate random value based on type
        if sensor_type == "boolean":
            output_value = "random.choice([0, 1])"  # Boolean as 0/1
        elif sensor_type == "int":
            output_value = "random.randint(0, 100)"  # Integer between 0-100
        elif sensor_type == "real":
            output_value = "random.uniform(0, 100)"  # Float between 0-100
            
        print(f"Generating {sensor_type} sensor data with value: {output_value}")
        
        output_code.append(f"# Generate {sensor_type} sensor data")
        output_code.append("sensor_data = {")
        output_code.append('    "m2m:cin": {')
        output_code.append('        "lbl": [')
        output_code.append('            f"{self.name}"')
        output_code.append('        ],')
        output_code.append(f'        "con": f"{{self.name}}, {{int(time.time())}}, {{{output_value}}}"')
        output_code.append('    }')
        output_code.append('}')
        output_code.append("# Send to all output ports")
        output_code.append("for port_name in dir(self):")
        output_code.append("    if port_name.startswith('out_'):")
        output_code.append("        port = getattr(self, port_name)")
        output_code.append("        result[port] = sensor_data")
        
    elif role == "controller":
        # For controllers, only send to the specified port (not all ports)
        output_code.append("# Process and forward data only to the specified port")
        output_code.append("if hasattr(self.state, 'data_to_send') and self.state.data_to_send is not None and hasattr(self.state, 'output_port') and self.state.output_port:")
        output_code.append("    port = getattr(self, self.state.output_port)")
        output_code.append("    result[port] = self.state.data_to_send")
    
    output_code.append("return result")
    
    return chr(10).join(["        " + line for line in output_code])

def generate_component_class(component, json_model=None):
    """Generate PyDEVS AtomicDEVS class for a component"""
    component_name = component['name']
    component_id = component['id']
    component_role = component['role']
    in_ports = component['ports']['in']
    out_ports = component['ports']['out']
    parameters = component.get('parameters', {})
    timers = component.get('timers', [])
    behaviors = component.get('behaviour', [])
    
    # For controllers, use the template-based approach to handle conditions
    if component_role == 'controller' and json_model:
        return generate_controller_code(component, json_model)
    
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
{generate_ext_transition(behaviors, component_role, component)}
"""
    
    output_function_method = f"""    def outputFnc(self):
        \"\"\"Generate output\"\"\"
{generate_output_function(behaviors, component_role, component)}
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
    
    # Add generic attributes needed for all components
    state_attrs.append("        self.data_to_send = None")
    state_attrs.append("        self.output_port = None")
    state_attrs.append("        self.received_value = None")  # Generic value storage
    
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

def generate_ext_transition(behaviors, role, component=None):
    """Generate extTransition method"""
    if role == "sensor":
        # return "        print(f\"[{self.name}] extTransition called with inputs: {inputs}\")\n        return self.state"
        return "        print(f\"extTransition called\")\n        return self.state"
    
    ext_code = ["        received_data = None"]
    
    # Process received data
    ext_code.append("        for port_name, port_value in inputs.items():")
    # ext_code.append("            print(f\"[{self.name}] Received data on {port_name}: {port_value}\")")
    # ext_code.append("            received_data = port_value")
    ext_code.append("            received_data")
    
    # For actuators, handle input generically
    if role == "actuator":
        ext_code.append("        # For actuator, handle inputs generically by port")
        ext_code.append("        if received_data is not None:")
        
        # Get port names from component
        in_ports = component['ports']['in']
        for i, port in enumerate(in_ports):
            # Generate dynamic code for each port
            ext_code.append(f"            if port_name == self.{port}:")
            
            # Track if we've added any actions for this port
            added_actions = False
            
            # Find matched connections for this port in the component's connectionsInternal
            if 'connectionsInternal' in component:
                for connection in component.get('connectionsInternal', []):
                    # Make pattern matching more robust - check for various forms of 'receive'
                    if connection.get('from', '').lower().startswith(('receive', 'recive', 'recv')):
                        action = connection.get('to', 'Actuate')
                        data_recipient = connection.get('dataRecipient', '')
                        if data_recipient:
                            ext_code.append(f"                print(f\"[{{self.name}}] Actuating {data_recipient} based on received command\")")
                            ext_code.append(f"                self.state.{data_recipient} = True")
                            # If there are other recipients, set them to false
                            for other_conn in component.get('connectionsInternal', []):
                                other_recipient = other_conn.get('dataRecipient', '')
                                if other_recipient and other_recipient != data_recipient:
                                    ext_code.append(f"                self.state.{other_recipient} = False")
                            added_actions = True
            
            # Ensure there's always at least one action in each if block
            if not added_actions:
                ext_code.append(f"                print(f\"[{{self.name}}] Processing input on port {port}\")")
                ext_code.append(f"                # Default action for port {port}")
                ext_code.append(f"                self.state.data_to_send = received_data")
        
        ext_code.append("        self.state.data_to_send = received_data")
        ext_code.append("        return self.state")
        return "\n".join(ext_code)
    
    # Store the received data
    ext_code.append("        self.state.data_to_send = received_data")
    
    # For controllers, extract generic value handling without any hardcoded logic
    if role == "controller":
        ext_code.append("        # Process data for controller")
        ext_code.append("        if received_data is not None:")
        ext_code.append("            # Extract data from the message")
        ext_code.append("            if isinstance(received_data, dict) and 'm2m:cin' in received_data:")
        ext_code.append("                content = received_data['m2m:cin'].get('con', '')")
        ext_code.append("                parts = content.split(',')")
        ext_code.append("                if len(parts) > 2:")  # Expecting format "sensor_id, timestamp, value"
        ext_code.append("                    try:")
        ext_code.append("                        value = float(parts[2].strip())")
        ext_code.append("                        self.state.received_value = value")
        ext_code.append("                        #print(f\"[{self.name}] Processing value: {value}\")")
        
        # Extract conditions from component if available
        if component and 'connectionsInternal' in component:
            conditions_found = False
            for i, connection in enumerate(component.get('connectionsInternal', [])):
                if 'condition' in connection and connection['condition']:
                    conditions_found = True
                    condition = connection['condition']
                    left = condition.get('left', '')
                    operator = condition.get('operator', '')
                    right = condition.get('right', '')
                    to_action = connection.get('to', '')
                    data_recipient = connection.get('dataRecipient', left)  # Default to left operand if not specified
                    
                    if left and operator and right is not None:
                        # Find the appropriate port for this action
                        port_num = None
                        for j, out_port in enumerate(component['ports']['out']):
                            port_num = j
                            # Try to find a matching outgoing connection in the model
                            for behavior in component.get('behaviour', []):
                                if behavior.get('name') == to_action and 'toMessagePorts' in behavior:
                                    port_num = int(behavior['toMessagePorts'].split('_')[1])
                            
                        # Handle the first condition with 'if', others with 'elif'
                        if_statement = "if" if i == 0 else "elif"
                        
                        ext_code.append(f"                        # Condition from model: {left} {operator} {right}")
                        ext_code.append(f"                        {if_statement} value {operator} {right}:")
                        ext_code.append(f"                            self.state.{data_recipient} = True")
                        # Find other possible data recipients to set to False
                        for other_conn in component.get('connectionsInternal', []):
                            if 'condition' in other_conn and other_conn['condition']:
                                other_recipient = other_conn.get('dataRecipient', '')
                                if other_recipient and other_recipient != data_recipient:
                                    ext_code.append(f"                            self.state.{other_recipient} = False")
                                
                        ext_code.append(f"                            self.state.data_to_send = received_data")
                        ext_code.append(f"                            self.state.output_port = \"out_{port_num}\"")
                        ext_code.append(f"                            print(f\"[{{self.name}}] Value {{value}} {operator} {right}: Sending to {to_action}\")")
            
            # Add the else case if conditions were found
            if conditions_found:
                ext_code.append("                        else:")
                ext_code.append("                            # No condition matched")
                ext_code.append("                            self.state.data_to_send = None") 
                ext_code.append("                            print(f\"[{self.name}] Value {value} is in normal range: No action\")")
        
        # Close the try-except block
        ext_code.append("                    except (ValueError, IndexError):")
        ext_code.append("                        print(f\"[{self.name}] Error parsing value from: {content}\")")
    
    ext_code.append("        return self.state")
    
    return "\n".join(ext_code)

def generate_controller_code(component, json_model):
    """Generate controller component code based on JSON specification"""
    # Extract all conditions from the component's connectionsInternal
    conditions = []
    
    # Find all unique variable names used in conditions
    condition_variables = set()
    
    for conn in component.get('connectionsInternal', []):
        if 'condition' in conn and conn['condition']:
            condition = conn['condition']
            
            # Check if condition is a string or a dictionary
            if isinstance(condition, str):
                # Parse the string condition (e.g., "if motion==1")
                if condition.startswith("if "):
                    condition_text = condition[3:].strip()  # Remove "if " prefix
                else:
                    condition_text = condition
                    
                # Try to extract left, operator, right parts
                if "==" in condition_text:
                    left, right = condition_text.split("==", 1)
                    operator = "=="
                elif ">" in condition_text:
                    left, right = condition_text.split(">", 1)
                    operator = ">"
                elif "<" in condition_text:
                    left, right = condition_text.split("<", 1)
                    operator = "<"
                else:
                    # Default if we can't parse
                    left = "motion"
                    operator = "=="
                    right = "1"
                    
                left = left.strip()
                right = right.strip()
            else:
                # The normal case where condition is a dictionary
                left = condition.get('left', '')
                operator = condition.get('operator', '')
                right = condition.get('right', '')
                
            to_action = conn.get('to', '')
            data_recipient = conn.get('dataRecipient', left)  # Default to left operand if not specified
            
            # Add the variable name to our set of tracked variables
            if left:
                condition_variables.add(left)
            
            if left and operator and right is not None:
                # Find the appropriate port for this action
                port_num = None
                for j, out_port in enumerate(component['ports']['out']):
                    port_num = j
                    # Try to find a matching outgoing connection in the model
                    for behavior in component.get('behaviour', []):
                        if behavior.get('name') == to_action and 'toMessagePorts' in behavior:
                            port_num = int(behavior['toMessagePorts'].split('_')[1])
                
                condition_info = {
                    'left': left,
                    'operator': operator,
                    'right': right,
                    'to': to_action,
                    'port': f"out_{port_num}",
                    'dataRecipient': data_recipient
                }
                conditions.append(condition_info)
    
    # Generate condition handling code as if-elif-else blocks
    condition_code = []
    
    # Use lowercase version of variable name for consistency
    value_var_name = "value"  # Default fallback name
    
    for i, cond in enumerate(conditions):
        prefix = "if" if i == 0 else "elif"
        condition_code.append(
            f"                        {prefix} {value_var_name} {cond['operator']} {cond['right']}:\n"
            f"                            self.state.{cond['dataRecipient']} = True\n"
            f"                            self.state.data_to_send = received_data\n"
            f"                            self.state.output_port = \"{cond['port']}\"\n"
            f"                            #print(f\"[{{self.name}}] {cond['left']} {{value}} {cond['operator']} {cond['right']}: Sending to {cond['to']}\")"
        )
    
    if condition_code:
        condition_code.append(
            "                        else:\n"
            "                            # No condition matched\n"
            "                            self.state.data_to_send = None\n"
            f"                            print(f\"[{{self.name}}] Value {{value}} is in normal range: No action\")"
        )
    
    # Combine all conditions into one string
    condition_logic = "\n".join(condition_code)
    
    # Generate the full controller class code manually
    controller_code = f"""from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class {component['name']}State:
    def __init__(self):
"""
    
    # Add parameters to state
    for param_name, param_info in component.get('parameters', {}).items():
        initial_value = param_info.get('initialValue', 'None')
        if param_info.get('type') == 'boolean':
            if isinstance(initial_value, bool):
                initial_value = str(initial_value).capitalize()
            elif isinstance(initial_value, str) and initial_value.lower() in ['true', 'false']:
                initial_value = initial_value.capitalize()
        controller_code += f"        self.{param_name} = {initial_value}\n"
    
    # Add standard controller state properties
    controller_code += "        self.data_to_send = None\n"
    controller_code += "        self.output_port = None\n"
    
    # Add all condition variables to state
    for var in condition_variables:
        controller_code += f"        self.{var} = None  # Condition variable from model\n"
    
    # Complete the controller class
    controller_code += f"""
class {component['name']}(AtomicDEVS):
    def __init__(self, name="{component['name']}", **kwargs):
        AtomicDEVS.__init__(self, name)
        self.state = {component['name']}State()
        self.timeLast = 0.0
        
        # Initialize ports
"""
    
    # Add ports
    for port in component['ports']['in']:
        controller_code += f"        self.{port} = self.addInPort(\"{port}\")\n"
    
    for port in component['ports']['out']:
        controller_code += f"        self.{port} = self.addOutPort(\"{port}\")\n"
    
    # Add parameter initialization
    controller_code += "\n        # Initialize parameters\n"
    for param_name, param_info in component.get('parameters', {}).items():
        controller_code += f"        self.state.{param_name} = kwargs.get('{param_name}', {param_info.get('initialValue', 'None')})\n"
    
    # Add standard DEVS methods
    controller_code += """
    def timeAdvance(self):
        \"\"\"Return time until next internal transition\"\"\"
        return INFINITY if self.state.data_to_send is None else 0.0
        
    def intTransition(self):
        \"\"\"Handle internal transition\"\"\"
        self.state.data_to_send = None
        self.state.output_port = None
        return self.state

    def extTransition(self, inputs):
        \"\"\"Handle external transition\"\"\"
        received_data = None
        for port_name, port_value in inputs.items():
            #print(f"[{self.name}] Received data on {port_name}: {port_value}")
            received_data = port_value
            
        # Process data for controller
        if received_data is not None:
            # Extract data from received message
            if isinstance(received_data, dict) and 'm2m:cin' in received_data:
                content = received_data['m2m:cin'].get('con', '')
                parts = content.split(',')
                if len(parts) > 2:
                    try:
                        # Extract value from the message
                        value = float(parts[2].strip())
"""

    # Store the extracted value in all the condition variables
    for var in condition_variables:
        controller_code += f"                        self.state.{var} = value  # Store in condition variable\n"

    controller_code += f"""                        #print(f"[{{self.name}}] Processing value: {{value}}")
                        
                        # Apply model-defined conditions
"""
    # Add the condition logic
    controller_code += condition_logic

    # Complete the class with remaining methods
    controller_code += """
                    except (ValueError, IndexError):
                        #print(f"Error parsing value from: {content}")
                        print("Error parsing value")
        return self.state

    def outputFnc(self):
        \"\"\"Generate output\"\"\"
        result = {}
        if hasattr(self.state, 'data_to_send') and self.state.data_to_send is not None and self.state.output_port:
            port = getattr(self, self.state.output_port)
            result[port] = self.state.data_to_send
        return result

    def __lt__(self, other):
        \"\"\"Comparison method required for sorting during simulation\"\"\"
        return self.name < other.name
"""

    return controller_code

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

def save_model_json(model_json, output_path):
    """Save the model JSON to a file"""
    import json
    import os
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the JSON model
    with open(output_path, 'w') as f:
        json.dump(model_json, f, indent=2)
    
    print(f"Model JSON saved to: {output_path}")
    return output_path

def save_connections_json(model_json, output_path):
    """
    Extract and save connections information to a separate JSON file
    
    Args:
        model_json: The complete model JSON
        output_path: Path where to save the connections file
    
    Returns:
        The path where the connections file was saved
    """
    import json
    import os
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Extract connections from the model
    connections = model_json.get('connections', [])
    
    # Create enhanced connections with component names
    enhanced_connections = []
    components = {comp['id']: comp for comp in model_json.get('components', [])}
    
    for conn in connections:
        source_parts = conn['from'].split('.')
        target_parts = conn['to'].split('.')
        
        source_id = source_parts[0]
        source_port = source_parts[1]
        source_name = components.get(source_id, {}).get('name', source_id)
        
        target_id = target_parts[0]
        target_port = target_parts[1]
        target_name = components.get(target_id, {}).get('name', target_id)
        
        enhanced_connections.append({
            "from": conn['from'],
            "to": conn['to'],
            "source": {
                "id": source_id,
                "name": source_name,
                "port": source_port,
                "role": components.get(source_id, {}).get('role', 'unknown')
            },
            "target": {
                "id": target_id,
                "name": target_name,
                "port": target_port,
                "role": components.get(target_id, {}).get('role', 'unknown')
            }
        })
    
    connections_json = {
        "connections": enhanced_connections,
        "summary": f"Total connections: {len(enhanced_connections)}"
    }
    
    # Save the connections JSON
    with open(output_path, 'w') as f:
        json.dump(connections_json, f, indent=2)
    
    print(f"Connections JSON saved to: {output_path}")
    return output_path

def generate_all_files(model_json, output_dir):
    """
    Generate all necessary files from the model JSON
    
    Args:
        model_json: The complete model JSON
        output_dir: Directory where to save all generated files
    
    Returns:
        A list of paths to all generated files
    """
    import os
    import json
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    
    # Save the model JSON first
    model_json_path = os.path.join(output_dir, "model.json")
    save_model_json(model_json, model_json_path)
    generated_files.append(model_json_path)
    
    # Save connections JSON
    connections_json_path = os.path.join(output_dir, "connections.json")
    save_connections_json(model_json, connections_json_path)
    generated_files.append(connections_json_path)
    
    # Generate component Python files
    components = model_json.get('components', [])
    component_files = []
    
    for component in components:
        component_name = component['name']
        component_id = component['id']
        component_role = component.get('role', 'unknown')
        
        # Create a safe filename
        filename = f"{component_name.lower().replace(' ', '_')}.py"
        file_path = os.path.join(output_dir, filename)
        
        # Generate the component code
        component_code = generate_component_class(component, model_json)
        
        # Save to file
        with open(file_path, 'w') as f:
            f.write(component_code)
        
        print(f"Generated {component_role} component: {file_path}")
        generated_files.append(file_path)
        component_files.append(component_name.lower().replace(' ', '_'))
    
    # Generate the coupled model
    coupled_model_code = generate_coupled_model(model_json, component_files)
    coupled_model_path = os.path.join(output_dir, "coupled_model.py")
    
    with open(coupled_model_path, 'w') as f:
        f.write(coupled_model_code)
    
    print(f"Generated coupled model: {coupled_model_path}")
    generated_files.append(coupled_model_path)
    
    # Create a simple run script
    run_script = """from pypdevs.simulator import Simulator
from coupled_model import GeneratedModel
import os

# Create the model
model = GeneratedModel()

# Create the simulator
sim = Simulator(model)

# Configure simulation parameters
sim.setTerminationTime(100)  # Run for 100 time units
sim.setClassicDEVS()

# Run the simulation
sim.simulate()

print("Simulation complete!")
"""
    
    run_script_path = os.path.join(output_dir, "run_simulation.py")
    with open(run_script_path, 'w') as f:
        f.write(run_script)
    
    print(f"Generated run script: {run_script_path}")
    generated_files.append(run_script_path)
    
    return generated_files

# Example usage:
# if __name__ == "__main__":
#     import sys
#     import json
#     
#     if len(sys.argv) > 2:
#         model_file = sys.argv[1]
#         output_dir = sys.argv[2]
#         
#         with open(model_file, 'r') as f:
#             model_json = json.load(f)
#         
#         generate_all_files(model_json, output_dir)
#     else:
#         print("Usage: python model_generator.py <model_json_file> <output_directory>")
