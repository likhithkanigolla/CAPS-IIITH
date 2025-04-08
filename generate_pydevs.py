#!/usr/bin/env python3
import os
import sys
import argparse
from generator.file_generators import generate_pydevs_from_saml

def main():
    parser = argparse.ArgumentParser(description='Generate PyDEVS files from SAML models')
    parser.add_argument('saml_file', help='Path to the SAML (.capssaml) file')
    parser.add_argument('--hwml', dest='hwml_file', help='Optional path to HWML file for hardware details')
    parser.add_argument('--output-dir', dest='output_dir', help='Directory where PyDEVS files will be generated')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Enable debug output if verbose flag is set
    if args.verbose:
        os.environ['DEBUG'] = '1'
    
    # Validate input file
    if not os.path.exists(args.saml_file):
        print(f"Error: SAML file not found: {args.saml_file}")
        return 1
    
    # Validate HWML file if provided
    if args.hwml_file and not os.path.exists(args.hwml_file):
        print(f"Warning: HWML file not found: {args.hwml_file}")
    
    # Create output directory if not exists
    if args.output_dir and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    try:
        print(f"Generating PyDEVS files from SAML: {args.saml_file}")
        generated_files = generate_pydevs_from_saml(
            args.saml_file,
            args.hwml_file,
            args.output_dir
        )
        
        print(f"Successfully generated {len(generated_files)} files:")
        for filename in generated_files:
            print(f"  - {filename}")
        
        return 0
    except Exception as e:
        print(f"Error generating PyDEVS files: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
