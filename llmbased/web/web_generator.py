#!/usr/bin/env python3
"""
Template Generator for System Simulation Visualization

Processes model.json files and creates custom HTML, CSS, and JavaScript 
visualization templates tailored to the specific model.
"""

import os
import sys
import json
import argparse
import colorsys
import random
from pathlib import Path

def load_model(model_path):
    """Load a model.json file"""
    try:
        with open(model_path, 'r') as f:
            content = f.read()
            # Handle comment lines
            if content.strip().startswith('//'):
                content = '\n'.join(content.split('\n')[1:])
            
            model_data = json.loads(content)
            return model_data
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def generate_component_colors(components):
    """Generate a color mapping for all components"""
    colors = {}
    
    # Base colors (attractive, distinctive colors)
    base_colors = [
        '#2980b9', '#8e44ad', '#27ae60', '#e67e22', '#3498db', 
        '#9b59b6', '#2ecc71', '#f39c12', '#1abc9c', '#d35400', 
        '#c0392b', '#16a085', '#7f8c8d', '#34495e'
    ]
    
    # For large models, generate additional colors procedurally
    if len(components) > len(base_colors):
        # Add procedurally generated colors for additional components
        for i in range(len(base_colors), len(components)):
            # Generate evenly distributed hues
            h = (i * 0.618033988749895) % 1  # Golden ratio conjugate produces well-distributed colors
            s = 0.7 + random.random() * 0.3  # High saturation
            v = 0.7 + random.random() * 0.3  # Good brightness
            
            # Convert HSV to RGB, then to hex
            r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)]
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            base_colors.append(hex_color)
    
    # Assign colors to components
    for i, component in enumerate(components):
        colors[component['id']] = base_colors[i % len(base_colors)]
    
    return colors

def generate_css(model_data, output_path):
    """Generate custom CSS based on the model"""
    components = model_data.get('components', [])
    component_colors = generate_component_colors(components)
    
    css_content = """/* Auto-generated component styles */
body {
    font-family: sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

.container {
    display: flex;
    width: 95%;
    max-width: 1600px;
    margin: 20px auto;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

.main-content {
    flex: 3;
    padding: 20px;
    border-right: 1px solid #ccc;
}

.sidebar {
    flex: 1;
    padding: 20px;
    background-color: #e9e9e9;
}

.diagram-container {
    position: relative;
    min-height: 500px;
    border: 1px solid #ddd;
    background-color: #ffffff;
}

/* Component base styles */
.component rect {
    stroke: #333;
    stroke-width: 1.5;
    rx: 5;
    ry: 5;
    filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
}

.component text {
    font-size: 12px;
    font-weight: bold;
    text-anchor: middle;
    dominant-baseline: middle;
    fill: #fff;
}

.component .type-label {
    font-size: 10px;
    font-style: italic;
    fill: #eee;
}

.component .data-value {
    font-size: 12px;
    font-weight: bold;
    text-anchor: middle;
    fill: #ffff00;
    opacity: 0;
}

.component.with-data .data-value {
    opacity: 1;
}

/* Connection line styles */
.connection {
    stroke-width: 2;
    fill: none;
    opacity: 0.7;
}

.connection.active {
    stroke-width: 3;
    stroke-opacity: 1 !important;
    animation: flow-pulse 0.5s ease-in-out;
}

/* Animation styles */
@keyframes flow-pulse {
    0% { stroke-dasharray: none; stroke-opacity: 0.7; }
    50% { stroke-dasharray: 10 5; stroke-opacity: 1; }
    100% { stroke-dasharray: none; stroke-opacity: 0.9; }
}

@keyframes data-pulse {
    0% { font-size: 10px; opacity: 0.7; }
    50% { font-size: 14px; opacity: 1; }
    100% { font-size: 12px; opacity: 0.9; }
}

.component .data-value.animate {
    animation: data-pulse 0.5s ease-in-out;
}

.component.active rect {
    stroke: #ffdd57;
    stroke-width: 3;
    transform: scale(1.05);
}

/* Legend styles */
.legend {
    list-style: none;
    padding: 0;
    margin-top: 20px;
}

.legend li {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
}

.legend-color {
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 10px;
    border: 1px solid #555;
    border-radius: 3px;
}

/* Controls and log */
.control-buttons {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

#start-sim-btn, #stop-sim-btn, #restart-sim-btn {
    padding: 10px 15px;
    font-size: 16px;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

#start-sim-btn {
    background-color: #3498db;
}

#stop-sim-btn {
    background-color: #e74c3c;
}

#restart-sim-btn {
    background-color: #2ecc71;
}

#start-sim-btn:hover {
    background-color: #2980b9;
}

#stop-sim-btn:hover {
    background-color: #c0392b;
}

#restart-sim-btn:hover {
    background-color: #27ae60;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.log-container {
    background-color: #333;
    color: #0f0;
    padding: 10px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    overflow-y: auto;
    border-radius: 4px;
    height: 200px;
}

/* Custom component colors */
"""
    
    # Add component-specific styles
    for comp_id, color in component_colors.items():
        css_content += f"""
.component-{comp_id} rect {{ 
    fill: {color}; 
}}

.legend-item-{comp_id} {{
    background-color: {color};
}}
"""
    
    with open(output_path, 'w') as f:
        f.write(css_content)
    
    print(f"Generated CSS file: {output_path}")
    return component_colors

def generate_js(model_data, component_colors, output_path):
    """Generate custom JavaScript based on the model"""
    
    # Create a JS object with component colors
    color_mapping_js = "{\n"
    for comp_id, color in component_colors.items():
        color_mapping_js += f"        '{comp_id}': '{color}',\n"
    color_mapping_js += "    }"
    
    js_content = f"""// Auto-generated visualization script
document.addEventListener('DOMContentLoaded', () => {{
    const svg = document.getElementById('system-diagram');
    const startBtn = document.getElementById('start-sim-btn');
    const stopBtn = document.getElementById('stop-sim-btn');
    const restartBtn = document.getElementById('restart-sim-btn');
    const timeDisplay = document.getElementById('sim-time');
    const logContainer = document.getElementById('sim-log');
    const svgNS = "http://www.w3.org/2000/svg";

    let modelData = null;
    let simulationData = [];
    let componentElements = {{}};
    let connectionElements = {{}};
    let componentPositions = {{}};
    let currentEventTime = 0;
    let isSimulationRunning = false;

    const COMPONENT_WIDTH = 150;
    const COMPONENT_HEIGHT = 70;
    const H_SPACING = 100;
    const V_SPACING = 50;
    const SIMULATION_SPEED_FACTOR = 5;
    const ANIMATION_DURATION = 500;

    // Pre-defined component colors from the generated template
    const componentColors = {color_mapping_js};

    // Load data
    async function loadData() {{
        try {{
            logEvent("Loading simulation data...");
            
            // Load model.json
            const modelResponse = await fetch('model.json');
            if (!modelResponse.ok) throw new Error(`Failed to load model.json: ${{modelResponse.status}}`);
            modelData = await modelResponse.json();
            logEvent("Model data loaded successfully");
            
            // Load CSV data
            const csvResponse = await fetch('parsed_output.csv');
            if (!csvResponse.ok) throw new Error(`Failed to load CSV: ${{csvResponse.status}}`);
            const csvText = await csvResponse.text();
            
            // Parse CSV
            const csvData = parseCSV(csvText);
            processSimulationData(csvData);
        }} catch (error) {{
            console.error("Error loading data:", error);
            logEvent(`Error: ${{error.message}}`);
        }}
    }}

    // Parse CSV keeping values as strings
    function parseCSV(text) {{
        const lines = text.split('\\n').filter(line => line.trim());
        let startLine = 0;
        
        if (lines[0].includes('// filepath:')) {{
            startLine = 1;
        }}
        
        const headers = lines[startLine].split(',').map(h => h.trim());
        const result = [];
        
        for (let i = startLine + 1; i < lines.length; i++) {{
            if (!lines[i].trim()) continue;
            
            const values = lines[i].split(',').map(v => v.trim());
            const row = {{}};
            
            headers.forEach((header, j) => {{
                if (j < values.length) {{
                    row[header] = values[j];
                }}
            }});
            
            result.push(row);
        }}
        
        return result;
    }}

    // Process simulation data
    function processSimulationData(data) {{
        simulationData = data.filter(row => 
            row && row.time && row.from && row.to && row.value !== undefined
        );
        
        logEvent(`Loaded ${{simulationData.length}} simulation events`);
        
        if (simulationData.length === 0) {{
            logEvent("Warning: No valid simulation data found");
        }} else {{
            startBtn.disabled = false;
            restartBtn.disabled = false;
            renderSystem();
        }}
    }}

    // Render the system diagram
    function renderSystem() {{
        if (!modelData || !svg) return;
        
        svg.innerHTML = '';
        createArrowheadMarker();
        positionComponents();
        
        modelData.components.forEach(component => {{
            createComponentElement(component);
        }});
        
        modelData.connections.forEach(connection => {{
            createConnectionElement(connection);
        }});
        
        setSVGViewBox();
        generateLegend();
    }}

    // Create arrowhead marker
    function createArrowheadMarker() {{
        const defs = document.createElementNS(svgNS, 'defs');
        const marker = document.createElementNS(svgNS, 'marker');
        marker.setAttribute('id', 'arrowhead');
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '7');
        marker.setAttribute('refX', '8');
        marker.setAttribute('refY', '3.5');
        marker.setAttribute('orient', 'auto');
        
        const polygon = document.createElementNS(svgNS, 'polygon');
        polygon.setAttribute('points', '0 0, 10 3.5, 0 7');
        polygon.setAttribute('fill', '#555');
        marker.appendChild(polygon);
        defs.appendChild(marker);
        svg.appendChild(defs);
    }}

    // Generate legend with component names
    function generateLegend() {{
        const legendContainer = document.querySelector('.legend');
        if (!legendContainer) return;
        
        legendContainer.innerHTML = '';
        
        modelData.components.forEach(comp => {{
            const item = document.createElement('li');
            
            const colorBox = document.createElement('span');
            colorBox.className = `legend-color legend-item-${{comp.id}}`;
            colorBox.style.backgroundColor = componentColors[comp.id] || '#7f8c8d';
            
            const label = document.createElement('span');
            label.textContent = comp.name || comp.id;
            
            item.appendChild(colorBox);
            item.appendChild(label);
            legendContainer.appendChild(item);
        }});
    }}

    // Position components based on flow analysis
    function positionComponents() {{
        const graph = buildConnectionGraph();
        const levels = analyzeComponentFlow(graph);
        
        Object.entries(levels).forEach(([id, level], index) => {{
            const component = modelData.components.find(c => c.id === id);
            if (!component) return;
            
            const x = 100 + level * (COMPONENT_WIDTH + H_SPACING);
            const y = 50 + index * (COMPONENT_HEIGHT + V_SPACING);
            
            componentPositions[id] = {{
                x, y,
                width: COMPONENT_WIDTH,
                height: COMPONENT_HEIGHT
            }};
        }});
        
        optimizePositions(graph);
    }}

    // Build connection graph
    function buildConnectionGraph() {{
        const graph = {{}};
        
        modelData.components.forEach(comp => {{
            graph[comp.id] = {{ incoming: [], outgoing: [] }};
        }});
        
        modelData.connections.forEach(conn => {{
            const [fromComp, fromPort] = conn.from.split('.');
            const [toComp, toPort] = conn.to.split('.');
            
            if (graph[fromComp]) graph[fromComp].outgoing.push(toComp);
            if (graph[toComp]) graph[toComp].incoming.push(fromComp);
        }});
        
        return graph;
    }}

    // Analyze component flow to determine levels
    function analyzeComponentFlow(graph) {{
        const levels = {{}};
        const visited = new Set();
        
        // Find starting components (no incoming connections)
        const startNodes = Object.keys(graph).filter(id => graph[id].incoming.length === 0);
        
        // If we found clear starting points, use breadth-first traversal
        if (startNodes.length > 0) {{
            let currentLevel = startNodes;
            let level = 0;
            
            while (currentLevel.length > 0) {{
                currentLevel.forEach(id => {{
                    levels[id] = level;
                    visited.add(id);
                }});
                
                // Find next level components
                const nextLevel = [];
                currentLevel.forEach(id => {{
                    graph[id].outgoing.forEach(target => {{
                        if (!visited.has(target) && 
                            graph[target].incoming.every(src => visited.has(src))) {{
                            nextLevel.push(target);
                        }}
                    }});
                }});
                
                currentLevel = nextLevel;
                level++;
            }}
        }}
        
        // Assign remaining components based on role or position in the list
        modelData.components.forEach((comp, index) => {{
            if (!visited.has(comp.id)) {{
                // Assign level based on component type/role if possible
                const role = comp.role ? comp.role.toLowerCase() : '';
                
                if (role === 'sensor' || role === 'input') {{
                    levels[comp.id] = 0;
                }} else if (role === 'controller' || role === 'processor') {{
                    levels[comp.id] = 1;
                }} else if (role === 'actuator' || role === 'output') {{
                    levels[comp.id] = 2;
                }} else {{
                    // Default placement
                    levels[comp.id] = index % 3; // Simple distribution for remaining components
                }}
            }}
        }});
        
        return levels;
    }}

    // Optimize component positions for better visualization
    function optimizePositions(graph) {{
        // TODO: Add position optimization logic if needed
    }}

    // Create component element
    function createComponentElement(component) {{
        const pos = componentPositions[component.id];
        if (!pos) return;
        
        const group = document.createElementNS(svgNS, 'g');
        group.setAttribute('class', `component component-${{component.id}}`);
        group.setAttribute('data-id', component.id);
        
        // Create rectangle
        const rect = document.createElementNS(svgNS, 'rect');
        rect.setAttribute('x', pos.x);
        rect.setAttribute('y', pos.y);
        rect.setAttribute('width', pos.width);
        rect.setAttribute('height', pos.height);
        group.appendChild(rect);
        
        // Create component name
        const nameText = document.createElementNS(svgNS, 'text');
        nameText.setAttribute('x', pos.x + pos.width/2);
        nameText.setAttribute('y', pos.y + pos.height/2 - 15);
        nameText.textContent = component.name || component.id;
        group.appendChild(nameText);
        
        // Create component type/ID
        const typeText = document.createElementNS(svgNS, 'text');
        typeText.setAttribute('x', pos.x + pos.width/2);
        typeText.setAttribute('y', pos.y + pos.height/2 + 5);
        typeText.setAttribute('class', 'type-label');
        typeText.textContent = component.id;
        group.appendChild(typeText);
        
        // Create data value display
        const dataText = document.createElementNS(svgNS, 'text');
        dataText.setAttribute('x', pos.x + pos.width/2);
        dataText.setAttribute('y', pos.y + pos.height/2 + 25);
        dataText.setAttribute('class', 'data-value');
        dataText.textContent = '—';
        group.appendChild(dataText);
        
        componentElements[component.id] = group;
        svg.appendChild(group);
    }}

    // Create connection element
    function createConnectionElement(connection) {{
        const [fromComp, fromPort] = connection.from.split('.');
        const [toComp, toPort] = connection.to.split('.');
        
        if (!componentPositions[fromComp] || !componentPositions[toComp]) return;
        
        const fromPos = componentPositions[fromComp];
        const toPos = componentPositions[toComp];
        
        // Calculate start and end points
        const startX = fromPos.x + fromPos.width;
        const startY = fromPos.y + fromPos.height/2;
        const endX = toPos.x;
        const endY = toPos.y + toPos.height/2;
        
        // Create path with bezier curve
        const path = document.createElementNS(svgNS, 'path');
        path.setAttribute('class', 'connection');
        
        const controlPointDistance = (endX - startX) / 2;
        const d = `M ${{startX}} ${{startY}} 
                   C ${{startX + controlPointDistance}} ${{startY}}, 
                     ${{endX - controlPointDistance}} ${{endY}}, 
                     ${{endX}} ${{endY}}`;
        
        path.setAttribute('d', d);
        path.setAttribute('marker-end', 'url(#arrowhead)');
        path.setAttribute('data-from', connection.from);
        path.setAttribute('data-to', connection.to);
        
        // Apply source component color
        const sourceColor = componentColors[fromComp];
        if (sourceColor) {{
            path.style.stroke = sourceColor;
        }}
        
        connectionElements[`${{connection.from}}-${{connection.to}}`] = path;
        svg.appendChild(path);
    }}

    // Set SVG viewBox for proper scaling
    function setSVGViewBox() {{
        let minX = Infinity, minY = Infinity;
        let maxX = 0, maxY = 0;
        
        Object.values(componentPositions).forEach(pos => {{
            minX = Math.min(minX, pos.x);
            minY = Math.min(minY, pos.y);
            maxX = Math.max(maxX, pos.x + pos.width);
            maxY = Math.max(maxY, pos.y + pos.height);
        }});
        
        const padding = 50;
        minX = Math.max(0, minX - padding);
        minY = Math.max(0, minY - padding);
        maxX += padding;
        maxY += padding;
        
        const width = maxX - minX;
        const height = maxY - minY;
        svg.setAttribute('viewBox', `${{minX}} ${{minY}} ${{width}} ${{height}}`);
    }}

    // Start simulation
    function startSimulation() {{
        if (simulationData.length === 0) {{
            logEvent("No simulation data to play");
            return;
        }}
        
        currentEventIndex = 0;
        currentEventTime = simulationData[0].time;
        isSimulationRunning = true;
        
        if (simulationTimeoutId) {{
            clearTimeout(simulationTimeoutId);
        }}
        
        startBtn.disabled = true;
        stopBtn.disabled = false;
        restartBtn.disabled = true;
        logContainer.innerHTML = '';
        logEvent("Simulation started");
        
        processCurrentTimeEvents();
    }}

    // Stop simulation
    function stopSimulation() {{
        if (simulationTimeoutId) {{
            clearTimeout(simulationTimeoutId);
            simulationTimeoutId = null;
        }}
        
        isSimulationRunning = false;
        startBtn.disabled = false;
        stopBtn.disabled = true;
        restartBtn.disabled = false;
        
        logEvent("Simulation stopped");
    }}

    // Restart simulation
    function restartSimulation() {{
        // First stop any running simulation
        if (isSimulationRunning) {{
            stopSimulation();
        }}
        
        // Reset component displays
        Object.values(componentElements).forEach(element => {{
            element.classList.remove('active', 'with-data');
            const dataText = element.querySelector('.data-value');
            if (dataText) {{
                dataText.textContent = '—';
            }}
        }});
        
        // Reset connections
        Object.values(connectionElements).forEach(element => {{
            element.classList.remove('active');
        }});
        
        // Reset time display
        timeDisplay.textContent = "0.00";
        
        // Start again
        startSimulation();
    }}

    // Process current time events
    function processCurrentTimeEvents() {{
        const currentEvents = [];
        
        while (currentEventIndex < simulationData.length && 
               simulationData[currentEventIndex].time === currentEventTime) {{
            currentEvents.push(simulationData[currentEventIndex]);
            currentEventIndex++;
        }}
        
        if (currentEvents.length > 0) {{
            currentEvents.forEach(event => {{
                logEvent(`Time ${{event.time}}: ${{event.from}} → ${{event.to}}: ${{event.value}}`);
                animateDataFlow(event.from, event.to, event.value);
            }});
        }}
        
        if (currentEventIndex < simulationData.length) {{
            const nextEventTime = simulationData[currentEventIndex].time;
            const timeDelta = parseFloat(nextEventTime) - parseFloat(currentEventTime);
            const delay = (timeDelta * 1000) / SIMULATION_SPEED_FACTOR;
            
            timeDisplay.textContent = parseFloat(nextEventTime).toFixed(2);
            
            simulationTimeoutId = setTimeout(() => {{
                currentEventTime = nextEventTime;
                processCurrentTimeEvents();
            }}, delay);
        }} else {{
            // Simulation has completed
            isSimulationRunning = false;
            startBtn.disabled = false;
            stopBtn.disabled = true;
            restartBtn.disabled = false;
            logEvent("Simulation completed");
        }}
    }}

    // Animate data flow between components
    function animateDataFlow(from, to, value) {{
        const connKey = `${{from}}-${{to}}`;
        const connElement = connectionElements[connKey];
        
        if (connElement) {{
            const fromCompId = from.split('.')[0];
            const toCompId = to.split('.')[0];
            const fromElement = componentElements[fromCompId];
            const toElement = componentElements[toCompId];
            
            // Highlight and update source component
            if (fromElement) {{
                fromElement.classList.add('active', 'with-data');
                const dataText = fromElement.querySelector('.data-value');
                if (dataText) {{
                    dataText.textContent = value;
                    dataText.classList.add('animate');
                    setTimeout(() => {{
                        dataText.classList.remove('animate');
                    }}, ANIMATION_DURATION);
                }}
                
                setTimeout(() => {{
                    fromElement.classList.remove('active');
                }}, ANIMATION_DURATION);
            }}
            
            // Highlight connection
            connElement.classList.add('active');
            setTimeout(() => {{
                connElement.classList.remove('active');
            }}, ANIMATION_DURATION);
            
            // Highlight target with delay
            setTimeout(() => {{
                if (toElement) {{
                    toElement.classList.add('active', 'with-data');
                    const dataText = toElement.querySelector('.data-value');
                    if (dataText) {{
                        dataText.textContent = value;
                        dataText.classList.add('animate');
                        setTimeout(() => {{
                            dataText.classList.remove('animate');
                        }}, ANIMATION_DURATION);
                    }}
                    
                    setTimeout(() => {{
                        toElement.classList.remove('active');
                    }}, ANIMATION_DURATION);
                }}
            }}, ANIMATION_DURATION / 2);
        }}
    }}

    // Log an event to the event log
    function logEvent(message) {{
        const p = document.createElement('p');
        p.textContent = message;
        logContainer.appendChild(p);
        logContainer.scrollTop = logContainer.scrollHeight;
    }}

    // Set up event listeners
    let simulationTimeoutId = null;
    let currentEventIndex = 0;
    
    startBtn.disabled = true;
    stopBtn.disabled = true;
    restartBtn.disabled = true;
    
    startBtn.addEventListener('click', startSimulation);
    stopBtn.addEventListener('click', stopSimulation);
    restartBtn.addEventListener('click', restartSimulation);
    
    // Initialize the visualization
    logEvent("Initializing simulation viewer...");
    loadData();
}});
"""
    
    with open(output_path, 'w') as f:
        f.write(js_content)
    
    print(f"Generated JavaScript file: {output_path}")

def generate_html(output_path):
    """Generate HTML template file"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Simulation Viewer</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="main-content">
            <h1>System Diagram</h1>
            <div class="diagram-container">
                <svg id="system-diagram" width="100%" height="600"></svg>
            </div>
        </div>
        <div class="sidebar">
            <h2>Simulation Control</h2>
            <div class="control-buttons">
                <button id="start-sim-btn">Start Simulation</button>
                <button id="stop-sim-btn" disabled>Stop Simulation</button>
                <button id="restart-sim-btn">Restart Simulation</button>
            </div>
            <div class="info">
                <h3>Current Time: <span id="sim-time">0.00</span></h3>
            </div>
            <h2>Event Log</h2>
            <div id="sim-log" class="log-container">
                <p>Simulation not started.</p>
            </div>
            <h2>Component Legend</h2>
            <ul class="legend">
                <!-- Legend items will be dynamically generated -->
            </ul>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
"""
    
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"Generated HTML file: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate visualization templates from model.json')
    parser.add_argument('model_path', help='Path to model.json file')
    parser.add_argument('--output-dir', '-o', default=None, help='Output directory (defaults to model file location)')
    
    args = parser.parse_args()
    model_path = args.model_path
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.dirname(model_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load model data
    model_data = load_model(model_path)
    if not model_data:
        sys.exit(1)
    
    # Generate template files
    css_path = os.path.join(output_dir, "style.css")
    js_path = os.path.join(output_dir, "script.js")
    html_path = os.path.join(output_dir, "index.html")
    
    component_colors = generate_css(model_data, css_path)
    generate_js(model_data, component_colors, js_path)
    generate_html(html_path)
    
    print("\nTemplate generation complete. To use these templates:")
    print(f"1. Place your model.json and parsed_output.csv in {output_dir}")
    print(f"2. Open {html_path} in a web browser")

if __name__ == "__main__":
    main()
