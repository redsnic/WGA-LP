#!/usr/bin/env python3

# remove contigs with coverage less than a thresold,
# this is a minimal script that works on SPAdes nodes only

# usage: python remove_spades_lowcoverage.py scaffolds.fasta 20.35 mode
# mode can be (remove nodes with) less or greater (coverage)

import sys

def remove_nodes_by_coverage(fasta, threshold, mode):

    f = open(fasta, "r") 
    out = ""

    write_down = False
    for line in f.readlines():
        if line.startswith(">"):
            node_info = line.split("_")
            #node_num = int(node_info[1])
            #node_len = int(node_info[3])
            node_cov = float(node_info[5])
            if mode == "less" and node_cov > threshold:
                write_down = True
                out += line 
            elif mode == "greater" and node_cov > threshold:
                write_down = True
                out += line 
            elif not mode in ["greater", "less"]:
                raise Exception("Invalid mode " + mode + " use less or greater")
            else:
                write_down = False
        elif write_down:
            out += line

    f.close()
    return out
     

if __name__ == "__main__":

    fasta = sys.argv[1]
    threshold = float(sys.argv[2])

    mode = "less"
    if len(sys.argv) == 4:
        if sys.argv[3] == "greater":
            mode = "greater"

    print(remove_nodes_by_coverage(fasta, threshold, mode))  
