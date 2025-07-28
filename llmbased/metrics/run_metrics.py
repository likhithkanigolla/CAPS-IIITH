#!/usr/bin/env python3
"""
Run metrics collection on one or more model directories.
"""

import os
import sys
import argparse
import glob
import time
from metrics_collector import MetricsCollector

def run_metrics_collection(args):
    """Run metrics collection based on command line arguments"""
    collector = MetricsCollector(args.output_dir)
    
    # Process each model directory
    for model_pattern in args.model_dirs:
        # Expand glob patterns
        model_dirs = glob.glob(model_pattern)
        
        if not model_dirs:
            print(f"Warning: No directories match pattern '{model_pattern}'")
            continue
        
        for model_dir in model_dirs:
            if not os.path.isdir(model_dir):
                print(f"Skipping '{model_dir}': Not a directory")
                continue
                
            # Normalize the path to avoid duplicate directory issues
            model_dir = os.path.normpath(model_dir)
            
            print(f"\nProcessing model: {model_dir}")
            
            # Simulation metrics
            if args.simulation:
                collector.measure_simulation_runtime(model_dir, args.iterations)
            
            # Code statistics
            if args.code_stats:
                collector.collect_code_stats(model_dir)
            
            # Visualization metrics
            if args.visualization:
                collector.generate_visualization_metrics_script(model_dir)
                print(f"Visualization metrics script generated for {model_dir}")
                print("Open the index.html file in a browser to collect visualization metrics")
    
    # Generate final report
    report_path = collector.generate_report()
    print(f"\nCollection complete! Report generated at: {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Collect performance metrics for PyDEVS models")
    
    parser.add_argument("model_dirs", nargs="+", help="Path(s) to model directories (glob patterns supported)")
    parser.add_argument("--output-dir", "-o", default="metrics_results", help="Directory to store metrics results")
    parser.add_argument("--iterations", "-i", type=int, default=20, help="Number of iterations for simulation runtime measurement")
    
    # What to measure
    parser.add_argument("--simulation", action="store_true", help="Measure simulation runtime and memory usage")
    parser.add_argument("--code-stats", action="store_true", help="Collect code generation statistics")
    parser.add_argument("--visualization", action="store_true", help="Generate visualization metrics scripts")
    parser.add_argument("--all", "-a", action="store_true", help="Enable all metrics")
    
    args = parser.parse_args()
    
    # If --all is specified, enable all metrics
    if args.all:
        args.simulation = True
        args.code_stats = True
        args.visualization = True
    
    # If no metrics specified, enable all
    if not any([args.simulation, args.code_stats, args.visualization]):
        args.simulation = True
        args.code_stats = True
        args.visualization = True
        
    run_metrics_collection(args)

if __name__ == "__main__":
    main()
