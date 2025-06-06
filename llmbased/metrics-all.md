## 1 Single Sensor 
================================================================================
CAPSSAML to PyDEVS Generator (with Metrics Collection)
================================================================================
Metrics collection: ENABLED
Starting process at: 2025-05-13 04:27:37
Creating a copy of speed_sensor.capssaml with .txt extension
Generating JSON from CAPSSAML file...
Input size: approximately 66 tokens
Sending request to Gemini API...
  Started at: 04:27:37
  Completed at: 04:27:41
  Duration: 3.83 seconds
  Output size: approximately 153 tokens
Raw LLM response saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmpym8pa6d3.json.raw
Generated JSON saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmpym8pa6d3.json
Generating PyDEVS model from JSON...
  Started at: 04:27:41
Model JSON saved to: pydevs_speed_sensor_20250513_042741/model.json
Generated component: SpeedSensor -> pydevs_speed_sensor_20250513_042741/speedsensor.py
Generated coupled model: pydevs_speed_sensor_20250513_042741/model.py
Generated simulation script: pydevs_speed_sensor_20250513_042741/simulate.py
Generated experiment helper: pydevs_speed_sensor_20250513_042741/experiment.py
  Completed at: 04:27:41
  Duration: 0.00 seconds
Collecting code statistics for pydevs_speed_sensor_20250513_042741...
Generating visualization metrics script for pydevs_speed_sensor_20250513_042741...
Warning: index.html not found at pydevs_speed_sensor_20250513_042741/index.html
Report generated at metrics_results/metrics_report.md

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   3.83            66.3         153.4       
generate_json                  3.83            N/A          N/A         

Code Generation Statistics:
Model: pydevs_speed_sensor_20250513_042741
  Files: 4
  Lines: 170
  AtomicDEVS: 3
  CoupledDEVS: 3

Detailed metrics saved to: metrics_results/metrics_20250513_042737.json
=====================================


Complete! PyDEVS model generated successfully in: pydevs_speed_sensor_20250513_042741
Generated files are located in: pydevs_speed_sensor_20250513_042741
Running generated script: pydevs_speed_sensor_20250513_042741
  Started at: 04:27:41
  Completed at: 04:28:19
  Duration: 38.46 seconds
Output:
Running simulation...

Simulation output:
Model Loading...
Initialized SpeedSensor as c1
Model initialization complete
Simulation complete. Results saved to simulation.log


Simulation Log Preview (first 1000 chars):

__  Current Time:       0.00 __________________________________________ 


	INITIAL CONDITIONS in model <GeneratedModel.c1>
		Initial State: <speedsensor.SpeedSensorState object at 0x104e98ed0>
		Next scheduled internal transition at time 0.00


__  Current Time:       0.00 __________________________________________ 


	INTERNAL TRANSITION in model <GeneratedModel.c1>
		New State: <speedsensor.SpeedSensorState object at 0x104e98ed0>
		Output Port Configuration:
		Next scheduled internal transition at time 0.00


__  Current Time:       0.00 __________________________________________ 


	INTERNAL TRANSITION in model <GeneratedModel.c1>
		New State: <speedsensor.SpeedSensorState object at 0x104e98ed0>
		Output Port Configuration:
		Next scheduled internal transition at time 0.00


__  Current Time:       0.00 __________________________________________ 


	INTERNAL TRANSITION in model <GeneratedModel.c1>
		New State: <speedsensor.SpeedSensorState object at 0x104e98ed0>
		Output Port Conf

...

To view full log, open 'simulation.log'

Measuring simulation runtime for pydevs_speed_sensor_20250513_042741...
Using simulation script: pydevs_speed_sensor_20250513_042741/simulate.py
  Run 1/1...
  Run 1 completed successfully: 38.05s, 0.61MB
  Average runtime: 38.05 seconds
  Average memory: 0.61 MB

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   3.83            66.3         153.4       
generate_json                  3.83            N/A          N/A         

Code Generation Statistics:
Model: pydevs_speed_sensor_20250513_042741
  Files: 4
  Lines: 170
  AtomicDEVS: 3
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_speed_sensor_20250513_042741
  Avg. Runtime: 38.05 seconds
  Avg. Memory: 0.61 MB

Detailed metrics saved to: metrics_results/metrics_20250513_042737.json
=====================================

Running parser on: pydevs_speed_sensor_20250513_042741
Parser output:
0 entries written to pydevs_speed_sensor_20250513_042741/parsed_output.csv

Successfully created: pydevs_speed_sensor_20250513_042741/parsed_output.csv
Generating web pages for: pydevs_speed_sensor_20250513_042741
Running web generator on: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/model.json
Executing command: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/venv/bin/python /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/web/web_generator.py /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/model.json --output-dir /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741
Web generator output:
Generated CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/style.css
Generated JavaScript file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/script.js
Generated HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/index.html

Template generation complete. To use these templates:
1. Place your model.json and parsed_output.csv in /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741
2. Open /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/index.html in a web browser

Checking generated files:
- HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/template.html exists: False
- CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/template-styles.css exists: False
- JS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_speed_sensor_20250513_042741/template-script.js exists: False
Found alternate HTML files: ['index.html']

Final Metrics Summary:

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   3.83            66.3         153.4       
generate_json                  3.83            N/A          N/A         

Code Generation Statistics:
Model: pydevs_speed_sensor_20250513_042741
  Files: 4
  Lines: 170
  AtomicDEVS: 3
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_speed_sensor_20250513_042741
  Avg. Runtime: 38.05 seconds
  Avg. Memory: 0.61 MB

Detailed metrics saved to: metrics_results/metrics_20250513_042737.json
=====================================

Total process completed in 89.75 seconds
================================================================================

{
  "simulation_metrics": [
    {
      "model_dir": "pydevs_speed_sensor_20250513_042741",
      "model_name": "pydevs_speed_sensor_20250513_042741",
      "iterations": 1,
      "avg_runtime_seconds": 38.048896074295044,
      "avg_memory_usage_mb": 0.609375,
      "details": [
        {
          "iteration": 1,
          "runtime_seconds": 38.048896074295044,
          "memory_usage_mb": 0.609375,
          "success": true
        }
      ],
      "timestamp": "2025-05-13 04:28:58"
    }
  ],
  "code_generation_stats": [
    {
      "model_dir": "pydevs_speed_sensor_20250513_042741",
      "model_name": "pydevs_speed_sensor_20250513_042741",
      "atomic_devs_count": 3,
      "coupled_devs_count": 3,
      "total_files": 4,
      "total_lines": 170,
      "files_breakdown": [
        {
          "filename": "experiment.py",
          "lines": 40,
          "atomic_devs": 0,
          "coupled_devs": 0
        },
        {
          "filename": "model.py",
          "lines": 15,
          "atomic_devs": 0,
          "coupled_devs": 3
        },
        {
          "filename": "experiment.py",
          "lines": 39,
          "atomic_devs": 0,
          "coupled_devs": 0
        },
        {
          "filename": "speedsensor.py",
          "lines": 76,
          "atomic_devs": 3,
          "coupled_devs": 0
        }
      ],
      "timestamp": "2025-05-13 04:27:41"
    }
  ],
  "llm_processing_time": [
    {
      "task_name": "llm_api_call",
      "start_time": "2025-05-13 04:27:37",
      "end_time": "2025-05-13 04:27:41",
      "elapsed_seconds": 3.8278770446777344,
      "timestamp": "2025-05-13 04:27:41",
      "tokens_in": 66.3,
      "tokens_out": 153.4
    },
    {
      "task_name": "generate_json",
      "start_time": "2025-05-13 04:27:37",
      "end_time": "2025-05-13 04:27:41",
      "elapsed_seconds": 3.830475091934204,
      "timestamp": "2025-05-13 04:27:41"
    }
  ]
}

# Metrics Report

Generated on: 2025-05-13 04:27:41

## Simulation Runtime Metrics


| Model | Avg Runtime (s) | Avg Memory (MB) | Iterations |
|-------|----------------|-----------------|------------|
| pydevs_speed_sensor_20250513_042741 | 0.38 | 0.29 | 20 |

## Code Generation Statistics

| Model | Total Files | Total Lines | AtomicDEVS | CoupledDEVS |
|-------|-------------|-------------|------------|------------|
| pydevs_speed_sensor_20250513_042741 | 4 | 170 | 3 | 3 |

## LLM Processing Time

| Task | Elapsed Time (s) | Tokens In | Tokens Out |
|------|-----------------|-----------|------------|
| llm_api_call | 3.83 | 66.3 | 153.4 |
| generate_json | 3.83 | N/A | N/A |


*Raw data available in the metrics JSON file.*


## 2 simple IoT Window Actuator Scenario with 10s
================================================================================
CAPSSAML to PyDEVS Generator (with Metrics Collection)
================================================================================
Metrics collection: ENABLED
Starting process at: 2025-05-13 04:45:56
Creating a copy of temperature.capssaml with .txt extension
Generating JSON from CAPSSAML file...
Input size: approximately 302 tokens
Sending request to Gemini API...
  Started at: 04:45:56
  Completed at: 04:46:06
  Duration: 10.13 seconds
  Output size: approximately 560 tokens
Raw LLM response saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmpy618xlme.json.raw
Generated JSON saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmpy618xlme.json
Generating PyDEVS model from JSON...
  Started at: 04:46:06
Model JSON saved to: pydevs_temperature_20250513_044606/model.json
Generated component: TemperatureSensor -> pydevs_temperature_20250513_044606/temperaturesensor.py
Generated component: Server -> pydevs_temperature_20250513_044606/server.py
Generated component: Controller -> pydevs_temperature_20250513_044606/controller.py
Generated component: WindowActuator -> pydevs_temperature_20250513_044606/windowactuator.py
Generated coupled model: pydevs_temperature_20250513_044606/model.py
Generated simulation script: pydevs_temperature_20250513_044606/simulate.py
Generated experiment helper: pydevs_temperature_20250513_044606/experiment.py
  Completed at: 04:46:06
  Duration: 0.00 seconds
Collecting code statistics for pydevs_temperature_20250513_044606...
Generating visualization metrics script for pydevs_temperature_20250513_044606...
Warning: index.html not found at pydevs_temperature_20250513_044606/index.html
Report generated at metrics_results/metrics_report.md

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   10.13           302.90000000000003 560.3000000000001
generate_json                  10.13           N/A          N/A         

Code Generation Statistics:
Model: pydevs_temperature_20250513_044606
  Files: 7
  Lines: 384
  AtomicDEVS: 12
  CoupledDEVS: 3

Detailed metrics saved to: metrics_results/metrics_20250513_044556.json
=====================================


Complete! PyDEVS model generated successfully in: pydevs_temperature_20250513_044606
Generated files are located in: pydevs_temperature_20250513_044606
Running generated script: pydevs_temperature_20250513_044606
  Started at: 04:46:06
  Completed at: 04:46:06
  Duration: 0.15 seconds
Output:
Running simulation...

Simulation output:
Model Loading...
Initialized TemperatureSensor as c1
Initialized Server as c2
Initialized Controller as c3
Initialized WindowActuator as c4
Connected c1.out_0 to c2.in_0
Connected c1.out_1 to c3.in_0
Connected c3.out_1 to c4.in_1
Connected c3.out_0 to c4.in_0
Model initialization complete
Simulation complete. Results saved to simulation.log


Simulation Log Preview (first 1000 chars):

__  Current Time:       0.00 __________________________________________ 


	INITIAL CONDITIONS in model <GeneratedModel.c1>
		Initial State: <temperaturesensor.TemperatureSensorState object at 0x10280cdd0>
		Next scheduled internal transition at time 10.00


	INITIAL CONDITIONS in model <GeneratedModel.c2>
		Initial State: <server.ServerState object at 0x1028422d0>
		Next scheduled internal transition at time inf


	INITIAL CONDITIONS in model <GeneratedModel.c3>
		Initial State: <controller.ControllerState object at 0x1027108d0>
		Next scheduled internal transition at time inf


	INITIAL CONDITIONS in model <GeneratedModel.c4>
		Initial State: <windowactuator.WindowActuatorState object at 0x102ae5150>
		Next scheduled internal transition at time inf


__  Current Time:      10.00 __________________________________________ 


	EXTERNAL TRANSITION in model <GeneratedModel.c2>
		Input Port Configuration:
			port <in_0>:
				{'m2m:cin': {'lbl': ['c1'], 'con': 'c1, 1747091766, 48.24813260

...

To view full log, open 'simulation.log'

Measuring simulation runtime for pydevs_temperature_20250513_044606...
Using simulation script: pydevs_temperature_20250513_044606/experiment.py
  Run 1/1...
  Run 1 completed successfully: 0.10s, 0.02MB
  Average runtime: 0.10 seconds
  Average memory: 0.02 MB

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   10.13           302.90000000000003 560.3000000000001
generate_json                  10.13           N/A          N/A         

Code Generation Statistics:
Model: pydevs_temperature_20250513_044606
  Files: 7
  Lines: 384
  AtomicDEVS: 12
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_temperature_20250513_044606
  Avg. Runtime: 0.10 seconds
  Avg. Memory: 0.02 MB

Detailed metrics saved to: metrics_results/metrics_20250513_044556.json
=====================================

Running parser on: pydevs_temperature_20250513_044606
Parser output:
398 entries written to pydevs_temperature_20250513_044606/parsed_output.csv

Successfully created: pydevs_temperature_20250513_044606/parsed_output.csv
Generating web pages for: pydevs_temperature_20250513_044606
Running web generator on: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/model.json
Executing command: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/venv/bin/python /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/web/web_generator.py /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/model.json --output-dir /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606
Web generator output:
Generated CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/style.css
Generated JavaScript file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/script.js
Generated HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/index.html

Template generation complete. To use these templates:
1. Place your model.json and parsed_output.csv in /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606
2. Open /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/index.html in a web browser

Checking generated files:
- HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/template.html exists: False
- CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/template-styles.css exists: False
- JS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_temperature_20250513_044606/template-script.js exists: False
Found alternate HTML files: ['index.html']

Final Metrics Summary:

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   10.13           302.90000000000003 560.3000000000001
generate_json                  10.13           N/A          N/A         

Code Generation Statistics:
Model: pydevs_temperature_20250513_044606
  Files: 7
  Lines: 384
  AtomicDEVS: 12
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_temperature_20250513_044606
  Avg. Runtime: 0.10 seconds
  Avg. Memory: 0.02 MB

Detailed metrics saved to: metrics_results/metrics_20250513_044556.json
=====================================

Total process completed in 11.49 seconds
================================================================================

{
  "simulation_metrics": [
    {
      "model_dir": "pydevs_temperature_20250513_044606",
      "model_name": "pydevs_temperature_20250513_044606",
      "iterations": 1,
      "avg_runtime_seconds": 0.09715008735656738,
      "avg_memory_usage_mb": 0.015625,
      "details": [
        {
          "iteration": 1,
          "runtime_seconds": 0.09715008735656738,
          "memory_usage_mb": 0.015625,
          "success": true
        }
      ],
      "timestamp": "2025-05-13 04:46:07"
    }
  ],
  "code_generation_stats": [
    {
      "model_dir": "pydevs_temperature_20250513_044606",
      "model_name": "pydevs_temperature_20250513_044606",
      "atomic_devs_count": 12,
      "coupled_devs_count": 3,
      "total_files": 7,
      "total_lines": 384,
      "files_breakdown": [
        {
          "filename": "server.py",
          "lines": 54,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "controller.py",
          "lines": 75,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "windowactuator.py",
          "lines": 65,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "simulate.py",
          "lines": 40,
          "atomic_devs": 0,
          "coupled_devs": 0
        },
        {
          "filename": "temperaturesensor.py",
          "lines": 79,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "model.py",
          "lines": 32,
          "atomic_devs": 0,
          "coupled_devs": 3
        },
        {
          "filename": "experiment.py",
          "lines": 39,
          "atomic_devs": 0,
          "coupled_devs": 0
        }
      ],
      "timestamp": "2025-05-13 04:46:06"
    }
  ],
  "llm_processing_time": [
    {
      "task_name": "llm_api_call",
      "start_time": "2025-05-13 04:45:56",
      "end_time": "2025-05-13 04:46:06",
      "elapsed_seconds": 10.127387285232544,
      "timestamp": "2025-05-13 04:46:06",
      "tokens_in": 302.90000000000003,
      "tokens_out": 560.3000000000001
    },
    {
      "task_name": "generate_json",
      "start_time": "2025-05-13 04:45:56",
      "end_time": "2025-05-13 04:46:06",
      "elapsed_seconds": 10.132838010787964,
      "timestamp": "2025-05-13 04:46:06"
    }
  ]
}

# Metrics Report

Generated on: 2025-05-13 04:46:06

| Model | Avg Runtime (s) | Avg Memory (MB) | Iterations |
|-------|----------------|-----------------|------------|
| pydevs_temperature_20250513_044606 | 0.10 | 0.03 | 20 |

## Code Generation Statistics

| Model | Total Files | Total Lines | AtomicDEVS | CoupledDEVS |
|-------|-------------|-------------|------------|------------|
| pydevs_temperature_20250513_044606 | 7 | 384 | 12 | 3 |

## LLM Processing Time

| Task | Elapsed Time (s) | Tokens In | Tokens Out |
|------|-----------------|-----------|------------|
| llm_api_call | 10.13 | 302.90000000000003 | 560.3000000000001 |
| generate_json | 10.13 | N/A | N/A |


*Raw data available in the metrics JSON file.*

## 3 Motion Based Light Control 

================================================================================
CAPSSAML to PyDEVS Generator (with Metrics Collection)
================================================================================
Metrics collection: ENABLED
Starting process at: 2025-05-13 04:58:07
Creating a copy of MotionLight.capssaml with .txt extension
Generating JSON from CAPSSAML file...
Input size: approximately 221 tokens
Sending request to Gemini API...
  Started at: 04:58:07
  Completed at: 04:58:14
  Duration: 7.51 seconds
  Output size: approximately 435 tokens
Raw LLM response saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmpx6af5s2_.json.raw
Generated JSON saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmpx6af5s2_.json
Generating PyDEVS model from JSON...
  Started at: 04:58:14
Model JSON saved to: pydevs_MotionLight_20250513_045814/model.json
Generated component: MotionSensor -> pydevs_MotionLight_20250513_045814/motionsensor.py
Generated component: Router -> pydevs_MotionLight_20250513_045814/router.py
Generated component: Light -> pydevs_MotionLight_20250513_045814/light.py
Generated coupled model: pydevs_MotionLight_20250513_045814/model.py
Generated simulation script: pydevs_MotionLight_20250513_045814/simulate.py
Generated experiment helper: pydevs_MotionLight_20250513_045814/experiment.py
  Completed at: 04:58:14
  Duration: 0.00 seconds
Collecting code statistics for pydevs_MotionLight_20250513_045814...
Generating visualization metrics script for pydevs_MotionLight_20250513_045814...
Warning: index.html not found at pydevs_MotionLight_20250513_045814/index.html
Report generated at metrics_results/metrics_report.md

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   7.51            221.0        435.5       
generate_json                  7.51            N/A          N/A         

Code Generation Statistics:
Model: pydevs_MotionLight_20250513_045814
  Files: 6
  Lines: 337
  AtomicDEVS: 9
  CoupledDEVS: 3

Detailed metrics saved to: metrics_results/metrics_20250513_045807.json
=====================================


Complete! PyDEVS model generated successfully in: pydevs_MotionLight_20250513_045814
Generated files are located in: pydevs_MotionLight_20250513_045814
Running generated script: pydevs_MotionLight_20250513_045814
  Started at: 04:58:14
  Completed at: 04:58:15
  Duration: 0.21 seconds
Output:
Running simulation...

Simulation output:
Model Loading...
Initialized MotionSensor as c1
Initialized Router as c2
Initialized Light as c3
Connected c1.out_0 to c2.in_0
Connected c2.out_0 to c3.in_1
Connected c2.out_1 to c3.in_0
Model initialization complete
Simulation complete. Results saved to simulation.log


Simulation Log Preview (first 1000 chars):

__  Current Time:       0.00 __________________________________________ 


	INITIAL CONDITIONS in model <GeneratedModel.c1>
		Initial State: <motionsensor.MotionSensorState object at 0x1032abb90>
		Next scheduled internal transition at time 1.00


	INITIAL CONDITIONS in model <GeneratedModel.c2>
		Initial State: <router.RouterState object at 0x1030d7c90>
		Next scheduled internal transition at time inf


	INITIAL CONDITIONS in model <GeneratedModel.c3>
		Initial State: <light.LightState object at 0x103323810>
		Next scheduled internal transition at time inf

[c2] Value 34.035934771460816 is in normal range: No action

__  Current Time:       1.00 __________________________________________ 


	EXTERNAL TRANSITION in model <GeneratedModel.c2>
		Input Port Configuration:
			port <in_0>:
				{'m2m:cin': {'lbl': ['c1'], 'con': 'c1, 1747092495, 34.035934771460816'}}
		New State: <router.RouterState object at 0x1030d7c90>
		Next scheduled internal transition at time inf


	INTERNAL TRANSITIO

...

To view full log, open 'simulation.log'

Measuring simulation runtime for pydevs_MotionLight_20250513_045814...
Using simulation script: pydevs_MotionLight_20250513_045814/experiment.py
  Run 1/1...
  Run 1 completed successfully: 0.17s, 0.06MB
  Average runtime: 0.17 seconds
  Average memory: 0.06 MB

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   7.51            221.0        435.5       
generate_json                  7.51            N/A          N/A         

Code Generation Statistics:
Model: pydevs_MotionLight_20250513_045814
  Files: 6
  Lines: 337
  AtomicDEVS: 9
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_MotionLight_20250513_045814
  Avg. Runtime: 0.17 seconds
  Avg. Memory: 0.06 MB

Detailed metrics saved to: metrics_results/metrics_20250513_045807.json
=====================================

Running parser on: pydevs_MotionLight_20250513_045814
Parser output:
1999 entries written to pydevs_MotionLight_20250513_045814/parsed_output.csv

Successfully created: pydevs_MotionLight_20250513_045814/parsed_output.csv
Generating web pages for: pydevs_MotionLight_20250513_045814
Running web generator on: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/model.json
Executing command: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/venv/bin/python /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/web/web_generator.py /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/model.json --output-dir /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814
Web generator output:
Generated CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/style.css
Generated JavaScript file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/script.js
Generated HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/index.html

Template generation complete. To use these templates:
1. Place your model.json and parsed_output.csv in /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814
2. Open /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/index.html in a web browser

Checking generated files:
- HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/template.html exists: False
- CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/template-styles.css exists: False
- JS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_MotionLight_20250513_045814/template-script.js exists: False
Found alternate HTML files: ['index.html']

Final Metrics Summary:

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   7.51            221.0        435.5       
generate_json                  7.51            N/A          N/A         

Code Generation Statistics:
Model: pydevs_MotionLight_20250513_045814
  Files: 6
  Lines: 337
  AtomicDEVS: 9
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_MotionLight_20250513_045814
  Avg. Runtime: 0.17 seconds
  Avg. Memory: 0.06 MB

Detailed metrics saved to: metrics_results/metrics_20250513_045807.json
=====================================

Total process completed in 9.42 seconds
================================================================================
{
  "simulation_metrics": [
    {
      "model_dir": "pydevs_MotionLight_20250513_045814",
      "model_name": "pydevs_MotionLight_20250513_045814",
      "iterations": 1,
      "avg_runtime_seconds": 0.16787505149841309,
      "avg_memory_usage_mb": 0.0625,
      "details": [
        {
          "iteration": 1,
          "runtime_seconds": 0.16787505149841309,
          "memory_usage_mb": 0.0625,
          "success": true
        }
      ],
      "timestamp": "2025-05-13 04:58:16"
    }
  ],
  "code_generation_stats": [
    {
      "model_dir": "pydevs_MotionLight_20250513_045814",
      "model_name": "pydevs_MotionLight_20250513_045814",
      "atomic_devs_count": 9,
      "coupled_devs_count": 3,
      "total_files": 6,
      "total_lines": 337,
      "files_breakdown": [
        {
          "filename": "light.py",
          "lines": 65,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "simulate.py",
          "lines": 40,
          "atomic_devs": 0,
          "coupled_devs": 0
        },
        {
          "filename": "model.py",
          "lines": 27,
          "atomic_devs": 0,
          "coupled_devs": 3
        },
        {
          "filename": "experiment.py",
          "lines": 39,
          "atomic_devs": 0,
          "coupled_devs": 0
        },
        {
          "filename": "motionsensor.py",
          "lines": 76,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "router.py",
          "lines": 90,
          "atomic_devs": 3,
          "coupled_devs": 0
        }
      ],
      "timestamp": "2025-05-13 04:58:14"
    }
  ],
  "llm_processing_time": [
    {
      "task_name": "llm_api_call",
      "start_time": "2025-05-13 04:58:07",
      "end_time": "2025-05-13 04:58:14",
      "elapsed_seconds": 7.506994962692261,
      "timestamp": "2025-05-13 04:58:14",
      "tokens_in": 221.0,
      "tokens_out": 435.5
    },
    {
      "task_name": "generate_json",
      "start_time": "2025-05-13 04:58:07",
      "end_time": "2025-05-13 04:58:14",
      "elapsed_seconds": 7.511683702468872,
      "timestamp": "2025-05-13 04:58:14"
    }
  ]
}


# Metrics Report

Generated on: 2025-05-13 05:00:51

## Simulation Runtime Metrics

| Model | Avg Runtime (s) | Avg Memory (MB) | Iterations |
|-------|----------------|-----------------|------------|
| pydevs_MotionLight_20250513_045814 | 0.18 | 0.03 | 20 |

## Code Generation Statistics

| Model | Total Files | Total Lines | AtomicDEVS | CoupledDEVS |
|-------|-------------|-------------|------------|------------|
| pydevs_MotionLight_20250513_045814 | 6 | 337 | 9 | 3 |

## LLM Processing Time

| Task | Elapsed Time (s) | Tokens In | Tokens Out |
|------|-----------------|-----------|------------|
| llm_api_call | 7.66 | 221.0 | 440.7 |
| generate_json | 7.67 | N/A | N/A |

*Raw data available in the metrics JSON file.*


## Large Example with multiple conditions 

================================================================================
CAPSSAML to PyDEVS Generator (with Metrics Collection)
================================================================================
Metrics collection: ENABLED
Starting process at: 2025-05-13 05:02:43
Creating a copy of SCUNA.capssaml with .txt extension
Generating JSON from CAPSSAML file...
Input size: approximately 362 tokens
Sending request to Gemini API...
  Started at: 05:02:43
  Completed at: 05:02:54
  Duration: 11.13 seconds
  Output size: approximately 705 tokens
Raw LLM response saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmp6didvbhd.json.raw
Generated JSON saved to: /var/folders/9_/xsy51vhx14z013rcw2jjgtlm0000gn/T/tmp6didvbhd.json
Generating PyDEVS model from JSON...
  Started at: 05:02:54
Model JSON saved to: pydevs_SCUNA_20250513_050254/model.json
Generated component: DoorLockSensor -> pydevs_SCUNA_20250513_050254/doorlocksensor.py
Generated component: DoorLockActuator -> pydevs_SCUNA_20250513_050254/doorlockactuator.py
Generated component: Controller -> pydevs_SCUNA_20250513_050254/controller.py
Generated coupled model: pydevs_SCUNA_20250513_050254/model.py
Generated simulation script: pydevs_SCUNA_20250513_050254/simulate.py
Generated experiment helper: pydevs_SCUNA_20250513_050254/experiment.py
  Completed at: 05:02:54
  Duration: 0.00 seconds
Collecting code statistics for pydevs_SCUNA_20250513_050254...
Generating visualization metrics script for pydevs_SCUNA_20250513_050254...
Warning: index.html not found at pydevs_SCUNA_20250513_050254/index.html
Report generated at metrics_results/metrics_report.md

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   11.14           362.7        705.9       
generate_json                  11.14           N/A          N/A         

Code Generation Statistics:
Model: pydevs_SCUNA_20250513_050254
  Files: 6
  Lines: 302
  AtomicDEVS: 9
  CoupledDEVS: 3

Detailed metrics saved to: metrics_results/metrics_20250513_050243.json
=====================================


Complete! PyDEVS model generated successfully in: pydevs_SCUNA_20250513_050254
Generated files are located in: pydevs_SCUNA_20250513_050254
Running generated script: pydevs_SCUNA_20250513_050254
  Started at: 05:02:54
  Completed at: 05:02:54
  Duration: 0.16 seconds
Output:
Running simulation...

Simulation output:
Model Loading...
Initialized DoorLockSensor as c1
Initialized DoorLockActuator as c2
Initialized Controller as c3
Connected c1.out_0 to c2.in_0
Connected c3.out_0 to c2.in_0
Connected c1.out_1 to c3.in_1
Model initialization complete
Simulation complete. Results saved to simulation.log


Simulation Log Preview (first 1000 chars):

__  Current Time:       0.00 __________________________________________ 


	INITIAL CONDITIONS in model <GeneratedModel.c1>
		Initial State: <doorlocksensor.DoorLockSensorState object at 0x100d64ed0>
		Next scheduled internal transition at time inf


	INITIAL CONDITIONS in model <GeneratedModel.c2>
		Initial State: <doorlockactuator.DoorLockActuatorState object at 0x100d9a150>
		Next scheduled internal transition at time inf


	INITIAL CONDITIONS in model <GeneratedModel.c3>
		Initial State: <controller.ControllerState object at 0x101038310>
		Next scheduled internal transition at time inf



...

To view full log, open 'simulation.log'

Measuring simulation runtime for pydevs_SCUNA_20250513_050254...
Using simulation script: pydevs_SCUNA_20250513_050254/experiment.py
  Run 1/1...
  Run 1 completed successfully: 0.08s, 0.03MB
  Average runtime: 0.08 seconds
  Average memory: 0.03 MB

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   11.14           362.7        705.9       
generate_json                  11.14           N/A          N/A         

Code Generation Statistics:
Model: pydevs_SCUNA_20250513_050254
  Files: 6
  Lines: 302
  AtomicDEVS: 9
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_SCUNA_20250513_050254
  Avg. Runtime: 0.08 seconds
  Avg. Memory: 0.03 MB

Detailed metrics saved to: metrics_results/metrics_20250513_050243.json
=====================================

Running parser on: pydevs_SCUNA_20250513_050254
Parser output:
0 entries written to pydevs_SCUNA_20250513_050254/parsed_output.csv

Successfully created: pydevs_SCUNA_20250513_050254/parsed_output.csv
Generating web pages for: pydevs_SCUNA_20250513_050254
Running web generator on: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/model.json
Executing command: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/venv/bin/python /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/web/web_generator.py /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/model.json --output-dir /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254
Web generator output:
Generated CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/style.css
Generated JavaScript file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/script.js
Generated HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/index.html

Template generation complete. To use these templates:
1. Place your model.json and parsed_output.csv in /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254
2. Open /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/index.html in a web browser

Checking generated files:
- HTML file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/template.html exists: False
- CSS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/template-styles.css exists: False
- JS file: /Users/likhithkanigolla/IIITH/MS/S1-Course/IS/CAPS-IIITH/llmbased/pydevs_SCUNA_20250513_050254/template-script.js exists: False
Found alternate HTML files: ['index.html']

Final Metrics Summary:

===== LLM METRICS SUMMARY =====

LLM Processing Time:
Task                           Duration (s)    Tokens In    Tokens Out  
----------------------------------------------------------------------
llm_api_call                   11.14           362.7        705.9       
generate_json                  11.14           N/A          N/A         

Code Generation Statistics:
Model: pydevs_SCUNA_20250513_050254
  Files: 6
  Lines: 302
  AtomicDEVS: 9
  CoupledDEVS: 3

Simulation Runtime Metrics:
Model: pydevs_SCUNA_20250513_050254
  Avg. Runtime: 0.08 seconds
  Avg. Memory: 0.03 MB

Detailed metrics saved to: metrics_results/metrics_20250513_050243.json
=====================================

Total process completed in 12.49 seconds
================================================================================

{
  "simulation_metrics": [
    {
      "model_dir": "pydevs_SCUNA_20250513_050254",
      "model_name": "pydevs_SCUNA_20250513_050254",
      "iterations": 1,
      "avg_runtime_seconds": 0.08398795127868652,
      "avg_memory_usage_mb": 0.03125,
      "details": [
        {
          "iteration": 1,
          "runtime_seconds": 0.08398795127868652,
          "memory_usage_mb": 0.03125,
          "success": true
        }
      ],
      "timestamp": "2025-05-13 05:02:55"
    }
  ],
  "code_generation_stats": [
    {
      "model_dir": "pydevs_SCUNA_20250513_050254",
      "model_name": "pydevs_SCUNA_20250513_050254",
      "atomic_devs_count": 9,
      "coupled_devs_count": 3,
      "total_files": 6,
      "total_lines": 302,
      "files_breakdown": [
        {
          "filename": "controller.py",
          "lines": 70,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "simulate.py",
          "lines": 40,
          "atomic_devs": 0,
          "coupled_devs": 0
        },
        {
          "filename": "model.py",
          "lines": 27,
          "atomic_devs": 0,
          "coupled_devs": 3
        },
        {
          "filename": "experiment.py",
          "lines": 39,
          "atomic_devs": 0,
          "coupled_devs": 0
        },
        {
          "filename": "doorlocksensor.py",
          "lines": 66,
          "atomic_devs": 3,
          "coupled_devs": 0
        },
        {
          "filename": "doorlockactuator.py",
          "lines": 60,
          "atomic_devs": 3,
          "coupled_devs": 0
        }
      ],
      "timestamp": "2025-05-13 05:02:54"
    }
  ],
  "llm_processing_time": [
    {
      "task_name": "llm_api_call",
      "start_time": "2025-05-13 05:02:43",
      "end_time": "2025-05-13 05:02:54",
      "elapsed_seconds": 11.13500690460205,
      "timestamp": "2025-05-13 05:02:54",
      "tokens_in": 362.7,
      "tokens_out": 705.9
    },
    {
      "task_name": "generate_json",
      "start_time": "2025-05-13 05:02:43",
      "end_time": "2025-05-13 05:02:54",
      "elapsed_seconds": 11.140730857849121,
      "timestamp": "2025-05-13 05:02:54"
    }
  ]
}


# Metrics Report

Generated on: 2025-05-13 05:02:54

## Simulation Runtime Metrics


| Model | Avg Runtime (s) | Avg Memory (MB) | Iterations |
|-------|----------------|-----------------|------------|
| pydevs_SCUNA_20250513_050254 | 0.09 | 0.01 | 20 |

## Code Generation Statistics

| Model | Total Files | Total Lines | AtomicDEVS | CoupledDEVS |
|-------|-------------|-------------|------------|------------|
| pydevs_SCUNA_20250513_050254 | 6 | 302 | 9 | 3 |

## LLM Processing Time

| Task | Elapsed Time (s) | Tokens In | Tokens Out |
|------|-----------------|-----------|------------|
| llm_api_call | 11.14 | 362.7 | 705.9 |
| generate_json | 11.14 | N/A | N/A |


*Raw data available in the metrics JSON file.*
