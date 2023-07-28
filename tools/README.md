# Summary of each files

`parser.py` filters the full clinvar release xml for the diseases we are looking for. It takes as input the full clinvar release xml, a search string for disease (defined within the code), and outputs IDs of variations containing that disease string. This list of IDs is stored in `debug.txt` in base directory.

`mod_xmlfilter.py` takes the file of IDs as input and pulls the corresponding Clinvars nodes into a new text file `retinoblastoma.txt` as output. The text file will contain all Clinvar xmls related to the disease.

`createqs.py` takes as input an xml of disease-specific variations and create json question sets based on the contents of each xml node. A temporary `temp.xml` containing the current node content is generated during intermediary stages of parsing. For cases where the variation does not have a SNP id, variation ids are used instead (e.g. Deletion, single nucleotide variation, etc). These question sets are outputted in `sample.json`.

The steps below walk you through on how to use these files.

# Walkthrough

## parser.py
1. In line 119, change the string content of `re.search` to the name of disease you are looking for (default 'Eye cancer, retinoblastoma')
2. In line 122, change the name of the output file where the IDs are stored (default debug.txt)
3. Run ```python tools/parser.py --g 'GRCh37' --x ClinVarFullRelease_00-latest.xml```. The code will loop through all Clinvar IDs within the full release, writing the ones with target disease keyword in the specified file.

 By now you should have a debug.txt file in base directory

## mod_xmlfilter
4. In line 18, change the name of the input file for this step to the output file for last step. This is the document containing a list of IDs (default debug.txt).
5. In line 37, change the name of the output file where the variation xmls are stored (default retinoblastoma.txt)
6. Run ```python tools/mod_xmlfilter.py```. The code will loop through all Clinvar IDs within the full release, pulling xml nodes whose IDs appear in debug.txt into retinoblastoma.txt
7. Rename .txt into .xml for the output file
8. Add <Disease_name>...</Disease_name> brackets at top and bottom of documents.

## createqs.py
9. In line 17, change the name of the input file to the output file for last step. This is the document with filtered xmls (default retinoblastoma.xml).
10. Run ```python tools/createqs.py``` to generate a json of question sets corresponding to variations.