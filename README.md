# tempus-challenge

### Introduction 
This repository describes a variant annotation tool by accessing VCF input data and processing it using Ensembl's VEP API, BCFTools, and a custom python script. To execute the program use **run_docker_pipeline.sh**, which will produce a CSV file output including each variant's sequencing depth, percentage reads, and VEP annotations. A list of CSV columns and their descriptions is provided in the Appendix below. 

### Description
The **run_docker_pipeline.sh** shell script contains three sections: 
1. First, the VEP annotation runs locally inside a Docker container using a mounted VEP cache. Using a local cache significantly improves performance by avoiding thousands of remote requests to Ensembl servers.
1. Second, BCFTools extracts relevant data fields and restructures it as a TSV file for downstream processing.
1. Last, the python script *write_variant_csv.py* reformats the TSV file, calculates percentage reads, and writes the annotated data to a CSV file.

***Note*** that the provided VCF file features two sample columns: *normal* and *vaf5*. Their similarity (consistent genotypes, equivalent sequencing depth, etc.) suggests they originate from a common source and have been processed differently. The **run_docker_pipeline.sh** script writes a distinct CSV annotation file for each of these sample IDs because of their likely redundancy. It is therefore **not appropriate to calculate the minor allele frequency**, as this metric refers to a population-level calculation. The present VCF file reveals that allele frequencies (*INFO=AF*) merely reflect the sample's genotype.

***Caveats*** This pipeline uses the VEP's *--pick* parameter for the sake of simplicity, reporting a single transcipt according to its [ranking system](https://useast.ensembl.org/info/docs/tools/vep/script/vep_other.html#pick). Consequently, the results may miss relevant transcipt and regulatory feature predictions as well as differences across multiple alternate alleles, or it may be modified according to the specific interests of users. 


### Getting Started

#### Install Ensembl VEP Docker Image and BCFTools

Ensembl provides specific documentation for installing the ensemblorg/ensembl-vep image [here](https://useast.ensembl.org/info/docs/tools/vep/script/vep_download.html#docker). Navigate to these guidelines or follow the installation described below.
```
# [1] download ensembl-vep docker image
docker pull ensemblorg/ensembl-vep

# [2] set up cache and fasta files; note that the VCF file specifies the GRCh37 assembly
docker run -t -i -v $HOME/vep_data:/data ensemblorg/ensembl-vep INSTALL.pl -a cf -s homo_sapiens -y GRCh37
```

BCFTools can be downloaded directly into a Conda (Mamba) environment from the Bioconda channel: ```conda install -c bioconda -c conda-forge bcftools```. Alternatively, utilize the ```.yml``` file in the *envs* folder to create an environment that includes BCFTools (as well as other dependencies).


#### Run the Shell Script

Ensure that the input VCF file is located in the repository's root directory. From this directory, first ensure that **run_docker_pipeline.sh** is executable. Then, run the pipeline by passing the VCF input's basename to the shell script as its only argument: 
```
# run the pipeline 
./run_docker_pipeline.sh tempus_challenge_data.vcf
```


### Appendix

| CSV Column Name   | Description				                                    		   |
| :---------------- | :----------------------------------------------------------- |
| CHROM             | chromosome      		                              				   |
| POS               | start position on chromosome                        			   |
| REF	              | reference allele identity        	                  			   |
| ALT-A             | alternative allele identity        			                     |    
| ALT-B             | minor allele identity (if present)      			               |
| DEPTH	            | depth of sequencing       				                           |
| PERC-REF          | frequency of reference allele as a percentage        	       |
| PERC-ALT-A        | frequency of alternative allele as a percentage        	     |
| PERC-ALT-B        | frequency of minor allele as a percentage (if present)       |
| GENE-SYMBOL       | HGNC gene symbol       					                             |
| GENE-ID           | Ensembl stable gene identifier (prefix: ENSG)        	       |
| TRANSCRIPT-ID     | Ensembl stable transcript identifier (prefix: ENST)          |
| VARIANT-CLASS     | type of variation (i.e. SNV, duplication)        		         | 
| TRANSCRIPT-BIOTYPE| biological classification of transcript     		             |
| VARIATION-EFFECT  | consequence(s) of variation       			                     |
| IMPACT-SCORE      | impact can be: HIGH, MEDIUM, LOW, or MODIFIER    	           |
