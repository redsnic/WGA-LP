# WGA-LP

WGA-LP is a pipeline for whole genome assembly that 
simplifies the usage of different tools and helps the 
user in evaluating his results.

This pipeline also includes tools to expand the analysis
by including interfaces to other software.

WGA-LP was built to operate directly from raw `.fastq` files 
and was originally used to analyze the genome 
of a set Lactobacilli (hence the L in the acronym)

## Installation

The best way to install WGA-LP is through [docker](https://www.docker.com/).
The **wgalp image** is available [here](https://hub.docker.com/repository/docker/redsnic/wgalp) and includes all the 
software and databases required for the analysis. 

The image is intended to be used with `docker exec` and
provides a bash shell ready for use. Further information 
is available on the docker hub page of wgalp. 

## Pipeline external tools

This pipeline relies on many external tools that provide some of the core functionalities of WGA-LP:

* **bamtools**: manage `.bam` files
* **bazam**: convert `.bam` files back to `.fastq` 
* **bracken**: postprocess kraken2 reports to find contamination
* **BWA**: align `.fastq` files to a reference genome
* **FastQC**: evaluate `.fastq` quality
* **kraken2**: evaluate possible contaminations of the sequenced sample (minikraken db is required)
* **mauve**: program for multiple alignment, used to reorder contigs
* **minia**: a simple assembler for bacterial genomes
* **prokka**: annotate assembled genomes from bacteria 
* **samtools** and **plot-bamstats**: manage `.sam` and `.bam` files, create reports
* **SPAdes**: a more complex assembler for bacterial genomes
* **TrimmomaticPE**: tool to clean `.fastq` reads
* **checkM**, **merqury** and **quast**: tools to evaluate WGA quality

All these tools are freely available for installation. 

## Re-running the pipeline

WGA-LP pipeline is organized to keep track of the analysis in order to avoid running successful steps multiple times.
The execution is divided in sub-programs that are composed of multiple steps. To rerun a specific step it is necessary 
to delete its folder from the output directory (of a specific sample). 

For example to re run trimming, delete `TrimmomaticPE` folder file inside the output directory of the choosen sample.

## Launching the execution 

to run the pipeline, execute `wgalp` with `python3`.
This will show a list of all the possible tools available 
for the analysis. Executing `wgalp <program_name>` will 
provide further information on the specific sub program and
its usage.

For reference, this is the help message of wgalp:

```
This programs is an helper to run the sub procedures of wgalp
usage: wgalp <program> [args]

the following is a list of all the available programs:
        trim : trim reads and/or assess contaminations with kraken2
        decontaminate : remove reads mapping to a contaminant non ambiguosly
        assemble : assemble reads into scaffolds or contigs
        check-coverage : compute coverage statistics of an assembled genome
        view-nodes : compute coverage plots for specific nodes of a whole genome assembly       reorder : reorder a whole genome assembly using a reference genome
        filter-assembly : select contigs by ID
                          (to be used with the webapp: https://redsnic.shinyapps.io/ContigCoverageVisualizer/)
        annotate : run prokka annotation with NCBI standard
        plasmid : extract putative plasmids using recycler
        quality : evaluate assembly quality using checkM, merqury and quast
        understand-origin : runs kraken2 in selection mode
        kdb-load : pre-load kraken2 database in RAM, so that you dont have to load it multiple times (use --memory-mapped option when possible)
        kdb-unload : remove loaded kraken2 db from RAM
        filter-fastq : select reads from a fastq file
        help : show this message (equivalent to --help or -h)

Run wgalp <program> --help for specific information about the selected program.
```

## Manual installation

If you, for some reason, want to install all the dependencies for WGA-LP 
manually, avoiding docker, please refer to the commands 
in the Dockerfile, as those are the instructions to install 
WGA-LP on Ubuntu 18.04 LTS. WGA-LP can only be installed on
**Linux** machines and with the **bash shell** available.

### Updating and installing WGA-LP 

To install the python package associated to the pipeline, run the following commands:

```
# clone this Git repository:
git clone https://github.com/redsnic/WGA-LP.git
# move in the WGA-LP folder:
cd WGA-LP
# install the package using pip3
pip3 install . 
```

to just upgrade to the last version do (in WGA-LP's directory):

```
git pull; pip3 instal .;
```