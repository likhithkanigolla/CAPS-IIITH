import os
import sys
import datetime
import shutil

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.component_extraction import extract_components
from generator.file_generators import (
    generate_actuator_file,
    generate_controller_file,
    generate_sensor_file,
    generate_interface_file,
    generate_sink_file,
    generate_model_file,
    generate_experiment_file,
    generate_readme_file
)
from generator.debug_utils import debug_print, log_exception
from parse_connections import parse_connections

def generate_pydevs_files(saml_file_path=None, hwml_file_path=None):
    """Main function to generate PyDEVS files from XML input."""
    debug_print(f"Starting PyDEVS file generation - SAML: {saml_file_path}, HWML: {hwml_file_path}")
    try:
        # Extract components and connections
        components = extract_components(saml_file_path, hwml_file_path)
        debug_print(f"Extracted {len(components)} components")
        
        if not components:
            debug_print("No components found in the XML files. Exiting.")
            print("No components found in the XML files.")
            return False
        
        # Get connections from both files if available
        connections = []
        try:
            if saml_file_path:
                debug_print(f"Parsing connections from SAML file: {saml_file_path}")
                saml_connections = parse_connections(saml_file_path)
                debug_print(f"Found {len(saml_connections)} connections in SAML file")
                connections.extend(saml_connections)
            
            if hwml_file_path:
                debug_print(f"Parsing connections from HWML file: {hwml_file_path}")
                hwml_connections = parse_connections(hwml_file_path)
                debug_print(f"Found {len(hwml_connections)} connections in HWML file")
                connections.extend(hwml_connections)
        except Exception as e:
            log_exception(e)
            debug_print("Error occurred while parsing connections. Exiting.")
            return False
        
        debug_print(f"Total connections: {len(connections)}")
        
        # Create timestamped output directory
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"/Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/generated_{timestamp}"
            os.makedirs(output_dir, exist_ok=True)
            debug_print(f"Created output directory: {output_dir}")
        except Exception as e:
            log_exception(e)
            debug_print("Error occurred while creating output directory. Exiting.")
            return False
        
        # Generate files for each component
        generated_files = []
        for component in components:
            debug_print(f"Processing component: {component['name']} (Type: {component['type']})")
            try:
                if component['type'] == 'sensor':
                    filename = generate_sensor_file(component, output_dir)
                elif component['type'] == 'actuator':
                    filename = generate_actuator_file(component, output_dir)
                elif component['type'] == 'controller':
                    filename = generate_controller_file(component, output_dir)
                else:
                    filename = generate_interface_file(component, output_dir)
                generated_files.append(filename)
            except Exception as e:
                log_exception(e)
                debug_print(f"Error generating file for component: {component['name']}")
        
        # Generate sink
        try:
            sink_file = generate_sink_file(output_dir)
            generated_files.append(sink_file)
        except Exception as e:
            log_exception(e)
            debug_print("Error generating sink file.")
        
        # Generate model
        try:
            model_file = generate_model_file(components, connections, output_dir)
            generated_files.append(model_file)
        except Exception as e:
            log_exception(e)
            debug_print("Error generating model file.")
        
        # Generate experiment
        try:
            exp_file = generate_experiment_file(output_dir)
            generated_files.append(exp_file)
        except Exception as e:
            log_exception(e)
            debug_print("Error generating experiment file.")
        
        # Generate README
        try:
            readme_file = generate_readme_file(components, connections, saml_file_path, hwml_file_path, output_dir)
            generated_files.append(readme_file)
        except Exception as e:
            log_exception(e)
            debug_print("Error generating README file.")
        
        # Copy input files for reference
        try:
            if saml_file_path:
                shutil.copy(saml_file_path, os.path.join(output_dir, os.path.basename(saml_file_path)))
                generated_files.append(os.path.basename(saml_file_path))
                debug_print(f"Copied SAML file to output directory: {os.path.basename(saml_file_path)}")
            if hwml_file_path:
                shutil.copy(hwml_file_path, os.path.join(output_dir, os.path.basename(hwml_file_path)))
                generated_files.append(os.path.basename(hwml_file_path))
                debug_print(f"Copied HWML file to output directory: {os.path.basename(hwml_file_path)}")
        except Exception as e:
            log_exception(e)
            debug_print("Error copying input files to output directory.")
        
        if not generated_files:
            debug_print("No files were generated. Exiting.")
            print("No files were generated.")
            return False
        
        print(f"Successfully generated PyDEVS files in {output_dir}:")
        for file in generated_files:
            print(f" - {file}")
        
        debug_print("PyDEVS file generation complete")
        return True
    
    except Exception as e:
        log_exception(e)
        debug_print("Critical error occurred during PyDEVS file generation. Exiting.")
        return False

def main():
    debug_print("Starting generator script")
    if len(sys.argv) < 2:
        print("Usage: python generator.py <saml_file> [hwml_file]")
        print("You must provide at least a SAML file, and optionally a HWML file")
        sys.exit(1)
    
    saml_file_path = sys.argv[1]
    hwml_file_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    debug_print(f"Input arguments - SAML: {saml_file_path}, HWML: {hwml_file_path}")
    
    if not os.path.exists(saml_file_path):
        print(f"Error: SAML file {saml_file_path} does not exist")
        sys.exit(1)
    
    if hwml_file_path and not os.path.exists(hwml_file_path):
        print(f"Error: HWML file {hwml_file_path} does not exist")
        sys.exit(1)
    
    debug_print("Calling generate_pydevs_files function")
    success = generate_pydevs_files(saml_file_path, hwml_file_path)
    if success:
        print("PyDEVS code generation completed successfully.")
    else:
        print("PyDEVS code generation failed.")
        sys.exit(1)

if __name__ == "__main__":
    debug_print("Executing main function")
    main()