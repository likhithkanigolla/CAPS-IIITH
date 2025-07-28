import os
import sys
import json
import shutil
import tempfile
import re
import datetime
import subprocess
from pathlib import Path
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Import generator modules
from generator.generator import generate_pydevs_model

# Import metrics
try:
    from metrics.llm_metrics import time_llm_task, TimeLLMTask, get_metrics_collector
    METRICS_ENABLED = True
except ImportError:
    # Create dummy implementations if metrics module is not available
    def time_llm_task(task_name=None):
        def decorator(func):
            return func
        return decorator
    
    class TimeLLMTask:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args, **kwargs): pass
        def set_tokens_out(self, *args, **kwargs): pass
    
    def get_metrics_collector():
        return None
    
    METRICS_ENABLED = False

# Add function to display metrics summary
def print_metrics_summary():
    """Print a summary of collected metrics to the console"""
    if not METRICS_ENABLED:
        print("Metrics collection is disabled.")
        return
    
    collector = get_metrics_collector()
    if not collector or not collector.results:
        print("No metrics have been collected yet.")
        return
    
    print("\n===== LLM METRICS SUMMARY =====")
    
    # Print LLM processing time metrics
    if "llm_processing_time" in collector.results and collector.results["llm_processing_time"]:
        print("\nLLM Processing Time:")
        print(f"{'Task':<30} {'Duration (s)':<15} {'Tokens In':<12} {'Tokens Out':<12}")
        print("-" * 70)
        
        for record in collector.results["llm_processing_time"]:
            task_name = record.get("task_name", "Unknown")
            elapsed = record.get("elapsed_seconds", 0)
            tokens_in = record.get("tokens_in", "N/A")
            tokens_out = record.get("tokens_out", "N/A")
            
            print(f"{task_name:<30} {elapsed:<15.2f} {tokens_in:<12} {tokens_out:<12}")
    
    # Print code generation stats if available
    if "code_generation_stats" in collector.results and collector.results["code_generation_stats"]:
        print("\nCode Generation Statistics:")
        for stat in collector.results["code_generation_stats"]:
            print(f"Model: {stat.get('model_name', 'Unknown')}")
            print(f"  Files: {stat.get('total_files', 0)}")
            print(f"  Lines: {stat.get('total_lines', 0)}")
            print(f"  AtomicDEVS: {stat.get('atomic_devs_count', 0)}")
            print(f"  CoupledDEVS: {stat.get('coupled_devs_count', 0)}")
    
    # Print simulation metrics if available
    if "simulation_metrics" in collector.results and collector.results["simulation_metrics"]:
        print("\nSimulation Runtime Metrics:")
        for metric in collector.results["simulation_metrics"]:
            print(f"Model: {metric.get('model_name', 'Unknown')}")
            print(f"  Avg. Runtime: {metric.get('avg_runtime_seconds', 0):.2f} seconds")
            print(f"  Avg. Memory: {metric.get('avg_memory_usage_mb', 0):.2f} MB")
    
    print("\nDetailed metrics saved to:", collector.results_file if hasattr(collector, 'results_file') else "Unknown location")
    print("=====================================\n")

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


@time_llm_task("generate_json")
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
    
    # Count input tokens (approximate)
    tokens_in = len(input_text.split()) * 1.3  # Rough estimate: 1.3 tokens per word
    print(f"Input size: approximately {int(tokens_in)} tokens")

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
        model_name="gemini-2.0-flash",
        generation_config={
            "temperature": 1,  # Lower temperature for more consistent output
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
    start_time = datetime.datetime.now()
    print(f"  Started at: {start_time.strftime('%H:%M:%S')}")
    
    try:
        chat = model.start_chat()
        with TimeLLMTask("llm_api_call", tokens_in=tokens_in) as task:
            response = chat.send_message(
                f"Parse this CAPSSAML file and return ONLY valid JSON:\n\n{input_text}"
            )
            
            # Estimate output tokens
            tokens_out = len(response.text.split()) * 1.3  # Rough estimate
            task.set_tokens_out(tokens_out)
            
            # Print completion time
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"  Completed at: {end_time.strftime('%H:%M:%S')}")
            print(f"  Duration: {duration:.2f} seconds")
            print(f"  Output size: approximately {int(tokens_out)} tokens")
        
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
    start_time = datetime.datetime.now()
    print(f"  Started at: {start_time.strftime('%H:%M:%S')}")
    
    pydevs_output_dir = generate_pydevs_model(json_file_path, output_dir)
    
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"  Completed at: {end_time.strftime('%H:%M:%S')}")
    print(f"  Duration: {duration:.2f} seconds")
    
    # Clean up the temporary txt file if we created one
    if txt_file_path != capssaml_file_path:
        os.remove(txt_file_path)
    
    # Record metrics at the end if metrics are enabled
    if METRICS_ENABLED:
        collector = get_metrics_collector()
        if collector:
            collector.collect_code_stats(pydevs_output_dir)
            collector.generate_visualization_metrics_script(pydevs_output_dir)
            collector.generate_report()
            # Print metrics summary
            print_metrics_summary()
    
    print(f"\nComplete! PyDEVS model generated successfully in: {pydevs_output_dir}")
    return pydevs_output_dir

def run_experiment(script_path):
    """Run the experiment script"""
    print(f"Running generated script: {script_path}")
    experiment_file = os.path.join(script_path, "experiment.py")
    
    start_time = datetime.datetime.now()
    print(f"  Started at: {start_time.strftime('%H:%M:%S')}")
    
    # Run experiment.py in its own directory
    result = subprocess.run(
        ["/Users/likhithkanigolla/IIITH/MS/S1-Course/IS/venv/bin/python", "experiment.py"], 
        capture_output=True, 
        text=True,
        cwd=script_path  # Set the working directory to where the generated files are
    )
    
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"  Completed at: {end_time.strftime('%H:%M:%S')}")
    print(f"  Duration: {duration:.2f} seconds")
    
    print("Output:")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    # If metrics are enabled, record the simulation run
    if METRICS_ENABLED:
        collector = get_metrics_collector()
        if collector:
            # Record this simulation run
            collector.measure_simulation_runtime(script_path, iterations=1)
            # Print updated metrics
            print_metrics_summary()
    
    return result.returncode == 0
        
def run_parser(folder_path):
    """Run the parser on the generated folder"""
    # Construct paths to required files
    model_json_path = os.path.join(folder_path, "model.json")
    log_file_path = os.path.join(folder_path, "simulation.log")
    
    # Verify files exist
    if not os.path.exists(model_json_path):
        print(f"Error: model.json not found at {model_json_path}")
        return False
        
    if not os.path.exists(log_file_path):
        print(f"Error: simulation.log not found at {log_file_path}")
        return False
    
    # Get the absolute path to the parser script
    parser_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parser", "parser.py")
    
    # Run the parser as a subprocess
    print(f"Running parser on: {folder_path}")
    result = subprocess.run(
        [sys.executable, parser_script, folder_path],
        capture_output=True,
        text=True
    )
    
    print("Parser output:")
    print(result.stdout)
    
    if result.stderr:
        print("Parser errors:")
        print(result.stderr)
        return False
    
    # Check if parsed_output.csv was created
    output_csv = os.path.join(folder_path, "parsed_output.csv")
    if os.path.exists(output_csv):
        print(f"Successfully created: {output_csv}")
        return True
    else:
        print("Parser did not create expected output file")
        return False

def generate_web_pages(folder_path):
    """Generate web pages from the parsed output"""
    print(f"Generating web pages for: {folder_path}")
    
    # Ensure we have the absolute path to the folder
    folder_path = os.path.abspath(folder_path)
    
    # First check if model.json exists in the folder
    model_json_path = os.path.join(folder_path, "model.json")
    if not os.path.exists(model_json_path):
        print(f"Error: model.json not found at {model_json_path}")
        
        # Look for any JSON file in the folder
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        if json_files:
            source_json = os.path.join(folder_path, json_files[0])
            print(f"Found alternative JSON file: {source_json}")
            try:
                shutil.copy2(source_json, model_json_path)
                print(f"Copied {source_json} to {model_json_path}")
            except Exception as e:
                print(f"Error copying JSON file: {e}")
                return False
        else:
            print(f"No JSON files found in {folder_path}")
            return False
    
    # Get the path to the web generator script
    webgenerator_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web", "web_generator.py")
    if not os.path.exists(webgenerator_script):
        print(f"Error: web_generator.py not found at {webgenerator_script}")
        return False
    
    # Create a copy of the model.json file for the web generator to use
    web_model_json = os.path.join(folder_path, "model.json")
    
    # Run the web generator script with absolute paths
    print(f"Running web generator on: {web_model_json}")
    
    # Execute the web generator script
    cmd = [
        sys.executable,  # Python executable
        webgenerator_script,  # Path to the web generator script
        web_model_json,  # Path to model.json
        "--output-dir",  # Use output-dir option
        folder_path  # Output to the same folder
    ]
    
    print(f"Executing command: {' '.join(cmd)}")
    
    # Run the command
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        print("Web generator output:")
        print(result.stdout)
        
        if result.stderr:
            print("Web generator errors:")
            print(result.stderr)
    except Exception as e:
        print(f"Error executing web generator: {e}")
        return False
    
    # Check if web files were generated (using the correct filenames from web_generator.py)
    html_path = os.path.join(folder_path, "template.html") 
    css_path = os.path.join(folder_path, "template-styles.css")
    js_path = os.path.join(folder_path, "template-script.js")
    
    # Check files directly
    html_exists = os.path.exists(html_path)
    css_exists = os.path.exists(css_path)
    js_exists = os.path.exists(js_path)
    
    print(f"Checking generated files:")
    print(f"- HTML file: {html_path} exists: {html_exists}")
    print(f"- CSS file: {css_path} exists: {css_exists}")
    print(f"- JS file: {js_path} exists: {js_exists}")
    
    if html_exists and css_exists and js_exists:
        print(f"Web pages successfully generated for: {folder_path}")
        return True
    else:
        # If template.html wasn't created, look for any HTML files that might have been generated
        html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
        if html_files:
            print(f"Found alternate HTML files: {html_files}")
            return True
        
        print(f"Web pages generation failed.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <capssaml_file_path> [output_directory] [system_instructions_path]")
        sys.exit(1)
    
    print("=" * 80)
    print("CAPSSAML to PyDEVS Generator (with Metrics Collection)")
    print("=" * 80)
    print(f"Metrics collection: {'ENABLED' if METRICS_ENABLED else 'DISABLED'}")
    
    capssaml_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    system_instructions = sys.argv[3] if len(sys.argv) > 3 else None
    
    start_time = datetime.datetime.now()
    print(f"Starting process at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Process the file through the entire pipeline
    generated_folder = process_capssaml_file(capssaml_file, output_dir, system_instructions)
    print(f"Generated files are located in: {generated_folder}")
    if os.path.exists(generated_folder):
        # Run the experiment
        sim_success = run_experiment(generated_folder)
        
        # Run the parser on the generated data
        if sim_success:
            parser_success = run_parser(generated_folder)
            
            # Generate web pages from the parsed output
            if parser_success:
                generate_web_pages(generated_folder)
        
        # Print final metrics summary
        if METRICS_ENABLED:
            print("\nFinal Metrics Summary:")
            print_metrics_summary()
    else:
        print(f"Error: {generated_folder} not found.")
    
    end_time = datetime.datetime.now()
    total_duration = (end_time - start_time).total_seconds()
    print(f"Total process completed in {total_duration:.2f} seconds")
    print("=" * 80)