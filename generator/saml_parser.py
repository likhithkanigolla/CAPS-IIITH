import xml.etree.ElementTree as ET
import re
from .debug_utils import debug_print

def parse_saml_file(file_path):
    """
    Parse a SAML file and extract component and connection information.
    
    Args:
        file_path: Path to the SAML file
        
    Returns:
        tuple: (components, connections)
    """
    debug_print(f"Parsing SAML file: {file_path}")
    
    try:
        # Parse XML tree
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Extract namespace from root tag
        namespace_match = re.match(r'{(.*)}', root.tag)
        namespace = namespace_match.group(1) if namespace_match else None
        
        components = []
        connections = []
        component_map = {}  # To store component ID to name mapping
        
        # Function to add namespace to tag if needed
        def tag_with_ns(tag):
            return f"{{{namespace}}}{tag}" if namespace else tag
        
        # Process all SAElements to find components and connections
        for idx, element in enumerate(root.findall('.//*[@xsi:type]', 
                                     {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})):
            element_type = element.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            
            # Handle components
            if element_type == 'components:Component':
                component = parse_component(element, idx)
                components.append(component)
                component_map[idx] = component['name']
                debug_print(f"Found component: {component['name']}")
            
            # Handle connections
            elif element_type == 'components:Connection':
                connection = {
                    'source_component': '',
                    'source_port': 0,
                    'source_port_type': 'output',
                    'target_component': '',
                    'target_port': 0,
                    'target_port_type': 'input'
                }
                connections.append(connection)
        
        # Process connections after all components are known
        connection_idx = 0
        for element in root.findall('.//*[@xsi:type="components:Connection"]', 
                                   {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}):
            if connection_idx < len(connections):
                source_ref = element.get('source')
                target_ref = element.get('target')
                
                # Extract component and port information from refs
                if source_ref and target_ref:
                    source_comp_idx, source_port_idx = extract_ref_info(source_ref)
                    target_comp_idx, target_port_idx = extract_ref_info(target_ref)
                    
                    # Set connection information
                    if source_comp_idx in component_map and target_comp_idx in component_map:
                        connections[connection_idx]['source_component'] = component_map[source_comp_idx]
                        connections[connection_idx]['source_port'] = source_port_idx
                        connections[connection_idx]['target_component'] = component_map[target_comp_idx]
                        connections[connection_idx]['target_port'] = target_port_idx
                        
                        debug_print(f"Found connection: {connections[connection_idx]['source_component']} -> {connections[connection_idx]['target_component']}")
                
                connection_idx += 1
        
        # Fix connections with missing information
        connections = [conn for conn in connections if conn['source_component'] and conn['target_component']]
        
        # Assign component types based on behavior and naming conventions
        for component in components:
            infer_component_type(component)
            
        return components, connections
            
    except Exception as e:
        debug_print(f"Error parsing SAML file: {str(e)}")
        return [], []

def parse_component(element, idx):
    """Parse a component element and extract information."""
    component = {
        'name': element.get('name', f"Component_{idx}"),
        'type': 'generic',  # Will be inferred later
        'in_ports': [],
        'out_ports': [],
        'data_interval': 5.0  # Default data interval for sensors
    }
    
    # Process ports
    port_idx = 0
    for port in element.findall('.//ports'):
        port_type = port.get('{http://www.w3.org/2001/XMLSchema-instance}type', '')
        
        if 'InMessagePort' in port_type:
            component['in_ports'].append(port_idx)
        elif 'OutMessagePort' in port_type:
            component['out_ports'].append(port_idx)
        
        port_idx += 1
    
    # Look for behaviors that might indicate component type
    has_sense = any('Sense' in e.get('{http://www.w3.org/2001/XMLSchema-instance}type', '') 
                  for e in element.findall('.//behaviouralElements'))
    has_actuate = any('Actuate' in e.get('{http://www.w3.org/2001/XMLSchema-instance}type', '') 
                     for e in element.findall('.//behaviouralElements'))
    has_server = any('Server' in e.get('{http://www.w3.org/2001/XMLSchema-instance}type', '') 
                    for e in element.findall('.//behaviouralElements'))
    has_choice = any('Choice' in e.get('{http://www.w3.org/2001/XMLSchema-instance}type', '') 
                    for e in element.findall('.//behaviouralElements'))
    
    # Look for timers which might indicate a sensor
    has_timer = any('Timer' in e.get('name', '') for e in element.findall('.//behaviouralElements'))
    
    # Initial type determination based on behavior
    if has_sense or has_timer:
        component['type'] = 'sensor'
        
        # Try to determine sensor data interval from timer period
        for timer in element.findall('.//behaviouralElements[@xsi:type="components:StartTimer"]', 
                                    {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}):
            period = timer.get('period')
            if period and period.isdigit():
                # Convert ms to seconds
                component['data_interval'] = int(period) / 1000.0
    elif has_actuate:
        component['type'] = 'actuator'
    elif has_choice:
        component['type'] = 'controller'
    elif has_server:
        component['type'] = 'interface'
    
    return component

def extract_ref_info(ref):
    """Extract component index and port index from a reference string."""
    # Example ref: "//@SAElements.0/@ports.1"
    comp_match = re.search(r'@SAElements\.(\d+)', ref)
    port_match = re.search(r'@ports\.(\d+)', ref)
    
    comp_idx = int(comp_match.group(1)) if comp_match else -1
    port_idx = int(port_match.group(1)) if port_match else 0
    
    return comp_idx, port_idx

def infer_component_type(component):
    """Use naming conventions and port configuration to infer component type."""
    name = component['name'].lower()
    
    # Override based on naming conventions which are more reliable
    if 'sensor' in name or 'temperature' in name or 'humid' in name:
        component['type'] = 'sensor'
    elif 'actuator' in name or 'window' in name or 'fan' in name or 'valve' in name:
        component['type'] = 'actuator'
    elif 'controller' in name or 'control' in name:
        component['type'] = 'controller'
    elif 'server' in name or 'gateway' in name or 'interface' in name:
        component['type'] = 'interface'
    
    # Infer based on port configuration as fallback
    if component['type'] == 'generic':
        if len(component['out_ports']) > 0 and len(component['in_ports']) == 0:
            component['type'] = 'sensor'
        elif len(component['in_ports']) > 0 and len(component['out_ports']) == 0:
            component['type'] = 'actuator'
        elif len(component['in_ports']) > 0 and len(component['out_ports']) > 0:
            component['type'] = 'controller'
    
    return component['type']
