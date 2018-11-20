# Script name: ShowLayerDetail 
# Show Layer and Type on Display via M117 command.
# 
# This script inserts addition lines in the gcode file
#   - Layer nr / Total Layers
#   - Layer nr / Total Layers & Type of Layer
# 
# This script is licensed under the Creative Commons - Attribution - Share Alike (CC BY-SA) terms
# Author: Gaston Bougie
#
# To do:
# - Give users the option to change display layout
# - Use option M118 to send information to octoprint over serial like: action:disconnect, action:pause and action:resume
# - Example: 
#            x-axis home (or almost left)
#            Y-axis  brings bed up front for clear viewitems
#            M118 action:photo
#            wait x seconds (howto in Marlin?)
#            Octopy grabs a picture
#            continue printing next layer
# - Add an octoprint option to create a snapshop on a layer
# - Add snapshot hotend location presets, and let user customize
# - As you know the total layers, and layer position, imagine a camera connected to the hotend and use X-axis with close-up camera



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
