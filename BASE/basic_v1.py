import xml.etree.ElementTree as ET

class CAPSParser:
    def __init__(self, hwml_file, saml_file):
        self.hwml_file = hwml_file
        self.saml_file = saml_file
        self.hardware_info = {}
        self.software_behavior = {}

    def parse_hwml(self):
        """ Parses the .capshwml file to extract hardware information """
        tree = ET.parse(self.hwml_file)
        root = tree.getroot()

        node = root.find(".//nodes")
        if node is not None:
            self.hardware_info["name"] = node.get("name", "UnknownNode")
            self.hardware_info["OS"] = node.get("OS", "UnknownOS")
            self.hardware_info["macProtocol"] = node.get("macProtocol", "UnknownMAC")
            self.hardware_info["routingProtocol"] = node.get("routingProtocol", "UnknownRouting")

        microcontroller = node.find(".//microcontroller")
        if microcontroller is not None:
            processor = microcontroller.find(".//processors")
            if processor is not None:
                self.hardware_info["processor"] = {
                    "name": processor.get("name", "UnknownProcessor"),
                    "frequency": processor.get("frequency", "0"),
                    "cpi": processor.get("cpi", "0"),
                }

        memory = microcontroller.find(".//memory")
        if memory is not None:
            self.hardware_info["memory"] = {"type": memory.get("name", "UnknownMemory"), "size": memory.get("size", "0")}

    def parse_saml(self):
        """ Parses the .capssaml file to extract software behavior """
        tree = ET.parse(self.saml_file)
        root = tree.getroot()

        for element in root.findall(".//SAElements"):
            component_name = element.get("name", "UnknownComponent")
            self.software_behavior[component_name] = []

            for mode in element.findall(".//modes"):
                for behavior in mode.findall(".//behaviouralElements"):
                    self.software_behavior[component_name].append(behavior.get("name", "UnknownBehavior"))

    def get_parsed_data(self):
        return {
            "hardware": self.hardware_info,
            "software": self.software_behavior,
        }

# Example Usage
hwml_path = "../SAML-SAMPLE/model/FirstProgram.capshwml"
saml_path = "../SAML-SAMPLE/model/FirstProgram.capssaml"

parser = CAPSParser(hwml_path, saml_path)
parser.parse_hwml()
parser.parse_saml()

parsed_data = parser.get_parsed_data()
print(parsed_data)  # Check extracted details
