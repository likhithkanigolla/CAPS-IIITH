from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class {{ component_name }}State:
    def __init__(self):
        # Initialize state variables based on parameters
        {% for param in parameters %}
        self.{{ param.name }} = {{ param.default_value }}
        {% endfor %}
        self.data_to_send = None
        self.output_port = None


class {{ component_name }}(AtomicDEVS):
    def __init__(self, name="{{ component_name }}", **kwargs):
        AtomicDEVS.__init__(self, name)
        self.state = {{ component_name }}State()
        self.timeLast = 0.0
        
        # Initialize ports
        {% for port in in_ports %}
        self.{{ port.name }} = self.addInPort("{{ port.name }}")
        {% endfor %}
        {% for port in out_ports %}
        self.{{ port.name }} = self.addOutPort("{{ port.name }}")
        {% endfor %}
        
        # Initialize parameters from kwargs
        {% for param in parameters %}
        self.state.{{ param.name }} = kwargs.get('{{ param.name }}', {{ param.default_value }})
        {% endfor %}

    def timeAdvance(self):
        """Return time until next internal transition"""
        return INFINITY if self.state.data_to_send is None else 0.0
        
    def intTransition(self):
        """Handle internal transition"""
        self.state.data_to_send = None
        self.state.output_port = None
        return self.state

    def extTransition(self, inputs):
        """Handle external transition"""
        received_data = None
        for port_name, port_value in inputs.items():
            print(f"[{self.name}] Received data on {port_name}: {port_value}")
            received_data = port_value
            
        # Process data for controller
        if received_data is not None:
            # Extract data from received message
            if isinstance(received_data, dict) and 'm2m:cin' in received_data:
                content = received_data['m2m:cin'].get('con', '')
                parts = content.split(',')
                if len(parts) > 2:
                    try:
                        # Extract value - Note: This extraction should be configurable 
                        # based on the message format defined in the model
                        value = float(parts[2].strip())
                        
                        # Apply model-defined conditions 
                        {{ condition_logic }}
                            
                    except (ValueError, IndexError):
                        print(f"[{self.name}] Error parsing value from: {content}")
        return self.state

    def outputFnc(self):
        """Generate output"""
        result = {}
        if hasattr(self.state, 'data_to_send') and self.state.data_to_send is not None and self.state.output_port:
            port = getattr(self, self.state.output_port)
            result[port] = self.state.data_to_send
        return result

    def __lt__(self, other):
        """Comparison method required for sorting during simulation"""
        return self.name < other.name
