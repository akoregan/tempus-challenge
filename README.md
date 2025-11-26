# tempus-challenge

Introduction: This repository describes a variant annotation tool. To execute the program use **run_docker_pipeline.sh** to produce a CSV file output, which includes each variant's sequencing depth, allele frequencies (as percentages), and VEP annotations. 

the fields: depth of sequencing; reference (PERC-REF), alternative (PERC-ALT), and minor allele frequencies (PERC-ALT-MINOR); as well as the Ensembl VEP fields gene symbol (GENE-SYMBOL), type of variation (VARIATION-CLASS), effect of variation (), etc.

Caveats

BCFTools and NextFlow can both be downloaded directly into a Conda (or Mamba) environment from the Bioconda channel: ```conda install -c bioconda -c conda-forge bcftools nextflow```.

The VCF data feature two sample columns, one titled *normal* and the other, *vaf5*. The genotypes in each of these columns are unfailingly the same. And because the depth and other data formats are often equivalent, the samples are likely the same one having undergone distinct pre-processing. To avoid recording redundant data, I have provided the user with the option to analyze the data labeled as *normal* or *vaf5* via an input parameter to the CLI. Both outputs recorded in the results folder.

Output: The impact (**HIGH, MEDIUM, LOW, MODIFIER**) has been provided as a means of filtering by severity.

| CSV Column Name               |
| CSV Column Name | Description |
| :-------------: | :---------: |
| CHROM           | Test        |
| POS             | Test        |
| Gene Name       | Test        |
| Gene ID         | Test        |
| Gene Name       | Test        |
| Gene ID         | Test        |
| Gene Name       | Test        |
| Gene ID         | Test        |

Getting Started: This program can be run from the command-line as a shell script. Relevant VCF format data are extracted using the bcftools ```toolkit```. Downstream formatting and API calls are executed in python. 

Only reports the first-ranked transcript according to the Ensembl VEP's pick parameter (ranking system [here](https://useast.ensembl.org/info/docs/tools/vep/script/vep_other.html#pick)). This summarizes data for the sake of simplicity. The results CSV therefore risks ignoring crucial transcript and regulatory feature consequences. 

```
docker run -it \
  -v "$PWD/.vep":/opt/vep/.vep \
  ensemblorg/ensembl-vep \
  INSTALL.pl -a cf -s homo_sapiens -y GRCh37

```


```
python variant_annotator.py <filename.tsv> <sample_name>
```
