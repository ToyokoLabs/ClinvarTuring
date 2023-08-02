#!/usr/bin/env python

import re
import sys
import gzip
import argparse
from collections import defaultdict
import xml.etree.ElementTree as ET
import time
import fileinput
import sys
import os



from xml.sax import parse
from xml.sax.handler import ContentHandler
from xml.dom.pulldom import parse, START_ELEMENT


# then sort it: cat clinvar_table.tsv | head -1 > clinvar_table_sorted.tsv; cat clinvar_table.tsv | tail -n +2 | sort  -k1,1 -k2,2n -k3,3 -k4,4 >> clinvar_table_sorted.tsv Reference on clinvar XML tag:
# ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/clinvar_submission.xsd Reference on clinvar XML tag:
# ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/README

mentions_pubmed_regex = '(?:PubMed|PMID)(.*)'  # group(1) will be all the text after the word PubMed or PMID
extract_pubmed_id_regex = '[^0-9]+([0-9]+)[^0-9](.*)'  # group(1) will be the first PubMed ID, group(2) will be all remaining text



def replace_semicolons(s, replace_with=":"):
    return s.replace(";", replace_with)


def remove_newlines_and_tabs(s):
    return re.sub("[\t\n\r]", " ", s)



FN = "ClinVarFullRelease_00-latest.xml"
event_stream = parse(FN)
id_lst = []

def parse_clinvar_tree(handle, dest=sys.stdout, multi=None, verbose=False, genome_build='GRCh37', term='Eye cancer, retinoblastoma'):
    """Parse clinvar XML
    Args:
        handle: Open input file handle for reading the XML data
        dest: Open output file handle or stream for simple variants
        multi: Open output file handle or stream for complex non-single-variant clinvar records
            (eg. compound het, haplotypes, etc.)
        verbose: Whether to write extra stats to stderr
        genome_build: Either 'GRCh37' or 'GRCh38'
    """

    curr_id = 0

    for event, elem in ET.iterparse(handle):


        if elem.tag != 'ClinVarSet' or event != 'end':
            continue

        if elem.tag == 'ClinVarSet':
            curr_id = elem.attrib.get('ID')

        print(curr_id)


        # initialize all the fields
        current_row = {}
        current_row['rcv'] = ''
        current_row['variation_type'] = ''
        current_row['variation_id'] = ''
        current_row['allele_id'] = ''

        # init new fields
        for list_column in ('inheritance_modes', 'age_of_onset', 'prevalence', 'disease_mechanism', 'xrefs'):
            current_row[list_column] = set()

        # now find the disease(s) this variant is associated with
        current_row['all_traits'] = []
        for traitset in elem.findall('.//TraitSet'):
            disease_name_nodes = traitset.findall('.//Name/ElementValue')
            trait_values = []
            for disease_name_node in disease_name_nodes:
                if disease_name_node.attrib is not None and disease_name_node.attrib.get('Type') == 'Alternate':
                    trait_values.append(disease_name_node.text)
                    if bool(re.search(term, disease_name_node.text)) == False:
                        break
                    else:
                        id_lst.append(curr_id)   # write end line

        # done parsing the xml for this one clinvar set.
        elem.clear()

    sys.stderr.write("Done\n")


def get_handle(path):
    if path[-3:] == '.gz':
        handle = gzip.open(path)
    else:
        handle = open(path)
    return handle


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract PMIDs from the ClinVar XML dump')
    parser.add_argument('-g', '--genome-build', choices=['GRCh37', 'GRCh38'],
                        help='Genome version (either GRCh37 or GRCh38)', required=True)
    parser.add_argument('-x', '--xml', dest='xml_path',
                        type=str, help='Path to the ClinVar XML dump', required=True)
    parser.add_argument('-s', '--search', type=str, required=True)
    parser.add_argument('-o', '--out', nargs='?', type=str, required=True)
    parser.add_argument('-m', '--multi', help="Output file name for complex alleles")
    

    args = parser.parse_args()

    if args.multi is not None:
        f = open(args.multi, 'w')
        parse_clinvar_tree(get_handle(args.xml_path), dest=args.out, multi=f, genome_build=args.genome_build)
        f.close()
    else:
        parse_clinvar_tree(get_handle(args.xml_path), dest=args.out, genome_build=args.genome_build, term=args.search)


print('###################Writing XML#########################')
FN = "ClinVarFullRelease_00-latest.xml"

event_stream = parse(FN)

for event, node in event_stream:
    if event == START_ELEMENT:
        if node.tagName == 'ClinVarSet':
            # print(node)'<Retinoblastoma>')
            currid = node.getAttribute('ID')
            print(currid)
            if currid in id_lst:
                print('========================================================')
                event_stream.expandNode(node)
                nodecontent = node.toxml()
                with open(args.out, 'a') as f:
                    f.write(nodecontent + '\n')
                print(nodecontent)
            else:
                #print(f'node {i}')
                pass

for line in fileinput.input([args.out], inplace=True):
    sys.stdout.write('  {l}'.format(l=line))


dname = args.out[:-4]

with open(args.out, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write('<' + dname + '>'.rstrip('\r\n') + '\n' + content)


with open(args.out, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'.rstrip('\r\n') + '\n' + content)


with open(args.out, 'a') as f:
    f.write('</' + dname + '>' + '\n')

print(args.out)
xmlout = args.out[:-3] + 'xml'
print(xmlout)
os.rename(args.out, xmlout)