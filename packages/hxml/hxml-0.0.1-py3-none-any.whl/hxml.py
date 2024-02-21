class XML:
    def __init__(self, xml_file: str) -> None:
        import xml.etree.ElementTree as ET
        from sty import fg, Style, RgbFg
        self.xml = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        fg.custom = Style(RgbFg(8, 214, 42))
        print(fg.custom + "Hello from hxml!" + fg.rs)

    def get(self, item: str):
        root_element_name = self.root.tag
        if item != root_element_name:
            print(f"Error: Provided item '{item}' does not match root element '{root_element_name}'.")
            return None
        
        data = {}
        for child in self.root:
            data[child.tag] = self._get_data_recursive(child)
        
        return data

    def _get_data_recursive(self, element):
        if len(element) == 0:
            return element.text.strip() if element.text else None
        else:
            data = {}
            for child in element:
                data[child.tag] = self._get_data_recursive(child)
            return data