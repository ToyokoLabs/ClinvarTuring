# Summary of each files

`parser.py` returns an xml file filtered to the disease we are looking for.


`createqs.py` takes as input an xml of disease-specific variations and create json question sets based on the contents of each xml node. A temporary `temp.xml` containing the current node content is generated during intermediary stages of parsing. For cases where the variation does not have a SNP id, variation ids are used instead (e.g. Deletion, single nucleotide variation, etc). These question sets are outputted in `sample.json`.

The steps below walk you through on how to use these files.

# Walkthrough

## parser.py
Example command:
```python tools/parser.py --g 'GRCh37' --x ClinVarFullRelease_00-latest.xml --s 'Eye cancer, retinoblastoma' --o 'retinoblastoma.txt'```

## createqs.py
3. In line 17, change the name of the input file to the output file for last step. This is the document with filtered xmls (default retinoblastoma.xml).
4. Run ```python tools/createqs.py``` to generate a json of question sets corresponding to variations.