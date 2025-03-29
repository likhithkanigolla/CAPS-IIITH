import os
import xml.etree.ElementTree as ET
import traceback
from .debug_utils import debug_print, log_exception

def extract_components(saml_file_path=None, hwml_file_path=None):
    """Extract component information from both SAML and HWML files."""
    debug_print(f"Starting component extraction - SAML: {saml_file_path}, HWML: {hwml_file_path}")
    namespaces = {
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'components': 'components',
        'filesystem': 'filesystem'
    }
    
    components = []
    # Process SAML file if provided
    if saml_file_path and os.path.exists(saml_file_path):
        try:
            debug_print(f"Parsing SAML file: {saml_file_path}")
            tree = ET.parse(saml_file_path)
            root = tree.getroot()
            
            if root.find('./SAElements', namespaces) is not None:
                debug_print("Found SAElements in SAML file")
                
                # Count elements for debugging
                element_count = len(root.findall('./SAElements', namespaces))
                debug_print(f"Found {element_count} SAElements")
                
                for i, element in enumerate(root.findall('./SAElements', namespaces)):
                    element_type = element.get(f'{{{namespaces["xsi"]}}}type')
                    debug_print(f"Element {i} type: {element_type}")
                    
                    if element_type and 'Component' in element_type:
                        component_name = element.get('name')
                        debug_print(f"Found component: {component_name}")
                        
                        # Extract ports
                        in_ports = []
                        out_ports = []
                        for j, port in enumerate(element.findall('./ports', namespaces)):
                            port_type = port.get(f'{{{namespaces["xsi"]}}}type', '')
                            debug_print(f"  Port {j} type: {port_type}")
                            if "InMessagePort" in port_type:
                                in_ports.append(j)
                            elif "OutMessagePort" in port_type:
                                out_ports.append(j)
                        
                        debug_print(f"  In ports: {in_ports}, Out ports: {out_ports}")
                        
                        # Extract behavior if available
                        behaviors = []
                        for mode in element.findall('./modes', namespaces):
                            debug_print(f"  Found mode for {component_name}")
                            for behavior in mode.findall('./behaviouralElements', namespaces):
                                behavior_type = behavior.get(f'{{{namespaces["xsi"]}}}type', '')
                                behavior_name = behavior.get('name', '')
                                debug_print(f"    Behavior: {behavior_name} (Type: {behavior_type})")
                                if behavior_type:
                                    behaviors.append({
                                        'type': behavior_type.split(':')[-1],
                                        'name': behavior_name
                                    })
                        
                        component_type = 'sensor' if 'Sensor' in component_name else \
                                        'actuator' if 'Actuator' in component_name else \
                                        'interface' if 'Interface' in component_name else \
                                        'controller'
                        
                        debug_print(f"  Identified as: {component_type}")
                        
                        components.append({
                            'name': component_name,
                            'type': component_type,
                            'in_ports': in_ports,
                            'out_ports': out_ports,
                            'behaviors': behaviors,
                            'source': 'saml'
                        })
        except Exception as e:
            print(f"Error extracting components from SAML file: {str(e)}")
            log_exception(f"SAML parsing error details: {traceback.format_exc()}")
    
    # Process HWML file if provided
    if hwml_file_path and os.path.exists(hwml_file_path):
        try:
            debug_print(f"Parsing HWML file: {hwml_file_path}")
            tree = ET.parse(hwml_file_path)
            root = tree.getroot()
            
            if root.find('./nodes', namespaces) is not None:
                debug_print("Found nodes in HWML file")
                
                # Count nodes for debugging
                node_count = len(root.findall('./nodes', namespaces))
                debug_print(f"Found {node_count} nodes")
                
                for node in root.findall('./nodes', namespaces):
                    node_name = node.get('name')
                    protocol = node.get('macProtocol', 'Unknown')
                    routing = node.get('routingProtocol', 'Unknown')
                    debug_print(f"Found node: {node_name}, Protocol: {protocol}, Routing: {routing}")
                    
                    # Get hardware details
                    hw_details = {}
                    for processor in node.findall('./microcontroller/processors', namespaces):
                        hw_details['processor'] = processor.get('name', 'Unknown')
                        hw_details['frequency'] = processor.get('frequency', 'Unknown')
                        debug_print(f"  Processor: {hw_details['processor']}, Frequency: {hw_details['frequency']}")
                    
                    for memory in node.findall('./microcontroller/memory', namespaces):
                        hw_details['memory'] = memory.get('name', 'Unknown')
                        hw_details['memory_size'] = memory.get('size', 'Unknown')
                        debug_print(f"  Memory: {hw_details['memory']}, Size: {hw_details['memory_size']}")
                    
                    # Check if this component already exists in SAML components
                    existing_component = None
                    for comp in components:
                        comp_name = comp['name'].replace(' ', '')
                        node_name_clean = node_name.replace(' ', '')
                        
                        # Check if either name contains the other
                        if node_name_clean in comp_name or comp_name in node_name_clean:
                            existing_component = comp
                            debug_print(f"  Matched with existing component: {comp['name']}")
                            break
                    
                    if existing_component:
                        # Update existing component with hardware info
                        debug_print(f"  Updating existing component {existing_component['name']} with hardware details")
                        existing_component.update({
                            'protocol': protocol,
                            'routing': routing,
                            'hw_details': hw_details,
                            'source': 'both'
                        })
                    else:
                        # Create new component
                        debug_print(f"  Creating new component for {node_name}")
                        component_type = 'sensor' if 'Sensor' in node_name else \
                                       'actuator' if 'Actuator' in node_name else \
                                       'interface' if 'Interface' in node_name else \
                                       'controller'
                        
                        debug_print(f"  Identified as: {component_type}")
                        
                        components.append({
                            'name': node_name,
                            'type': component_type,
                            'protocol': protocol,
                            'routing': routing,
                            'hw_details': hw_details,
                            'in_ports': [0],  # Default ports
                            'out_ports': [0],
                            'source': 'hwml'
                        })
        except Exception as e:
            print(f"Error extracting components from HWML file: {str(e)}")
            log_exception(f"HWML parsing error details: {traceback.format_exc()}")
    
    # Check for reserved names and rename components that might cause conflicts
    reserved_names = ["Server", "Model", "Simulator"]
    for comp in components:
        if comp['name'] in reserved_names:
            original_name = comp['name']
            comp['name'] = f"Data{comp['name']}"
            debug_print(f"Renamed component '{original_name}' to '{comp['name']}' to avoid naming conflicts")
    
    debug_print(f"Component extraction complete. Found {len(components)} components.")
    return components