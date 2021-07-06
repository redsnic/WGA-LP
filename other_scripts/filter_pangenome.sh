#! /bin/bash

# usage: 
# bash filter_pangenome.sh \
# path_to_extract_gene_ids_by_presence_absence_roary.R \ #1
# path_to_pangenome.fasta \ #2
# path_to_presence_absence.csv \ #3
# min_genomes_with_genes max_genomes_with_genes \ #4-5
# output_dir #6

cat $2 | sed 's/>[^\s]*\s/>/g' > pan_genome_reference_no_strange_ids.fa;
Rscript $1 --args $3 $4 $5 > output.list
wgalp filter-assembly --contigs pan_genome_reference_no_strange_ids.fa --selected-contigs output.list --output $6 
rm pan_genome_reference_no_strange_ids.fa
rm output.list