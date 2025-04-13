import json
import os
import sys
import datetime
from pathlib import Path
import shutil
import tempfile

from generator.model_generator import (
    generate_component_class,
    generate_coupled_model,
    save_model_json
)

def ensure_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_pydevs_model(json_file_path, output_dir=None):
    """
    Generate PyDEVS model from JSON specification
    
    Args:
        json_file_path: Path to JSON model specification
        output_dir: Output directory for PyDEVS files (optional)
        
    Returns:
        str: Path to the output directory
    """
    try:
        with open(json_file_path, 'r') as f:
            model_json = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON model: {e}")
        return None
    
    # Create output directory with timestamp if not provided
    if output_dir is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"pydevs_FirstProgram_{timestamp}"
    
    # Create the directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save a copy of the original JSON model for reference
    model_json_path = os.path.join(output_dir, "model.json")
    save_model_json(model_json, model_json_path)
    
    # Generate component files
    components = model_json['components']
    component_files = []
    
    for component in components:
        component_name = component['name']
        component_file = component_name.lower().replace(' ', '_')
        component_path = os.path.join(output_dir, f"{component_file}.py")
        component_files.append(component_file)
        
        # Generate component code, passing the full model_json for context
        component_code = generate_component_class(component, model_json)
        
        # Write to file
        with open(component_path, 'w') as f:
            f.write(component_code)
        
        print(f"Generated component: {component_name} -> {component_path}")
    
    # Generate the coupled model
    model_code = generate_coupled_model(model_json, component_files)
    model_path = os.path.join(output_dir, "model.py")
    
    with open(model_path, 'w') as f:
        f.write(model_code)
    
    print(f"Generated coupled model: {model_path}")
    
    # Generate simulation script
    generate_simulation_script(output_dir)
    
    return output_dir

def generate_simulation_script(output_dir):
    """Generate simulation script for running the model"""
    sim_script = """
import sys
import os
import random
import time

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pypdevs.simulator import Simulator
from model import GeneratedModel

# Create the model
model = GeneratedModel()

# Create the simulator
sim = Simulator(model)

# Configure the simulation
sim.setTerminationTime(1000.0)  # Run for 1000 time units
sim.setClassicDEVS()  # Use classic DEVS formalism

# Use the correct setVerbose syntax for your PyDEVS version
# It expects either None or a string filename, not a boolean
sim.setVerbose(None)  # No additional verbosity

# Redirect stdout to capture log
log_file = 'simulation.log'
original_stdout = sys.stdout
try:
    with open(log_file, 'w') as f:
        sys.stdout = f
        # Run the simulation
        sim.simulate()
finally:
    # Restore stdout
    sys.stdout = original_stdout

print(f"Simulation complete. Results saved to {log_file}")
"""
    
    sim_path = os.path.join(output_dir, "simulate.py")
    with open(sim_path, 'w') as f:
        f.write(sim_script)
    
    print(f"Generated simulation script: {sim_path}")
    
    # Create optional experiment script for convenience
    exp_script = """
import os
import subprocess
import sys

print("Running simulation...")

# Run the simulation
try:
    # First try to run with python command
    result = subprocess.run(['python', 'simulate.py'], capture_output=True, text=True)
    if result.returncode != 0 and sys.executable:
        # If that fails, try with the current Python interpreter
        print("Trying with current Python executable...")
        result = subprocess.run([sys.executable, 'simulate.py'], capture_output=True, text=True)
except Exception as e:
    print(f"Error running simulation: {e}")
    sys.exit(1)

# Print output
print("\\nSimulation output:")
print(result.stdout)

if result.stderr:
    print("\\nErrors:")
    print(result.stderr)

# Open the log file
try:
    with open('simulation.log', 'r') as f:
        log_content = f.read()
        print("\\nSimulation Log Preview (first 1000 chars):")
        print(log_content[:1000])
        print("\\n...\\n")
except FileNotFoundError:
    print("Simulation log file not found.")

print("To view full log, open 'simulation.log'")
"""
    
    exp_path = os.path.join(output_dir, "experiment.py")
    with open(exp_path, 'w') as f:
        f.write(exp_script)
    
    print(f"Generated experiment helper: {exp_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generator.py <config_file> [output_dir]")
        sys.exit(1)
    
    config_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None
    
    generate_pydevs_model(config_file, output_dir)
