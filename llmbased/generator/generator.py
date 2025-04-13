import json
import os
import sys
import datetime
from generator.model_generator import generate_component_class, generate_coupled_model
from generator.experiment_generator import generate_experiment

def ensure_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_pydevs_model(config_file, output_dir=None):
    """Generate PyDEVS model from configuration file"""
    # Generate output directory based on timestamp if not provided
    if output_dir is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"pydevs_model_{timestamp}"
    
    # Read JSON configuration
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print(f"Loaded configuration from {config_file}")
    
    # Create output directory
    ensure_directory(output_dir)
    
    # Generate component files
    component_files = []
    for component in config['components']:
        filename = f"{component['name'].lower().replace(' ', '_')}.py"
        filepath = os.path.join(output_dir, filename)
        component_files.append(filename.split('.')[0])
        
        with open(filepath, 'w') as f:
            f.write(generate_component_class(component))
        
        print(f"Generated component file: {filepath}")
    
    # Generate model file
    model_file = os.path.join(output_dir, "model.py")
    with open(model_file, 'w') as f:
        f.write(generate_coupled_model(config, component_files))
    
    print(f"Generated model file: {model_file}")
    
    # Generate experiment file
    experiment_file = os.path.join(output_dir, "experiment.py")
    with open(experiment_file, 'w') as f:
        f.write(generate_experiment())
    
    print(f"Generated experiment file: {experiment_file}")
    
    print(f"PyDEVS model generation complete. Output directory: {output_dir}")
    return output_dir

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generator.py <config_file> [output_dir]")
        sys.exit(1)
    
    config_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None
    
    generate_pydevs_model(config_file, output_dir)
