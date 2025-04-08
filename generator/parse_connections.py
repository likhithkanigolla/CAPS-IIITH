import xml.etree.ElementTree as ET
import sys
import os

def parse_connections(xml_file_path):
    """
    Parse a CAPS SAML or CAPSHWML XML file and extract all connections between components.
    """
    namespaces = {
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'components': 'components',
        'filesystem': 'filesystem'
    }
    
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        file_type = 'SAML' if root.find('./SAElements', namespaces) is not None else 'HWML'
        
        connections = []
        
        if file_type == 'SAML':
            components_by_pos = {}
            port_map = {}
            
            for i, element in enumerate(root.findall('./SAElements', namespaces)):
                element_type = element.get(f'{{{namespaces["xsi"]}}}type')
                
                if element_type and 'Component' in element_type:
                    component_name = element.get('name')
                    components_by_pos[i] = component_name
                    
                    for j, port in enumerate(element.findall('./ports', namespaces)):
                        port_reference = f"//@SAElements.{i}/@ports.{j}"
                        port_type = "input" if "InMessagePort" in port.get(f'{{{namespaces["xsi"]}}}type', '') else "output"
                        port_map[port_reference] = {
                            'component': component_name,
                            'port_idx': j,
                            'type': port_type
                        }
            
            for i, element in enumerate(root.findall('./SAElements', namespaces)):
                element_type = element.get(f'{{{namespaces["xsi"]}}}type')
                
                if element_type and 'Connection' in element_type:
                    source_port = element.get('source')
                    target_port = element.get('target')
                    
                    if source_port in port_map and target_port in port_map:
                        connections.append({
                            'source_component': port_map[source_port]['component'],
                            'source_port': port_map[source_port]['port_idx'],
                            'source_port_type': port_map[source_port]['type'],
                            'target_component': port_map[target_port]['component'],
                            'target_port': port_map[target_port]['port_idx'],
                            'target_port_type': port_map[target_port]['type']
                        })
                    else:
                        print(f"Warning: Connection {i} has missing ports: {source_port} -> {target_port}")
        
        elif file_type == 'HWML':
            node_map = {}
            
            for node in root.findall('./nodes', namespaces):
                node_name = node.get('name')
                protocol = node.get('macProtocol', 'Unknown')
                routing = node.get('routingProtocol', 'Unknown')
                
                node_map[node_name] = {
                    'protocol': protocol,
                    'routing': routing
                }
            
            node_list = list(node_map.keys())
            for i in range(len(node_list)):
                for j in range(i + 1, len(node_list)):
                    connections.append({
                        'source_component': node_list[i],
                        'source_port': node_map[node_list[i]]['protocol'],
                        'source_port_type': node_map[node_list[i]]['routing'],
                        'target_component': node_list[j],
                        'target_port': node_map[node_list[j]]['protocol'],
                        'target_port_type': node_map[node_list[j]]['routing']
                    })
        
        return connections
    except Exception as e:
        print(f"Error parsing XML file: {str(e)}")
        return []

def format_connections(connections):
    """Format the connections for better readability."""
    return [
        f"From: {conn['source_component']} ({conn['source_port']} - {conn['source_port_type']}) → "
        f"To: {conn['target_component']} ({conn['target_port']} - {conn['target_port_type']})"
        for conn in connections
    ]

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_connections_fixed.py <path_to_xml_file>")
        sys.exit(1)
    
    xml_file_path = sys.argv[1]
    if not os.path.exists(xml_file_path):
        print(f"Error: File {xml_file_path} does not exist")
        sys.exit(1)
    
    connections = parse_connections(xml_file_path)
    if connections:
        print(f"Found {len(connections)} connections:")
        for idx, connection in enumerate(format_connections(connections), 1):
            print(f"{idx}. {connection}")
    else:
        print("No connections found in the XML file")

if __name__ == "__main__":
    main()
