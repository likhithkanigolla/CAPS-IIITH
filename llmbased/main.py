import os
import sys
import json
import shutil
import tempfile
import re
import datetime
from pathlib import Path
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Import generator modules
from generator.generator import generate_pydevs_model

def read_system_instructions(file_path):
    """Read system instructions from a file"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warning: System instructions file '{file_path}' not found. Using default.")
        return None
    except Exception as e:
        print(f"Error reading system instructions file: {e}")
        return None


def extract_json_from_text(text):
    """Extract JSON from text that might contain other content"""
    # Try direct parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try finding JSON content with regex
    json_pattern = r'({[\s\S]*})'
    matches = re.findall(json_pattern, text)
    
    for potential_json in matches:
        try:
            return json.loads(potential_json)
        except json.JSONDecodeError:
            continue
    
    # If we get here, we couldn't find valid JSON
    return None


def generate_json(input_file_path, output_json_path=None, system_instructions_path=None):
    """
    Generate JSON from a CAPSSAML file using Gemini API
    
    Args:
        input_file_path: Path to the input CAPSSAML file
        output_json_path: Path to save the resulting JSON (optional)
        system_instructions_path: Path to system instructions file (optional)
        
    Returns:
        str: Path to the generated JSON file
    """
    try:
        with open(input_file_path, 'r') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    # Configure the Gemini API with your API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return None
        
    genai.configure(api_key=api_key)

    # Get system instructions from file or use default
    default_instructions_path = os.path.join(os.path.dirname(__file__), "system_instructions.txt")
    system_instructions_path = system_instructions_path or default_instructions_path
    system_instruction = read_system_instructions(system_instructions_path)
    
    if system_instruction is None:
        print("Error: Could not load system instructions. Aborting.")
        return None

    # Create the model instance
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config={
            "temperature": 0.2,  # Lower temperature for more consistent output
            "response_mime_type": "text/plain"
        },
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
        system_instruction=system_instruction
    )
    
    # If output_json_path is not provided, use a temporary file
    if output_json_path is None:
        output_json_path = tempfile.mktemp(suffix='.json')
    
    # Generate content
    print("Sending request to Gemini API...")
    try:
        chat = model.start_chat()
        response = chat.send_message(
            f"Parse this CAPSSAML file and return ONLY valid JSON:\n\n{input_text}"
        )
        
        # Extract only the JSON part from the response
        json_str = response.text
        
        # Debug: Save raw response for inspection
        debug_file = f"{output_json_path}.raw"
        with open(debug_file, 'w') as f:
            f.write(json_str)
        print(f"Raw LLM response saved to: {debug_file}")
        
        # Try to extract JSON from the response
        json_data = extract_json_from_text(json_str)
        
        if json_data:
            # Write the validated JSON to file
            with open(output_json_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            print(f"Generated JSON saved to: {output_json_path}")
            return output_json_path
        else:
            print("Error: Could not extract valid JSON from the LLM response.")
            # Save the raw output for inspection
            with open(output_json_path, 'w') as f:
                f.write(json_str)
            print(f"Raw output saved to: {output_json_path} for debugging")
            return None
            
    except Exception as e:
        print(f"Error during API call or response processing: {e}")
        return None


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
    if len(sys.argv) < 2:
        print("Usage: python main.py <capssaml_file_path> [output_directory] [system_instructions_path]")
        sys.exit(1)
    
    capssaml_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    system_instructions = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Process the file through the entire pipeline
    process_capssaml_file(capssaml_file, output_dir, system_instructions)