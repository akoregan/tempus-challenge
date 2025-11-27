#!/usr/bin/env bash

# [0] run checks

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: ./run_with_docker.sh <input_vcf>"
    exit 1
fi

VEP_INPUT="$1"
VEP_OUTPUT_BASENAME="vep_annotated_output.vcf"

mkdir -p ./temp

# [1] run VEP in docker

echo "Running VEP..."

docker run \
  -v "$HOME/vep_data":/data \
  -v "$PWD":/input \
  -v "$PWD/temp":/output \
  ensemblorg/ensembl-vep \
    vep \
    --cache --offline \
    --assembly GRCh37 \
    --format vcf --vcf \
    --pick --everything \
    --force_overwrite \
    -i "/input/${VEP_INPUT}" \
    -o "/output/${VEP_OUTPUT_BASENAME}"

# [2] split and query with BCFTools

echo "...VEP completed..."

for SAMPLE in $(bcftools query -l "./temp/${VEP_OUTPUT_BASENAME}"); do
    echo "Running bcftools and python on sample: ${SAMPLE} ... "

    BCF_OUTPUT_FILEPATH="./temp/bcftools_${SAMPLE}_output.tsv"

    bcftools +split-vep "./temp/${VEP_OUTPUT_BASENAME}" \
        -d \
        -c SYMBOL,Gene,Feature,VARIANT_CLASS,BIOTYPE,Consequence,IMPACT \
    | bcftools query \
        -H \
        -s "$SAMPLE" \
        -f '%CHROM\t%POS\t%REF\t%ALT{0}\t%ALT{1}[\t%GT\t%DP\t%RO\t%AO{0}\t%AO{1}]\t%SYMBOL\t%Gene\t%Feature\t%VARIANT_CLASS\t%BIOTYPE\t%Consequence\t%IMPACT\n' \
        > "$BCF_OUTPUT_FILEPATH"

    # [3] process with python
    python ./python/write_variant_csv.py "$BCF_OUTPUT_FILEPATH" "$SAMPLE"

    rm "$BCF_OUTPUT_FILEPATH"
done

echo "...annotation completed!"

rm "./temp/${VEP_OUTPUT_BASENAME}"
rm "./temp/${VEP_OUTPUT_BASENAME}_summary.html"
