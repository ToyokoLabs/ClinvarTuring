"""

Generate Q&A for model trainning

THIS IS A POC based on ClinVar sample XML found at
https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/sample_xml/RCV000077146.xml
"""
from bs4 import BeautifulSoup
import json


with open('../data/sample.xml') as f:
    data = f.read()
 
Bs_data = BeautifulSoup(data, "xml")

all_qa = []
pubdef = Bs_data.find('Attribute', {'Type':"public definition"})
# for <XRef Type="rs" ID="80358152" DB="dbSNP"/>
dbtype = Bs_data.find('XRef', {'DB': 'dbSNP'})
d = {}
id_ = dbtype.get('ID')
d["instruction"] = f"Which condition is asociated with RS{id_}?"
d["output"] = pubdef.text + f' The associated SNPedia page is https://www.snpedia.com/index.php/Rs{id_}. The NCBI page is https://www.ncbi.nlm.nih.gov/snp/{id_}.'
all_qa.append(d)
# descrption
d = {}
d["instruction"] = f"In which chromosome is located the RS{id_} SNP?"
chrm = Bs_data.find('SequenceLocation').get('Chr')
d["output"] = f'It is located in the chromosome {chrm}'
all_qa.append(d)
# MethodType
d = {}
d["instruction"] = f"Which methods support the evidence found for the RS{id_} SNP?"
methods = Bs_data.find_all('MethodType')
all_methods = set()
for method in methods:
    all_methods.add(method.text)
all_methods = list(all_methods)
d["output"] = f'Associated methods are: {",".join(all_methods)}'
all_qa.append(d)

json.dump(all_qa, open("../data/sample.json", 'w'), indent=4)

