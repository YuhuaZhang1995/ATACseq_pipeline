 # ATACseq_pipeline

This is an automatic pipeline of processing ATAC-seq data, which includes adapter-trimming, alignment, filtering and ploting.

## Usage of the ATACseq_pipeline: 

python command.py <config_file>

## Component of config_file:

1. Procedures to be involved, starts with **##**, e.g. **_##alignment_**
2. Parameters for the corresponding procedure, starts with **--**,e.g. **_--batch 14_**

### A quick start
In this case, the program will go through the whole procedure, and generate the intermediate files at each step and final results stored. The user need to specify **at least** the required parameters.

#### Required parameter

`##adapter_trimming`: Specify the procedure

`##alignment**`: Specify the procedure

`##filtering`: Specify the procedure

`--seq_data`: Pathway to the sequence data, end with Run_XXX, no '/' included at the end; the program will search for '/elder' folder and find the sequence data, **_e.g. --seq_data /pathway/to/data/Run_XXX_**

`--core_info_file`: The core information files, **_e.g. /pathway/to/file/Batch14_Run_1789_elder.txt_**;

`--batch`: The batch number, e.g. **_--batch 14_**;

`--run`: The run number, e.g. **_--run 1789_**;

#### Optional parameter

`--entire_output`: Where you would like to store the output(intermediate files and final results). The default is the current direrctory; 

`--job_AT`: Number of process for adapter trimming step, the default is 5;

`--job_align`: Number of process for alignment, the default is 3. Please pay attention to the **memory**, as the demand for the memory is considerably high;

`--job_filter`: Number of process for filtering, the default is 5;

`--intermediate_file`: Whether to keep the intermediate .bam files generated in the filtering step, the default is no. e.g. **_--intermediate_file Yes_**

#### A brief example of config_file

--entire_output .
--batch 14
--run 1789

##adapter_trimming
--job_AT 5
--seq_data /pathway/to/seq/data
--core_info_file /core/info/file.txt

##alignment
--job_align 5

##filtering
--job_filter 5
--intermediate_file Yes

### Separate each step
If the user prefer to run each procedure step by step and specify the output pathway for the intermediate files, just make the config_file contains only one operation each time.

#### Adapter_trimming

`--core_info_file`: The core information files, **_e.g. /pathway/to/file/Batch14_Run_1789_elder.txt_**;

`--seq_data`: Pathway to the sequence data, end with Run_XXX, no '/' included at the end; the program will search for '/elder' folder and find the sequence data, **_e.g. --seq_data /pathway/to/data/Run_XXX_**

`--job_AT`: Optional parameter. Number of process for adapter trimming step, the default is 5;

**Example**

##adapter_trimming
--core_info_file /core/info.txt
--job_AT 5
--seq_data /pathway/to/seq/data

#### Alignment

`--trimmed_file`: Pathway to the trimmed files, end with Run_XXX, no '/' included at the end; the program will search for '/elder' folder and find the sequence data;

`--out_conf`: Directory to store config and index files that would be used by gotcloud;

`--out_bam`: Directory to store the output bam files;

`--batch`: The batch number, e.g. **_--batch 14_**;

`--run`: The run number, e.g. **_--run 1789_**;

`--job_align`: Optional parameter. Number of process for alignment, the default is 3. Please pay attention to the **memory**, as the demand for the memory is considerably high;

**Example**

##alignment
--job_align 5
--trimmed_file /pathway/to/adapter/trimmed/file
--out_conf /directory/to/store/config/index/files/for/gotcloud
--out_bam /output/directory/to/store/generated/bam/file
--batch 14
--run 1789

#### Filtering

`--in_bam`: List of bam files. e.g. **_--in_bam /pathway/metagotCloudbamfiles_Batch14_Run1789_**;

`--out_proc_bam`: Output dir for processed .bam files;

`--job_filter`: Optional parameter. Number of process for filtering, the default is 5;

`--intermediate_file`: Optional parameter. Whether to keep the intermediate .bam files generated in the filtering step, the default is no. e.g. **_--intermediate_file Yes_**

**Example**

##filtering
--job_filter 5
--out_proc_bam /pathway
--in_bam /pathway/metagotCloudbamfiles_Batch14_Run1789
--intermediate_file Yes


