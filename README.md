# protein-ids
Protein IDs for CTL numbers

## Usage:
Place the contents of https://www.ncbi.nlm.nih.gov/nuccore/NC_010287 into data/NC_010287

```
virtualenv venv
. venv/bin/activate
pip install -r requirements
python protein_ids.py
```
Output is a % seperated file data/output.txt.
