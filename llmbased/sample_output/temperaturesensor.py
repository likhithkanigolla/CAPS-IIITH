from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class TemperatureSensorState:
    def __init__(self):
        self.Temperature = 0.0
        self.TemperatureTimer_next = 0.0
        self.data_to_send = None
        self.output_port = None
        self.received_value = None


class TemperatureSensor(AtomicDEVS):
    def __init__(self, name="TemperatureSensor", **kwargs):
        AtomicDEVS.__init__(self, name)
        self.state = TemperatureSensorState()
        self.timeLast = 0.0
        
        # Initialize ports
        self.out_0 = self.addOutPort("out_0")
        self.out_1 = self.addOutPort("out_1")
        
        # Initialize parameters
        self.state.Temperature = kwargs.get('Temperature', 0.0)

        # Initialize timers
        self.state.TemperatureTimer_next = 10.0

    def timeAdvance(self):
        """Return time until next internal transition"""
                # Check if there's data to send immediately
        if self.state.data_to_send is not None:
            return 0.0
        
        next_time = INFINITY
        if hasattr(self.state, 'TemperatureTimer_next'):
            next_time = min(next_time, self.state.TemperatureTimer_next - self.timeLast)
        return next_time
        
    def intTransition(self):
        """Handle internal transition"""
        if hasattr(self.state, 'TemperatureTimer_next') and self.state.TemperatureTimer_next <= self.timeLast:
            self.state.TemperatureTimer_next = self.timeLast + 10.0
        self.state.data_to_send = None
        return self.state

    def extTransition(self, inputs):
        """Handle external transition"""
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        return self.state

    def outputFnc(self):
        """Generate output"""
        result = {}
        # Generate sensor data
        sensor_data = {
            "m2m:cin": {
                "lbl": [
                    f"{self.name}"
                ],
                "con": f"{self.name}, {int(time.time())}, {random.uniform(0, 100)}"
            }
        }
        # Send to all output ports
        for port_name in dir(self):
            if port_name.startswith('out_'):
                port = getattr(self, port_name)
                result[port] = sensor_data
        return result

    def __lt__(self, other):
        """Comparison method required for sorting during simulation"""
        return self.name < other.name

