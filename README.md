 # ATACseq_pipeline

This is an automatic pipeline of processing ATAC-seq data, which includes adapter-trimming, alignment, filtering and ploting.

## Usage of the ATACseq_pipeline: 

python command.py config_file

## Component of config_file:

1. Procedures to be involved, starts with **##**, e.g. **_##alignment_**
2. Parameters for the corresponding procedure, starts with **--**,e.g. **_--batch 14_**

### A quick start
