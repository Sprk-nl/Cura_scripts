# Script name: ShowLayerDetail 
# Show Layer and Type on Display via M117 command.
# 
# This Cura Post Prosessing script inserts addition M117 lines in the gcode file:
#   - Layer nr / Total Layers
#   - Layer nr / Total Layers & Type of Layer
#
# Save script in: C:\Users\[username]\AppData\Roaming\cura\3.6\scripts
# Restart Cura
# enable the script in Cura:
# Menu ‘Extensions’ → ‘Post processing’ → ‘Modify g-code’ → ‘Add a Script’ → ‘ShowLayerDetail’
# More Cura information for post prosessing: https://ultimaker.com/en/resources/20442-post-processing-plugins
# 
# This script is licensed under the Creative Commons - Attribution - Share Alike (CC BY-SA) terms
# Author: Gaston Bougie


from ..Script import Script
class ShowLayerDetail(Script):
    def __init__(self):
        super().__init__()
        
    def getSettingDataString(self):
        return """{ 
            "name":"Show Layer Detail",
            "key": "ShowLayerDetail",
            "metadata": {},
            "version": 2,
            "settings": {}
        }"""
    
    def execute(self, data):
        layer_total = "-"
        for index, layer in enumerate(data):
            new_layer = ""
            lines = layer.split("\n")
            for line in lines:
                if line:
                    new_layer += line + "\n"
                    if line.startswith(";LAYER_COUNT:"):
                        layer_total = line[13:].rstrip()
                    if line.startswith(";LAYER:"):
                        this_layer = int(line[7:].rstrip()) + 1
                        new_layer += "M117 L{0}/{1}\n".format(this_layer, layer_total)
                    if line.startswith(";TYPE:"):
                        layer_type = line[6:].rstrip()
                        new_layer += "M117 L{0}/{1} {2}\n".format(this_layer, layer_total, layer_type)
            data[index] = new_layer
        return data
