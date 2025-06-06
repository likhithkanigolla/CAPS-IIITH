# PyDEVS Metrics Collection Tools

This directory contains tools for collecting performance and analysis metrics for the PyDEVS simulation system.

## Metrics Collected

1. **Simulation Runtime Metrics**
   - Execution time
   - Memory usage
   - Success/failure rate

2. **Code Generation Statistics**
   - Number of AtomicDEVS and CoupledDEVS classes
   - Total lines of code
   - Files generated

3. **LLM Processing Time**
   - Time per step in the LLM processing pipeline
   - Token counts (input and output)

4. **Visualization Performance**
   - Page load time
   - Frames per second
   - Rendering times

## Usage

### Collect Metrics for a Model

```bash
# Run all metrics collection for a specific model
python metrics/run_metrics.py /path/to/model_dir

# Run only specific metrics
python metrics/run_metrics.py --simulation --code-stats /path/to/model_dir

# Run with multiple iterations for simulation metrics
python metrics/run_metrics.py --iterations 5 /path/to/model_dir
```

### Measure LLM Processing Time

The LLM processing time metrics can be collected by:

1. Using the `@time_llm_task` decorator on functions:

```python
from metrics.llm_metrics import time_llm_task

@time_llm_task("my_task_name")
def my_function():
    # Function code here
```

2. Using the `TimeLLMTask` context manager for blocks of code:

```python
from metrics.llm_metrics import TimeLLMTask

with TimeLLMTask("task_name", tokens_in=1000) as task:
    # Code to be timed
    result = llm_model.generate()
    task.set_tokens_out(2000)
```

### Visualization Performance Metrics

Visualization metrics are collected in the browser. When you run the metrics collection with the `--visualization` flag, a script is injected into the web visualization. The script automatically collects:

- Page load time
- Rendering performance (frames per second)
- Event timing

To get the metrics:
1. Open the visualization in a browser
2. Click the "Download Metrics" button that appears in the control panel
3. The metrics will be downloaded as a JSON file

## Report Generation

A report in Markdown format is automatically generated after running metrics collection. The report is saved in the output directory (default: `metrics_results`).
