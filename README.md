# WGA-LP

This project specifies a tool to build pipelines concatenating bash and python code. 
Included in this repo is the implementation of a pipeline for Whole Genome Assembly, 
made specifically for Lactobacilli, that operates on raw `.fastq` files to produce
the annotated contigs of the assembled genomes.  

## Pre-requirements

> WGA-LP requires a system that can run `bash` scripts. To run the analysis on 
  the Lactobacilli data, at least 10GB of available RAM are required.

This pipeline relies on many external tools that must be installed in order to run the analysis:

* **bamtools**: manage `.bam` files
* **bazam**: convert `.bam` files back to `.fastq` 
* **bracken**: postprocess kraken2 reports to find contamination
* **BWA**: align `.fastq` files to a reference genome
* **FastQC**: evaluate `.fastq` quality
* **kraken2**: evaluate possible contaminations of the sequenced sample (minikraken db is required)
* **mauve**: program for multiple alignment, used to reorder contigs
* **minia**: a simple assembler for bacterial genomes
* **prokka**: annotate assembled genomes from bacteria 
* **samtools**: manage `.sam` and `.bam` files
* **SPAdes**: a more complex assembler for bacterial genomes
* **TrimmomaticPE**: tool to clean `.fastq` reads

## Coping with java tools

Mauve and Bazam tools are implemented in `java` and are available in the form of `.jar` files. To let the pipeline
know their location it is required that they are added to the execution path: 

### Manual approach

```
# skip these commands if you already have a valid folder in the path that you want to use
# create a bin folder in the home directory and add it to the path
mkdir $HOME/bin
export PATH=$PATH:$HOME/bin
# if you want to add that folder also to .bashrc run also
echo "export PATH=$PATH:$HOME/bin" >> $HOME/.bashrc
```

Then add bash script to run the .jar files to that folder 

```
folder=$HOME/bin # or another folder in your path
sudo echo "java -jar /your/path/to/bazam.jar \$@" > $folder/bazam && sudo chmod 775 $folder/bazam
sudo echo "java -Xmx500m -cp /your/path/to/Mauve.jar org.gel.mauve.contigs.ContigOrderer \$@" > $folder/mauveContigOrderer && sudo chmod 775 $folder/mauveContigOrderer
```

### Assisted approach

to simplify this process, you can use the `configure.sh` script in this way:

```
bash configure.sh /path/to/newPathFolder /path/to/bazam.jar /path/to/Mauve.jar
```

## Installation

To install the package run the following commands 

```
# clone this Git repository:
git clone https://github.com/redsnic/WGA-LP.git
# move in the WGA-LP folder:
cd WGA-LP
# install the package using pip (if you don't have pip use pip3)
pip install . 
```

see the last section to see how to actually launch the execution.

## Re-running the pipeline

WGA-LP pipeline is organized to keep track of the analysis in order to avoid running successful steps multiple times.
The execution is divided in sub-workflows that are composed of multiple steps. To rerun a specific step it is necessary 
to delete its folder from the output directory (of a specific sample) and to delete the `.checkpoint` file associated
to the current sub-workflow. 

For example to re run trimming, delete `TrimmomaticPE` folder and `fastq_trimming.checkpoint` file inside the output 
directory of the choosen sample.

## Managing the auxiliary data

To run the pipeline, it is required to provide `.tsv` tables like te ones in the `aux_data` folder. 

`samples_metadata` associates Folder (an identifier for the sample, the name of the folder in wich the raw reads are) and Organism (the name of the organism as
reported by kraken2). 

`reference_location` associates a Reference (that must mach the identifiers in the Organism column of `samples_metadata`) to its Location (a path to the `.fasta` file
of the reference). 

> look at the examples and modify the `.tsv` files accordingly to match the location of the files on your machine

## Launching the execution 

to run the pipeline, execute `complete_workflow.py` with `python3`: 

```
python3 workflows/complete_workflow.py \ 
    --output /path/to/existing/output/directory \
    --ref-table /path/to/samples_metadata.tsv \
    --ref-location-table /path/to/aux_data/references_location.tsv \
    --input /path/to/first/folder/with/raw_fastq_files/ /path/to/second/folder/with/raw_fastq_files/ \  # etc... 
    --kraken-db /path/to/minikraken_db/minikraken2_v1_8GB
```

explaination of the parameters:

* **output**: this will be the folder which will contain the results of the analysis on the **input** samples (must be already created!)
* **ref-table**: path to `sample_metadata` tsv file (can have any name, must have Folder and Organism columns)
* **ref-location-table**: path to `reference_location` tsv file (can have any name, must have Reference and Location columns)
* **input**: a list of paths to the input folders. A valid input folders contains only the two forward and reverse raw `.fastq` files (that must contain `_R1_` and `_R2_` in their name respectively)
* **kraken-db**: location of the minikraken db  

