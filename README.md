# tempus-challenge

### Introduction 
This repository describes a variant annotation tool. To execute the program use **run_docker_pipeline.sh** to produce a CSV file output, which includes each variant's sequencing depth, allele frequencies (as percentages), and VEP annotations. A list of CSV columns and their descriptions are provided in the Appendix below.


### Description
The **run_docker_pipeline.sh** shell script contains three sections: 
1. first, the VEP API is run locally on the input VCF file using a Docker container
1. second, BCFTools extracts relevant data and restructures it as a TSV file from downstream processing 
1. lastly, a python script *write_variant_csv.py* reformats the TSV file, calculates allele frequencies, and writes the annotated CSV file output

***Note*** that the provided VCF file features two sample columns: *normal* and *vaf5*. Their similarity (consistent genotypes, equivalent sequencing depth, etc.) suggests they originate from a common source and have been processed differently. The **run_docker_pipeline.sh** scipt requires the user to specify which of these two samples is relevant for analysis. The outputs of both options are recorded in the results folder.

***Caveats*** This pipeline uses the VEP's *--pick* parameter for the sake of simplicity, reporting a single transcipt according to its [ranking system](https://useast.ensembl.org/info/docs/tools/vep/script/vep_other.html#pick). Consequently, the results may miss relevant transcipt and regulatory feature predictions, or may be modified according to the specific interests of users.


### Getting Started

#### Install Ensembl VEP Docker Image and BCFTools

Ensembl provides specific documentation for installing the ensemblorg/ensembl-vep image [here](https://useast.ensembl.org/info/docs/tools/vep/script/vep_download.html#docker). Navigate to these guidelines or follow the process outlined below.
```
# [1] download ensembl-vep docker image
docker pull ensemblorg/ensembl-vep

# [2] set up cache and fasta files; note that the VCF file specifies the GRCh37 assembly
docker run -t -i -v $HOME/vep_data:/data ensemblorg/ensembl-vep INSTALL.pl -a cf -s homo_sapiens -y GRCh37
```

BCFTools can be downloaded directly into a Conda (Mamba) environment from the Bioconda channel: ```conda install -c bioconda -c conda-forge bcftools```. Alternatively, utilize the ```.yml``` file in the *envs* folder to create an environment that includes BCFTools.


#### Run the Shell Script

Ensure that the input VCF file is located in the repository's root directory. From this directory, execute **run_docker_pipeline.sh** by passing the VCF input's basename and the sample name as arguments: ```./run_docker_pipeline.sh tempus_challenge_data.vcf normal``` or ```./run_docker_pipeline.sh tempus_challenge_data.vcf vaf5```.


### Appendix

| CSV Column Name   | Description				                                    		   |
| :---------------- | :----------------------------------------------------------- |
| CHROM             | chromosome      		                              				   |
| POS               | start position on chromosome                        			   |
| REF	              | reference allele identity        	                  			   |
| ALT	              | alternative allele identity        			                     |    
| ALT-MINOR         | minor allele identity (if present)      			               |
| DEPTH	            | depth of sequencing       				                           |
| PERC-REF          | frequency of reference allele as a percentage        	       |
| PERC-ALT          | frequency of alternative allele as a percentage        	     |
| PERC-ALT-MINOR    | frequency of minor allele as a percentage (if present)       |
| GENE-SYMBOL       | HGNC gene symbol       					                             |
| GENE-ID           | Ensembl stable gene identifier (prefix: ENSG)        	       |
| TRANSCRIPT-ID     | Ensembl stable transcript identifier (prefix: ENST)          |
| VARIANT-CLASS     | type of variation (i.e. SNV, duplication)        		         | 
| TRANSCRIPT-BIOTYPE| biological classification of transcript     		             |
| VARIATION-EFFECT  | consequence(s) of variation       			                     |
| IMPACT-SCORE      | impact can be: HIGH, MEDIUM, LOW, or MODIFIER    	           |
