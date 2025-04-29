from pypdevs.DEVS import CoupledDEVS
from temperaturesensor import TemperatureSensor
from server import Server
from controller import Controller
from windowactuator import WindowActuator
class GeneratedModel(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "GeneratedModel")
        print("Model Loading...")
        
        # Initialize components
        self.c1 = self.addSubModel(TemperatureSensor("c1"))
        print("Initialized TemperatureSensor as c1")
        self.c2 = self.addSubModel(Server("c2"))
        print("Initialized Server as c2")
        self.c3 = self.addSubModel(Controller("c3"))
        print("Initialized Controller as c3")
        self.c4 = self.addSubModel(WindowActuator("c4"))
        print("Initialized WindowActuator as c4")

        # Connect components
        self.connectPorts(self.c1.out_0, self.c2.in_0)
        print("Connected c1.out_0 to c2.in_0")
        self.connectPorts(self.c1.out_1, self.c3.in_0)
        print("Connected c1.out_1 to c3.in_0")
        self.connectPorts(self.c3.out_1, self.c4.in_1)
        print("Connected c3.out_1 to c4.in_1")
        self.connectPorts(self.c3.out_0, self.c4.in_0)
        print("Connected c3.out_0 to c4.in_0")

        print("Model initialization complete")
