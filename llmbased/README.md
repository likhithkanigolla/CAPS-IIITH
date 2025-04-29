# CAPSSAML to PyDEVS Simulation Generator

This project provides a toolchain for converting CAPSSAML model specifications into PyDEVS simulation models, running simulations, and visualizing the results through an interactive web interface.

## Overview

The CAPS-IIITH LLM-based toolchain enables:

1. Converting CAPSSAML specifications to structured JSON using Gemini AI
2. Generating PyDEVS simulation models from the JSON specification
3. Running simulations to model system behavior
4. Parsing simulation results for analysis
5. Generating interactive web visualizations of the system and its behavior

## Installation

### Prerequisites

- Python 3.8+
- Google API key for Gemini AI

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CAPS-IIITH/llmbased
   ```

2. Install dependencies:
   ```bash
   pip install google-generativeai
   ```

3. Set up your Google API key:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage

```bash
python capssaml_to_pydevs.py <capssaml_file_path> [output_directory] [system_instructions_path]
```

Or using the main script:

```bash
python main.py <capssaml_file_path> [output_directory] [system_instructions_path]
```

### Parameters

- `capssaml_file_path`: Path to the input CAPSSAML file
- `output_directory` (optional): Directory to save generated files (defaults to timestamp-based directory)
- `system_instructions_path` (optional): Path to custom system instructions for the LLM (defaults to built-in instructions)

## Project Structure

- `main.py`: Core workflow and processing functions
- `capssaml_to_pydevs.py`: Command-line interface for the toolchain
- `generator/`: PyDEVS model generation code
  - `generator.py`: Main model generation orchestration
  - `model_generator.py`: Component code generation
- `parser/`: Simulation output processing
  - `generic_parser.py`: Parses PyDEVS simulation logs
  - `parser.py`: CLI for the parser
- `web/`: Web visualization generation
  - `web_generator.py`: Generates HTML, CSS, and JS for visualization

## Process Flow

1. **CAPSSAML Parsing**: The input CAPSSAML file is processed by the Gemini AI model to extract structured information into a JSON format.
2. **Model Generation**: The JSON specification is used to generate Python code for PyDEVS atomic and coupled models.
3. **Simulation**: The generated models are executed using the PyDEVS simulation framework.
4. **Result Parsing**: Simulation logs are parsed to extract event and data flow information.
5. **Visualization**: An interactive web interface is generated to visualize the system components, connections, and simulation behavior.

## Web Visualization Features

The generated web visualization includes:

- Interactive system diagram showing components and connections
- Color-coded components based on their roles (sensor, controller, actuator, etc.)
- Simulation playback controls (start, stop, restart)
- Data flow animation showing messages passing between components
- Event log tracking simulation progress
- Component state visualization

## Examples

A sample usage workflow:

```bash
# Generate PyDEVS model and run simulation
python main.py testing/example.capssaml output_dir

# The generated files will be in the output_dir directory
# - PyDEVS model files (.py)
# - Simulation output (simulation.log)
# - Web visualization (index.html, style.css, script.js)

# View the visualization by opening output_dir/index.html in a browser
```

## Component Types

The system supports modeling of different component types:

- **Sensors**: Generate data from external sources
- **Controllers**: Process data and make decisions
- **Actuators**: Perform actions based on controller decisions
- **Servers/Databases**: Store or process data

## License

[Include license information here]