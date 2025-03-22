from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class Sink(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Sink")
        self.inport = self.addInPort("in")

    def extTransition(self, inputs):
        received_data = inputs[self.inport]
        print(f"Sink received: {received_data}")
        return self