from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class OneM2MInterfaceState:
    def __init__(self):
        self.processing_time = 0.0 
        self.data_to_send = None

class OneM2MInterface(AtomicDEVS):
    def __init__(self, simulated_delay=1.0):
        AtomicDEVS.__init__(self, "OneM2MInterface")
        self.simulated_delay = simulated_delay
        self.state = OneM2MInterfaceState()
        self.timeLast = 0.0 
        self.inport = self.addInPort("in")
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        if self.state.data_to_send is None:
            return INFINITY
        return self.state.processing_time - self.timeLast

    def extTransition(self, inputs):
        self.state.data_to_send = inputs[self.inport]
        self.state.processing_time = self.timeLast + self.simulated_delay
        return self.state

    def outputFnc(self):
        sensor_data = self.state.data_to_send
        subscription_data = {
            "m2m:sgn": {
                "m2m:nev": {
                    "m2m:rep": {
                        "m2m:cin": {
                            "con": sensor_data["m2m:cin"]["con"],
                            "ri": "cin7124901579521707503",
                            "pi": "cnt8702778900039637980",
                            "rn": "cin_UKmyMwKBXt",
                            "ct": "20231207T061300,532674",
                            "lt": "20231207T061300,532674",
                            "ty": 4,
                            "cs": len(sensor_data["m2m:cin"]["con"]),
                            "st": 1,
                            "et": "20281205T061300,414361"
                        }
                    },
                    "net": 3
                },
                "sur": "/id-in/sub2711006235793759306"
            }
        }
        self.state.data_to_send = None
        print(f"OneM2M Interface simulated sending: {subscription_data}")
        return {self.outport: subscription_data}

    def intTransition(self):
        self.timeLast = self.state.processing_time
        self.state.processing_time = INFINITY
        return self.state