from pypdevs.simulator import Simulator
from model import IoTNodeModel
import logging


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    
    logging.debug("Starting the model")
    
    model = IoTNodeModel()
    logging.debug("Model Loaded")
    
    sim = Simulator(model)
    logging.debug("Simulator Loaded")
    
    sim.setClassicDEVS()
    logging.debug("Classic DEVS set")
    
    sim.setVerbose()
    logging.debug("Verbose mode set")
    
    sim.setTerminationTime(86400) # 24 hours
    logging.debug("Termination time set")
    
    logging.debug("Starting simulation")
    sim.simulate()
    logging.debug("Simulation finished")