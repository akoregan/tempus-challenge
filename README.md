# tempus-challenge

Introduction: This repository extracts variant information from a provided VCF file and implements the Ensembl's VEP API to determine consequences of the alternate allele, recording the output in CSV format.

Getting Started: This program can be run from the command-line as a shell script. Relevant VCF format data are extracted using the bcftools ```toolkit```. Downstream formatting and API calls are executed in python. 
