def generate_experiment():
    """Generate experiment code for running the simulation"""
    experiment_code = """from pypdevs.simulator import Simulator
from model import GeneratedModel
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    logging.debug("Starting the model")
    
    model = GeneratedModel()
    logging.debug("Model Loaded")
    
    sim = Simulator(model)
    logging.debug("Simulator Loaded")
    
    sim.setClassicDEVS()
    logging.debug("Classic DEVS set")
    
    sim.setVerbose()
    logging.debug("Verbose mode set")
    
    # Set simulation termination time (default: 24 hours)
    sim.setTerminationTime(86400)
    logging.debug("Termination time set")
    
    logging.debug("Starting simulation")
    sim.simulate()
    logging.debug("Simulation finished")
"""
    return experiment_code
