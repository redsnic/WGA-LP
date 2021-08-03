#!/bin/Rscript
#
# program to construct a summary table from many kraken2 reports
#
# Usage: Rscript kraken_table.R --args file1 file2 ... > output.tsv
#

require(tidyverse)

arguments <- commandArgs(trailingOnly = TRUE)
files <- arguments[2:length(arguments)]

out <- NULL
for(f in files){
  tab <- read_tsv(f, col_names = c("precentage", "reads", "reads_at_level", "level", "ID", "name")) %>% 
    mutate(level = map_chr(level, ~strsplit(., "")[[1]][1])) %>% 
    select(name, ID, level, precentage) %>%
    mutate(sample = !!f)
  if(is.null(out)){
    out <- tab
  }else{
    out <- bind_rows(out, tab)
  }
}

out <- out %>% 
  pivot_wider(names_from = "sample", values_from="precentage")

format_tsv(out) %>% cat