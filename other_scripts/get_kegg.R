# usage: Rscript get_kegg.R --args input.file > output.file
library(tidyverse)
args <- commandArgs(trailingOnly = TRUE)
read_tsv(args[2], comment = "##") %>% 
  select(KEGG_ko) %>%
  mutate(KEGG_ko = ifelse(KEGG_ko == "-", NA, KEGG_ko)) %>%
  pull(1) %>%
  na.omit() %>%
  map(~ strsplit(., ",")[[1]]) %>%
  unlist() %>%
  unique() %>% 
  map(~ strsplit(., ":")[[1]][2]) %>%
  paste(collapse = "\n") %>% 
  cat()