from pypdevs.simulator import Simulator
from pypdevs.DEVS import AtomicDEVS, CoupledDEVS

# Generator model that produces events every 5 time units
class Generator(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.out_port = self.addOutPort("out")
        self.state = 0

    def timeAdvance(self):
        return 5  # Trigger internal transition every 5 units

    def outputFnc(self):
        return {self.out_port: f"Tick {self.state}"}

    def intTransition(self):
        self.state += 1
        return self.state

# Collector model that prints received messages
class Collector(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.in_port = self.addInPort("in")
        self.state = None

    def extTransition(self, inputs):
        message = inputs[self.in_port]
        print(f"[Collector] Received: {message}")
        return self.state

    def timeAdvance(self):
        return float("inf")  # Passive model

# Coupled model connecting generator and collector
class TopModel(CoupledDEVS):
    def __init__(self):
        super().__init__("TopModel")
        self.gen = self.addSubModel(Generator("Generator"))
        self.col = self.addSubModel(Collector("Collector"))
        self.connectPorts(self.gen.out_port, self.col.in_port)

if __name__ == "__main__":
    model = TopModel()
    sim = Simulator(model)
    sim.setVerbose()  # Optional: Shows detailed simulation logs
    sim.setTerminationTime(20)
    sim.simulate()
    print("PyPDEVS test successful!")
