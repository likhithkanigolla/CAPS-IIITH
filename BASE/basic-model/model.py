from pypdevs.DEVS import CoupledDEVS

from water_quality_node import WaterQualitySensor
from onem2m_interface import OneM2MInterface
from sink import Sink

class WaterQualityModel(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "WaterQualityModel")
        print("Model Loaded")

        print("Initializing Water Quality Sensor")
        self.sensor = self.addSubModel(WaterQualitySensor("WM-WD-KH98-00", data_interval=3600)) # 1 hour
        
        print("Initializing OneM2M Interface")
        self.onem2m = self.addSubModel(OneM2MInterface(simulated_delay=1))
        
        print("Initializing Sink")
        self.sink = self.addSubModel(Sink())
        
        print("Connecting Sensor's outport to OneM2M Interface's inport")
        self.connectPorts(self.sensor.outport, self.onem2m.inport)
        
        print("Connecting OneM2M Interface's outport to Sink's inport")
        self.connectPorts(self.onem2m.outport, self.sink.inport)
        
        print("Model initialization complete")