library(tidyverse)

args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=4){
  print("USAGE: Rscript extract_gene_ids_by_presence_roary.R --args roary_presence_absence.csv min_genomes max_genomes")
}else{
  infile <- args[2]
  min_genomes <- strtoi(args[3])
  max_genomes <- strtoi(args[4])
  tab <- read_csv(args[2]) %>% filter(`No. isolates` >= min_genomes & `No. isolates` <= max_genomes) %>%
    pull(Gene) %>%
    paste(collapse="\n") %>%
    cat
  cat("\n")
}

