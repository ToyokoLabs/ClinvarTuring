"""
filter separate xml into files
"""


from xml.sax import parse
from xml.sax.handler import ContentHandler

from xml.dom.pulldom import parse, START_ELEMENT
import time


FN = "ClinVarFullRelease_00-latest.xml"


DISEASE = 'retinoblastoma'

file1 = open('debug.txt', 'r')
Lines = file1.readlines()
# Strips the newline character
new_list = [item.strip() for item in Lines]


i = 0
event_stream = parse(FN)
for event, node in event_stream:
    if event == START_ELEMENT:
        if node.tagName == 'ClinVarSet':
            # print(node)
            i += 1
            curr_id = node.getAttribute('ID')
            print(curr_id)
            if curr_id in new_list:
                print('========================================================')
                event_stream.expandNode(node)
                nodecontent = node.toxml()
                with open('retinoblastoma.txt', 'a') as f:
                    f.write(nodecontent + '\n')
                print(nodecontent)
            else:
                #print(f'node {i}')
                pass