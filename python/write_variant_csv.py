import pandas as pd
import sys
import argparse
import datetime
import pathlib

### ### ###

date = datetime.datetime.today().strftime("%Y%b%d")

### ### ###
# [1] check CLI usage and read in vcf tsv data

parser = argparse.ArgumentParser()
parser.add_argument ("filename", help = "input TSV file")
parser.add_argument ("sample_name", help = "sample name from VCF file")
args = parser.parse_args()

input_path = pathlib.Path (args.filename)
vcf_sample_name = args.sample_name

if not input_path.is_file() :
    print ("Invalid filepath.")
    sys.exit(1)

variant_df = pd.read_csv (input_path, sep = '\t')

# [2] reformat column titles and select column values

col_mapper = {

    "#[1]CHROM"                 :   "CHROM",
    "[2]POS"                    :   "POS",
    "[3]REF"                    :   "REF",
    "[4]ALT"                    :   "ALT-A",
    "[5]ALT"                    :   "ALT-B",
    f"[6]{vcf_sample_name}:GT"  :   "GENOTYPE",
    f"[7]{vcf_sample_name}:DP"  :   "DEPTH",
    f"[8]{vcf_sample_name}:RO"  :   "COUNT-REF",
    f"[9]{vcf_sample_name}:AO"  :   "COUNT-ALT",
    f"[10]{vcf_sample_name}:AO" :   "COUNT-ALT-MINOR",
    "[11]SYMBOL"                :   "GENE-SYMBOL",
    "[12]Gene"                  :   "GENE-ID",
    "[13]Feature"               :   "TRANSCRIPT-ID",
    "[14]VARIANT_CLASS"         :   "VARIANT-CLASS",
    "[15]BIOTYPE"               :   "TRANSCRIPT-BIOTYPE",
    "[16]Consequence"           :   "VARIATION-EFFECT",
    "[17]IMPACT"                :   "IMPACT-SCORE"

}

if list(variant_df.columns) != list(col_mapper.keys()) : # check validity of col_mapper
    print ("Columns don't match mapper. Exiting program.")
    sys.exit(1)

variant_df = variant_df.rename (columns = col_mapper)

for item in ["TRANSCRIPT-BIOTYPE", "VARIATION-EFFECT", "VARIANT-CLASS"] : 
    variant_df[item] = variant_df[item].str.upper()

# [3] use count columns to calculate percentage reads

numeric_cols = ["POS", "DEPTH", "COUNT-REF", "COUNT-ALT", "COUNT-ALT-MINOR"]
variant_df[numeric_cols] = variant_df[numeric_cols].apply(pd.to_numeric, errors="coerce")
variant_df.insert (10, "PERC-REF", (100 * variant_df["COUNT-REF"]/variant_df["DEPTH"]).round(2) )
variant_df.insert (11, "PERC-ALT", (100 * variant_df["COUNT-ALT"]/variant_df["DEPTH"]).round(2) )
variant_df.insert(12, "PERC-ALT-MINOR", (100 * variant_df["COUNT-ALT-MINOR"] / variant_df["DEPTH"]).round(2))

# [4] save dataframe as csv to results folder

variant_df = variant_df.fillna(".")

output_dir = pathlib.Path ("./results")
output_dir.mkdir (exist_ok = True)

variant_df.to_csv (
    pathlib.Path.joinpath (output_dir, f"annotated_{vcf_sample_name}_{date}.csv"), 
    index = False
)