from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class ControllerState:
    def __init__(self):
        self.Close = False
        self.Open = True
        self.data_to_send = None
        self.output_port = None
        self.Temperature = None  # Condition variable from model

class Controller(AtomicDEVS):
    def __init__(self, name="Controller", **kwargs):
        AtomicDEVS.__init__(self, name)
        self.state = ControllerState()
        self.timeLast = 0.0
        
        # Initialize ports
        self.in_0 = self.addInPort("in_0")
        self.out_0 = self.addOutPort("out_0")
        self.out_1 = self.addOutPort("out_1")

        # Initialize parameters
        self.state.Close = kwargs.get('Close', False)
        self.state.Open = kwargs.get('Open', True)

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
                        # Extract value from the message
                        value = float(parts[2].strip())
                        self.state.Temperature = value  # Store in condition variable
                        print(f"[{self.name}] Processing value: {value}")
                        
                        # Apply model-defined conditions
                        if value > 25:
                            self.state.Temperature = True
                            self.state.data_to_send = received_data
                            self.state.output_port = "out_1"
                            print(f"[{self.name}] Temperature {value} > 25: Sending to sendOpen")
                        elif value < 18:
                            self.state.Temperature = True
                            self.state.data_to_send = received_data
                            self.state.output_port = "out_0"
                            print(f"[{self.name}] Temperature {value} < 18: Sending to sendClose")
                        else:
                            # No condition matched
                            self.state.data_to_send = None
                            print(f"[{self.name}] Value {value} is in normal range: No action")
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
