# tempus-challenge

Introduction: This repository extracts variant information from a provided VCF file and implements the Ensembl's VEP API to determine consequences of the alternate allele, recording the output in CSV format.

The VCF data feature two sample columns, one titled *normal* and the other, *vaf5*. The genotypes in each of these columns are unfailingly the same. And because the depth and other data formats are often equivalent, the samples are likely the same one having undergone distinct pre-processing. To avoid recording redundant data, I have provided the user with the option to analyze the data labeled as *normal* or *vaf5* via an input parameter to the CLI. Both outputs recorded in the results folder.

Output: The impact (```HIGH, MEDIUM, LOW, MODIFIER```) has been provided as a means of filtering by severity.

| CSV Parameter Name | Description |
| :----------------: | :---------: |
| Gene Name          | Test        |
| Gene ID            | Test        |

Getting Started: This program can be run from the command-line as a shell script. Relevant VCF format data are extracted using the bcftools ```toolkit```. Downstream formatting and API calls are executed in python. 
