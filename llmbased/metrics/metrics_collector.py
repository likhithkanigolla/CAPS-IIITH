import os
import time
import json
import psutil
import subprocess
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MetricsCollector:
    def __init__(self, output_dir="metrics_results"):
        """Initialize the metrics collector"""
        self.results = {
            "simulation_metrics": [],
            "code_generation_stats": [],
            "llm_processing_time": []
        }
        
        # Create output directory if it doesn't exist
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Initialize results file path with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_file = os.path.join(output_dir, f"metrics_{timestamp}.json")
        
    def measure_simulation_runtime(self, model_dir, iterations=3):
        """Measure simulation runtime and memory usage"""
        print(f"Measuring simulation runtime for {model_dir}...")
        
        # Normalize the path to avoid duplicate directory issues
        model_dir = os.path.normpath(model_dir)
        
        # Find the simulation script
        sim_script = os.path.join(model_dir, "experiment.py")
        if not os.path.exists(sim_script):
            sim_script = os.path.join(model_dir, "experiment.py")
            if not os.path.exists(sim_script):
                print(f"Error: Simulation script not found in {model_dir}")
                print(f"Searched for: {os.path.join(model_dir, 'experiment.py')} and {os.path.join(model_dir, 'experiment.py')}")
                return None
        
        print(f"Using simulation script: {sim_script}")
        
        # Run the simulation multiple times and collect metrics
        results = []
        for i in range(iterations):
            print(f"  Run {i+1}/{iterations}...")
            
            # Start process monitoring
            process = psutil.Process(os.getpid())
            mem_before = process.memory_info().rss / 1024 / 1024  # Memory in MB
            
            # Time the simulation
            start_time = time.time()
            
            # Run the simulation in a subprocess
            result = subprocess.run(
                [sys.executable, os.path.basename(sim_script)],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(sim_script)  # Use the directory of the script as working directory
            )
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # Get memory usage after simulation
            mem_after = process.memory_info().rss / 1024 / 1024  # Memory in MB
            mem_used = max(0.01, mem_after - mem_before)  # Ensure positive value
            
            # Log the results
            run_result = {
                "iteration": i+1,
                "runtime_seconds": elapsed_time,
                "memory_usage_mb": mem_used,
                "success": result.returncode == 0
            }
            
            if result.returncode != 0:
                run_result["error"] = result.stderr
                print(f"  Error during run {i+1}: {result.stderr}")
            else:
                print(f"  Run {i+1} completed successfully: {elapsed_time:.2f}s, {mem_used:.2f}MB")
                
            results.append(run_result)
            
            # Let system stabilize between runs
            time.sleep(1)
        
        # Calculate averages
        successful_runs = [r for r in results if r["success"]]
        if successful_runs:
            avg_runtime = sum(r["runtime_seconds"] for r in successful_runs) / len(successful_runs)
            avg_memory = sum(r["memory_usage_mb"] for r in successful_runs) / len(successful_runs)
        else:
            avg_runtime = 0
            avg_memory = 0
        
        # Save the metrics
        metrics = {
            "model_dir": model_dir,
            "model_name": os.path.basename(model_dir.rstrip('/')),
            "iterations": iterations,
            "avg_runtime_seconds": avg_runtime,
            "avg_memory_usage_mb": avg_memory,
            "details": results,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.results["simulation_metrics"].append(metrics)
        self._save_results()
        
        # Print immediate feedback
        print(f"  Average runtime: {avg_runtime:.2f} seconds")
        print(f"  Average memory: {avg_memory:.2f} MB")
        
        return metrics

    def collect_code_stats(self, model_dir):
        """Collect statistics about generated code"""
        print(f"Collecting code statistics for {model_dir}...")
        
        if not os.path.exists(model_dir):
            print(f"Error: Model directory not found at {model_dir}")
            return None
        
        # Stats to collect
        stats = {
            "model_dir": model_dir,
            "model_name": os.path.basename(model_dir),
            "atomic_devs_count": 0,
            "coupled_devs_count": 0,
            "total_files": 0,
            "total_lines": 0,
            "files_breakdown": [],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Process each Python file
        for file in os.listdir(model_dir):
            if file.endswith(".py"):
                file_path = os.path.join(model_dir, file)
                
                # Count lines
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.count('\n') + 1
                
                # Check for DEVS classes
                atomic_count = content.count("AtomicDEVS")
                coupled_count = content.count("CoupledDEVS")
                
                # Add to stats
                stats["total_files"] += 1
                stats["total_lines"] += lines
                stats["atomic_devs_count"] += atomic_count
                stats["coupled_devs_count"] += coupled_count
                
                stats["files_breakdown"].append({
                    "filename": file,
                    "lines": lines,
                    "atomic_devs": atomic_count,
                    "coupled_devs": coupled_count
                })
        
        self.results["code_generation_stats"].append(stats)
        self._save_results()
        
        return stats
    
    def record_llm_processing_time(self, task_name, start_time, end_time, tokens_in=None, tokens_out=None, additional_info=None):
        """Record the processing time for an LLM task"""
        elapsed_time = end_time - start_time
        
        record = {
            "task_name": task_name,
            "start_time": datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_seconds": elapsed_time,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if tokens_in is not None:
            record["tokens_in"] = tokens_in
        
        if tokens_out is not None:
            record["tokens_out"] = tokens_out
        
        if additional_info is not None:
            record["additional_info"] = additional_info
        
        self.results["llm_processing_time"].append(record)
        self._save_results()
        
        return record
    
    def generate_visualization_metrics_script(self, model_dir):
        """Generate a JavaScript file to measure visualization performance"""
        print(f"Generating visualization metrics script for {model_dir}...")
        
        # Create visualization metrics directory in model_dir if it doesn't exist
        vis_metrics_dir = os.path.join(model_dir, "vis_metrics")
        if not os.path.exists(vis_metrics_dir):
            os.makedirs(vis_metrics_dir)
        
        # Path to the metrics JavaScript file
        metrics_js_path = os.path.join(vis_metrics_dir, "performance_metrics.js")
        
        # Content for the JavaScript metrics file
        js_content = """// Visualization Performance Metrics Script
console.log('Loading visualization metrics...');

// Performance metrics
const performanceMetrics = {
    loadStart: performance.now(),
    loadEnd: null,
    renderStart: null,
    renderEnd: null,
    framesCount: 0,
    lastFrameTime: null,
    frameTimes: [],
    events: []
};

// Record when the page is fully loaded
window.addEventListener('load', () => {
    performanceMetrics.loadEnd = performance.now();
    
    console.log(`Page load time: ${(performanceMetrics.loadEnd - performanceMetrics.loadStart).toFixed(2)}ms`);
    
    // Start tracking frame rate
    requestAnimationFrame(trackFrameRate);
    
    // Add event for simulation start
    const startBtn = document.getElementById('start-sim-btn');
    if (startBtn) {
        const originalClick = startBtn.onclick;
        startBtn.onclick = function(e) {
            performanceMetrics.events.push({
                type: 'simulation_start',
                time: performance.now()
            });
            console.log('Simulation started');
            return originalClick ? originalClick.call(this, e) : true;
        };
    }
    
    // Add event for simulation stop
    const stopBtn = document.getElementById('stop-sim-btn');
    if (stopBtn) {
        const originalClick = stopBtn.onclick;
        stopBtn.onclick = function(e) {
            performanceMetrics.events.push({
                type: 'simulation_stop',
                time: performance.now()
            });
            console.log('Simulation stopped');
            return originalClick ? originalClick.call(this, e) : true;
        };
    }
    
    // Save metrics to localStorage every 5 seconds
    setInterval(saveMetrics, 5000);
});

// Track frame rate
function trackFrameRate(timestamp) {
    if (performanceMetrics.lastFrameTime !== null) {
        const frameTime = timestamp - performanceMetrics.lastFrameTime;
        performanceMetrics.frameTimes.push(frameTime);
        
        // Keep only the last 100 frame times to avoid memory growth
        if (performanceMetrics.frameTimes.length > 100) {
            performanceMetrics.frameTimes.shift();
        }
    }
    
    performanceMetrics.lastFrameTime = timestamp;
    performanceMetrics.framesCount++;
    
    requestAnimationFrame(trackFrameRate);
}

// Save metrics to localStorage
function saveMetrics() {
    const now = new Date();
    
    // Calculate averages
    let avgFrameTime = 0;
    if (performanceMetrics.frameTimes.length > 0) {
        avgFrameTime = performanceMetrics.frameTimes.reduce((a, b) => a + b, 0) / performanceMetrics.frameTimes.length;
    }
    
    const metrics = {
        timestamp: now.toISOString(),
        pageLoadTime: performanceMetrics.loadEnd - performanceMetrics.loadStart,
        averageFrameTime: avgFrameTime,
        fps: avgFrameTime > 0 ? 1000 / avgFrameTime : 0,
        totalFrames: performanceMetrics.framesCount,
        events: performanceMetrics.events
    };
    
    // Save to localStorage
    localStorage.setItem('visualizationMetrics', JSON.stringify(metrics));
    console.log('Metrics saved:', metrics);
}

// Export metrics
window.getVisualizationMetrics = function() {
    return {
        pageLoadTime: performanceMetrics.loadEnd - performanceMetrics.loadStart,
        averageFrameTime: performanceMetrics.frameTimes.length > 0 ? 
            performanceMetrics.frameTimes.reduce((a, b) => a + b, 0) / performanceMetrics.frameTimes.length : 0,
        totalFrames: performanceMetrics.framesCount,
        events: performanceMetrics.events
    };
};

// Inject a button to download metrics
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.control-buttons');
    if (container) {
        const downloadBtn = document.createElement('button');
        downloadBtn.innerText = 'Download Metrics';
        downloadBtn.onclick = function() {
            const metrics = localStorage.getItem('visualizationMetrics');
            const blob = new Blob([metrics], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'visualization_metrics.json';
            a.click();
            
            URL.revokeObjectURL(url);
        };
        container.appendChild(downloadBtn);
    }
});

console.log('Visualization metrics loaded');
"""
        
        # Write the JavaScript file
        with open(metrics_js_path, 'w') as f:
            f.write(js_content)
        
        # Modify the index.html file to include our script
        index_html_path = os.path.join(model_dir, "index.html")
        if os.path.exists(index_html_path):
            with open(index_html_path, 'r') as f:
                html_content = f.read()
            
            # Check if our script is already included
            if "performance_metrics.js" not in html_content:
                # Insert our script before the closing body tag
                html_content = html_content.replace(
                    "</body>",
                    f'    <script src="vis_metrics/performance_metrics.js"></script>\n</body>'
                )
                
                # Write the modified HTML
                with open(index_html_path, 'w') as f:
                    f.write(html_content)
                
                print(f"Added performance metrics script to {index_html_path}")
            else:
                print(f"Performance metrics script already included in {index_html_path}")
        else:
            print(f"Warning: index.html not found at {index_html_path}")
        
        return metrics_js_path
    
    def _save_results(self):
        """Save the current results to a JSON file"""
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
            
    def generate_report(self):
        """Generate a human-readable report of the collected metrics"""
        report_path = os.path.join(self.output_dir, "metrics_report.md")
        
        with open(report_path, 'w') as f:
            f.write("# Metrics Report\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Simulation metrics
            f.write("## Simulation Runtime Metrics\n\n")
            if self.results["simulation_metrics"]:
                f.write("| Model | Avg Runtime (s) | Avg Memory (MB) | Iterations |\n")
                f.write("|-------|----------------|-----------------|------------|\n")
                
                for metric in self.results["simulation_metrics"]:
                    model_name = metric.get('model_name', 'simulation_test')
                    runtime = metric.get('avg_runtime_seconds', 0)
                    memory = metric.get('avg_memory_usage_mb', 0)
                    iterations = metric.get('iterations', 0)
                    f.write(f"| {model_name} | {runtime:.2f} | {memory:.2f} | {iterations} |\n")
            else:
                f.write("No simulation metrics collected yet.\n")
            
            # Code generation stats
            f.write("\n## Code Generation Statistics\n\n")
            if self.results["code_generation_stats"]:
                f.write("| Model | Total Files | Total Lines | AtomicDEVS | CoupledDEVS |\n")
                f.write("|-------|-------------|-------------|------------|------------|\n")
                
                for stat in self.results["code_generation_stats"]:
                    f.write(f"| {stat['model_name']} | {stat['total_files']} | {stat['total_lines']} | {stat['atomic_devs_count']} | {stat['coupled_devs_count']} |\n")
            else:
                f.write("No code generation statistics collected yet.\n")
            
            # LLM processing time
            f.write("\n## LLM Processing Time\n\n")
            if self.results["llm_processing_time"]:
                f.write("| Task | Elapsed Time (s) | Tokens In | Tokens Out |\n")
                f.write("|------|-----------------|-----------|------------|\n")
                
                for record in self.results["llm_processing_time"]:
                    tokens_in = record.get("tokens_in", "N/A")
                    tokens_out = record.get("tokens_out", "N/A")
                    f.write(f"| {record['task_name']} | {record['elapsed_seconds']:.2f} | {tokens_in} | {tokens_out} |\n")
            else:
                f.write("No LLM processing times recorded yet.\n")
            
            f.write("\n\n*Raw data available in the metrics JSON file.*\n")
        
        print(f"Report generated at {report_path}")
        return report_path


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        model_dir = sys.argv[1]
        collector = MetricsCollector()
        
        # Collect simulation metrics
        collector.measure_simulation_runtime(model_dir)
        
        # Collect code stats
        collector.collect_code_stats(model_dir)
        
        # Generate visualization metrics script
        collector.generate_visualization_metrics_script(model_dir)
        
        # Generate report
        collector.generate_report()
    else:
        print("Usage: python metrics_collector.py <model_directory>")
