# compute summary of Eggnog's "letter" categories
# usage: Rscript eggnog_letterfreq.R --args <inputpath> <outputpath> 

library(tidyverse)

#' Compute frequencies of letter classes from Eggnog annotation
#'
#' @param df An imported Eggnogg csv with columns COG_category and #query
#'
#' @return a dataframe with the frequency of each "letter" class
compute.eggnog.letter.frequency <- function(df){
    # - split letter categories in vectors 
    df <- df %>% mutate(COG_catlis = map(COG_category, ~ strsplit(.,"")[[1]]))
    # - get the list of possible letter categories
    descriptors <- df %>% pull(COG_catlis) %>% unlist %>% unique
    # - prepare the columns associated to the specific letter categories
    out <- list()
    out[["name"]] <- df$`#query`
    for (d in descriptors) {
        out[[paste(".", d, sep="")]] <- map_lgl(df$COG_catlis, ~ d %in% .)
    }
    # - extract counts of when the categories are set at TRUE
    out.df <- as.data.frame(out)
    out.df <- out.df %>%
        pivot_longer(starts_with("."), names_to = "descriptor", values_to = "value") %>% 
        filter(value == TRUE) %>% group_by(descriptor) %>%
        count() %>% 
        mutate(descriptor = strsplit(descriptor, "")[[1]][2])
    out.df
}

## --- MAIN

args <- commandArgs(trailingOnly=TRUE)
if(length(args) != 3){
    print("compute summary of Eggnog's \"letter\" categories")
    print("USAGE:")
    print("Rscript eggnog_letterfreq.R --args <inputpath> <outputpath>")
}else{
    # --- read input args
    # args[1] is --args
    input.path <- args[2]
    output.path <- args[3]
    print("loading_data ...")
    df <- read_tsv(input.path, comment = "##")
    print("computing ...")
    write_tsv(compute.eggnog.letter.frequency(df), output.path)
    print("DONE!")
}


