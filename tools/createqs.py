"""

Generate Q&A for model trainning

THIS IS A POC based on ClinVar sample XML found at
https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/sample_xml/RCV000077146.xml
"""
from bs4 import BeautifulSoup
import json
from xml.sax import parse
from xml.sax.handler import ContentHandler

from xml.dom.pulldom import parse, START_ELEMENT



FN = "retinoblastoma.xml"

event_stream = parse(FN)
for event, node in event_stream:
    if event == START_ELEMENT:
        if node.tagName == 'ClinVarSet':

            event_stream.expandNode(node)
            print(node)
            nodecontent = node.toxml()
            with open('temp.xml', 'w') as f:
                f.write(nodecontent)

            with open('temp.xml') as f:
                data = f.read()

            Bs_data = BeautifulSoup(data, "xml")


            all_qa = []
            pubdef = Bs_data.find('Attribute', {'Type':"public definition"})

            # for <XRef Type="rs" ID="80358152" DB="dbSNP"/>
            dbtype = Bs_data.find('XRef', {'DB': 'dbSNP'})


            d = {}
            try:
                id_ = dbtype.get('ID')
                id_ = 'RS' + id_ + ' SNP'
            except AttributeError:
                id_ = Bs_data.find('Measure').get('ID')
                if Bs_data.find('Measure').get('Type') == 'Deletion':
                    id_ = 'DEL' + id_
                elif Bs_data.find('Measure').get('Type') == 'single nucleotide variant':
                    id_ = 'SNV' + id_
                elif Bs_data.find('Measure').get('Type') == 'Duplication':
                    id_ = 'DUP' + id_
                elif Bs_data.find('Measure').get('Type') == 'Indel':
                    id_ = 'IND' + id_
                elif Bs_data.find('Measure').get('Type') == 'Inversion':
                    id_ = 'INV' + id_
                elif Bs_data.find('Measure').get('Type') == 'Insertion':
                    id_ = 'INS' + id_
                else:
                    print("Measure variation error")
                
            print(id_)
            d["instruction"] = f"Which condition is asociated with {id_}?"
            d["output"] = pubdef.text + f' The associated SNPedia page is https://www.snpedia.com/index.php/Rs{id_}. The NCBI page is https://www.ncbi.nlm.nih.gov/snp/{id_}.'
            all_qa.append(d)


            # descrption
            d = {}
            d["instruction"] = f"In which chromosome is {id_} located?"
            chrm = Bs_data.find('SequenceLocation').get('Chr')
            d["output"] = f'It is located in the chromosome {chrm}.'
            all_qa.append(d)


            # MethodType
            d = {}
            d["instruction"] = f"Which methods support the evidence found for the {id_}?"
            methods = Bs_data.find_all('MethodType')
            all_methods = set()
            for method in methods:
                all_methods.add(method.text)
            all_methods = list(all_methods)
            d["output"] = f'Associated methods are: {", ".join(all_methods)}.'
            all_qa.append(d)


            #pathogenic?
            d = {}
            d["instruction"] = f"What is the clinical significance of {id_}, is it benign or pathogenic?"
            patho = Bs_data.find('Description').text
            d["output"] = f'It is {patho}.'
            all_qa.append(d)


            #variation length
            d = {}
            d["instruction"] = f"How long is the variation length for {id_}?"
            leng = Bs_data.find('SequenceLocation').get('variantLength')
            d["output"] = f'The variation length is {leng} base pairs.'
            all_qa.append(d)

            #origin
            d = {}
            d["instruction"] = f"What is the origin for {id_}?"
            ori = Bs_data.find('Origin').text
            d["output"] = f'The origin is {ori}.'
            all_qa.append(d)


            #var type
            d = {}
            d["instruction"] = f"What is the type of genetic variation for {id_}?"
            vari = Bs_data.find('Measure').get('Type')
            d["output"] = f'The variation is a {vari}.'
            all_qa.append(d)

            #consequence
            if Bs_data.find("Attribute", {"Type": "MolecularConsequence"}) != None:
                d = {}
                d["instruction"] = f"What is the genetic molecular consequence for {id_}?"
                cons = Bs_data.find("Attribute", {"Type": "MolecularConsequence"}).text
                d["output"] = f'The resulting gene consequence is a {cons}.'
                all_qa.append(d)

            json.dump(all_qa, open("data/sample.json", 'a'), indent=4)

            open('temp.xml', 'w').close()

