

import xml.etree.ElementTree as ET
tree = ET.parse('/home/dinforma/rdfal/CKG/data/full database.xml')
root = tree.getroot()

sSet= set()
for child in root:
    sSet.add(str(child.attrib))
    #print(child.tag, child.attrib)
print(sSet)