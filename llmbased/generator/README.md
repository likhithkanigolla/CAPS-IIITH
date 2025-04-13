# PyDEVS Model Generator

This tool generates PyDEVS simulation code from JSON configuration files.

## Usage

```bash
python generator.py <config_file.json> <output_directory>
```

## Input Format

The input JSON file should define components, their behavior, and connections between them. See the sample.json file for the expected structure.

## Generated Files

The generator will create:

1. A Python file for each component defined in the JSON
2. A model.py file that connects all components
3. An experiment.py file to run the simulation

## Component Types

The generator supports these component roles:
- sensor: Generates data
- controller: Processes data and makes decisions
- actuator: Performs actions
- server: Stores or processes data

## Example

```bash
python generator.py ../sample.json ../generated_model
```

This will generate PyDEVS simulation code in the `generated_model` directory based on the configuration in `sample.json`.
