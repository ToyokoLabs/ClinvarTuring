"""

Generate Q&A for model trainning

THIS IS A POC based on ClinVar sample XML found at
https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/sample_xml/RCV000077146.xml
"""
from bs4 import BeautifulSoup
import json



FN = "../retinoblastoma2.xml"

type_dict = {'Deletion': 'DEL',
            'single nucleotide variant': 'SNV',
            'Duplication': 'DUP',
            'Indel': 'IND',
            'Inversion': 'INV',
            'Insertion': 'INS'}

with open(FN) as data:
    Bs_data = BeautifulSoup(data, "xml")
    clinvar_set = Bs_data.find_all('ClinVarSet')
    print(len(clinvar_set))
    all_qa = []
    for clinvs in clinvar_set:
        #print(clinvs)
        pubdef = clinvs.find('Attribute', {'Type':"public definition"})
        # for <XRef Type="rs" ID="80358152" DB="dbSNP"/>
        dbtype = clinvs.find('XRef', {'DB': 'dbSNP'})
        d = {}
        try:
            id_ = 'RS' + dbtype.get('ID') + ' SNP'
        except AttributeError:
            id_ = clinvs.find('Measure').get('ID')
            id_ = type_dict[clinvs.find('Measure').get('Type')] + id_
        d["instruction"] = f"Which condition is asociated with {id_}?"
        d["output"] = pubdef.text + f' The associated SNPedia page is https://www.snpedia.com/index.php/Rs{id_}. The NCBI page is https://www.ncbi.nlm.nih.gov/snp/{id_}.'
        all_qa.append(d)
        # descrption
        d = {}
        d["instruction"] = f"In which chromosome is {id_} located?"
        chrm = clinvs.find('SequenceLocation').get('Chr')
        d["output"] = f'It is located in the chromosome {chrm}.'
        all_qa.append(d)
        # MethodType
        d = {}
        d["instruction"] = f"Which methods support the evidence found for the {id_}?"
        methods = clinvs.find_all('MethodType')
        all_methods = set()
        for method in methods:
            all_methods.add(method.text)
        all_methods = list(all_methods)
        d["output"] = f'Associated methods are: {", ".join(all_methods)}.'
        all_qa.append(d)
        #pathogenic?
        d = {}
        d["instruction"] = f"What is the clinical significance of {id_}, is it benign or pathogenic?"
        patho = clinvs.find('Description').text
        d["output"] = f'It is {patho}.'
        all_qa.append(d)
        #variation length
        d = {}
        d["instruction"] = f"How long is the variation length for {id_}?"
        leng = clinvs.find('SequenceLocation').get('variantLength')
        d["output"] = f'The variation length is {leng} base pairs.'
        all_qa.append(d)
        #origin
        d = {}
        d["instruction"] = f"What is the origin for {id_}?"
        ori = clinvs.find('Origin').text
        d["output"] = f'The origin is {ori}.'
        all_qa.append(d)
        #var type
        d = {}
        d["instruction"] = f"What is the type of genetic variation for {id_}?"
        vari = clinvs.find('Measure').get('Type')
        d["output"] = f'The variation is a {vari}.'
        all_qa.append(d)
        #consequence
        if clinvs.find("Attribute", {"Type": "MolecularConsequence"}) != None:
            d = {}
            d["instruction"] = f"What is the genetic molecular consequence for {id_}?"
            cons = clinvs.find("Attribute", {"Type": "MolecularConsequence"}).text
            d["output"] = f'The resulting gene consequence is a {cons}.'
            all_qa.append(d)

with open("../data/retinoblastoma2.json", 'w') as f:
    json.dump(all_qa, f, indent=4)
