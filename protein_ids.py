"""
_protein_ids_
"""

import re

import BeautifulSoup


def import_genome(fname="data/NC_010287"):
    with open(fname, "r+") as f:
        soup = BeautifulSoup.BeautifulSoup(f)

    cds_spans = soup.findAll("span", id=re.compile(".*_CDS_.*"))
    return cds_spans


def parse_genome(cds_spans):
    output = []
    for s in cds_spans:
        # some may have no information at all
        required = ["gene", "locus_tag", "product", "protein_id"]
        if not any([r in s.text for r in required]):
            continue

        # gene may not be named
        gene_match = re.search('.*gene="(.*)".*', s.text)
        if gene_match:
            gene = gene_match.group(1)
        else:
            gene = "N/A"

        locus_tag = re.search('.*locus_tag="(.*)".*', s.text).group(1)
        try:
            # these should exist, but some of the HTML is split weird
            product = re.search('.*product="([ ,\[\]\'\na-zA-Z0-9^/_()+-]*)".*', s.text).group(1)
            product = re.sub('\s+', ' ', product).strip()
            protein_id = re.search('.*protein_id="(.*)".*', s.text).group(1)
            output.append({
                "gene": gene,
                "locus_tag": locus_tag,
                "product": product,
                "protein_id": protein_id
            })
        except Exception:
            output.append({"locus_tag": locus_tag})

    return output
    

def write_output(output, fname="data/output.txt"):
    with open(fname, "w+") as f:
        f.write("locus_tag%gene%product%protein_id\n")
        for o in output:
            f.write(
                "{}%{}%{}%{}\n".format(
                    o["locus_tag"],
                    o.get("gene", "ERR"),
                    o.get("product", "ERR"),
                    o.get("protein_id", "ERR")
                )
            )


if __name__ == "__main__":
    print("Processing data...")
    cds_spans = import_genome()
    output = parse_genome(cds_spans)
    print("Writing data...")
    write_output(output)
    print("Done!")
