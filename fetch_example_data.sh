# This script is meant to run with a docker installation
# usage: bash fetch_example_data.sh

# --- download data folder ---
cd /root
pip install gdown
gdown https://drive.google.com/uc?id=1hg-Eacm6J70X42BCKKqdDsZhYnHOGxR4
mkdir example_data

# --- unzip ---
tar xvf WGA-LP_Data.tar.gz -C example_data/
rm WGA-LP_Data.tar.gz

for f in `find example_data/ -path "*.gz"`; do gunzip $f ; done
# --- prepare bwa indexes ---
for f in `find example_data/ -path "*.fasta"`; do bwa index $f ; done

# --- prepare fastq directories ---
mkdir /root/shared/144
mkdir /root/shared/144_working_directory
# --- prepare references' directories ---
mkdir /root/shared/references
mkdir /root/shared/references/rhamnosus
mkdir /root/shared/references/pediococcus
# --- prepare references for the simulations ---
mkdir /root/shared/simulation_references
# --- move data ---
mv /root/example_data/144_raw_reads/* /root/shared/144/
mv /root/example_data/LRhamnosus_example_references/* /root/shared/references/rhamnosus/
mv /root/example_data/PAcidilactici_example_references/* /root/shared/references/pediococcus/
mv /root/example_data/simulation_references/* /root/shared/simulation_references/

# --- finish cleanup ---
rm -rf /root/example_data


