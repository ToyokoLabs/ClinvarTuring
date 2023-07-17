"""
filter separate xml into files
"""


from xml.sax import parse
from xml.sax.handler import ContentHandler

from xml.dom.pulldom import parse, START_ELEMENT
import time


FN = "ClinVarFullRelease_00-latest.xml"


DISEASE = 'retinoblastoma'

i = 0
event_stream = parse(FN)
for event, node in event_stream:
    if event == START_ELEMENT:
        if node.tagName == 'ClinVarSet':
            #print(node)
            i += 1
            event_stream.expandNode(node)
            nodecontent = node.toxml()
            if DISEASE in nodecontent.lower():
                clinvarassertions = node.getElementsByTagName("ClinVarAssertion")
                for cva in clinvarassertions:
                    traitset = cva.getElementsByTagName('TraitSet')
                    for trait in traitset:
                        if trait.hasAttribute("Type") and trait.getAttribute("Type")=='Disease':
                            for name in trait.getElementsByTagName("ElementValue"):
                                if DISEASE in name.toxml():
                                    print(nodecontent)
            else:
                #print(f'node {i}')
                pass



