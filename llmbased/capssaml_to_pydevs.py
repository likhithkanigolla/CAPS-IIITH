#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile
import datetime
from pathlib import Path

# Import local modules
from main import generate as generate_json
from generator.generator import generate_pydevs_model

def process_capssaml_file(capssaml_file_path, output_dir=None, system_instructions_path=None):
    """
    Process a CAPSSAML file and generate PyDEVS model
    
    Args:
        capssaml_file_path: Path to the CAPSSAML file
        output_dir: Output directory for PyDEVS files (optional)
        system_instructions_path: Path to system instructions file (optional)
        
    Returns:
        str: Path to the output directory containing PyDEVS files
    """
    # Validate input file
    if not os.path.exists(capssaml_file_path):
        print(f"Error: File '{capssaml_file_path}' not found.")
        return None
    
    input_path = Path(capssaml_file_path)
    
    # Create a copy with .txt extension if the file doesn't already have it
    if input_path.suffix.lower() != '.txt':
        print(f"Creating a copy of {input_path.name} with .txt extension")
        txt_file_path = tempfile.mktemp(suffix='.txt')
        shutil.copy2(capssaml_file_path, txt_file_path)
    else:
        txt_file_path = capssaml_file_path
    
    # Step 1: Generate JSON from CAPSSAML file
    print("Generating JSON from CAPSSAML file...")
    json_file_path = generate_json(txt_file_path, None, system_instructions_path)
    
    if json_file_path is None:
        print("Failed to generate JSON. Aborting.")
        return None
    
    # Generate default output directory if not provided
    if output_dir is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = os.path.basename(capssaml_file_path).split('.')[0]
        output_dir = f"pydevs_{file_name}_{timestamp}"
    
    # Step 2: Generate PyDEVS model from JSON
    print("Generating PyDEVS model from JSON...")
    pydevs_output_dir = generate_pydevs_model(json_file_path, output_dir)
    
    # Clean up the temporary txt file if we created one
    if txt_file_path != capssaml_file_path:
        os.remove(txt_file_path)
    
    print(f"\nComplete! PyDEVS model generated successfully in: {pydevs_output_dir}")
    return pydevs_output_dir

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python capssaml_to_pydevs.py <capssaml_file_path> [output_directory] [system_instructions_path]")
        sys.exit(1)
    
    capssaml_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    system_instructions = sys.argv[3] if len(sys.argv) > 3 else None
    
    process_capssaml_file(capssaml_file, output_dir, system_instructions)
