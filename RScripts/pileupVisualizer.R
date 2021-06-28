#!/usr/bin/env Rscript

# this script contains some utils to view the result of a `samtools depth` output.
library(tidyverse)
args <- commandArgs(trailingOnly=TRUE)
# Rscript pileupVisualizer.R --args draw ~/WGA_batteri/143_our/depth/samtools_depth/aligned_to_143_dec_clean.depth output NODE_5_length_281865_cov_44.033765
# 1 --args, 2 mode, 3 filepath (pointing a .depth file), 4 output path
print(args)
mode <- args[2]
file_path <- args[3]
output_path <- args[4]

print("loading data ...")
depth.file <- read_tsv(file_path, col_names = FALSE)

plot_and_save <- function(depth.file, node){
    print(paste("preparing graph for", node, "..."))
    df. <- depth.file %>% filter(X1 == !!node)
    p <- ggplot(df.) +
        geom_line(aes(x=X2, y=X3)) +
        geom_hline(yintercept = mean(df.$X3), color="red", linetype="dashed") +
        geom_hline(yintercept = median(df.$X3), color="red", linetype="dotted") +
        labs(title = paste("Coverage vs position for", node), x="position", y="coverage") +
        scale_y_log10()
    ggsave(paste(output_path, "/", "coverage_", node, ".png", sep=""), device="png", plot=p)
}

if(mode == "view"){ # draw coverage plot of a specific node
    node_names <- args[5:length(args)]
    for(node in node_names){
        plot_and_save(depth.file, node)
    }
}else if(mode == "view-all"){
    node_names <- depth.file %>% pull(X1) %>% unique()
    for(node in node_names){
        plot_and_save(depth.file, node)
    }
}


