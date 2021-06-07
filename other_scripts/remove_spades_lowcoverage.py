# remove contigs with coverage less than a thresold

# usage: python remove_spades_lowcoverage.py scaffolds.fasta 20.35 

import sys

def remove_low_coverage_nodes(fasta, threshold):

    f = open(fasta, "r")
    out = ""

    write_down = False
    for line in f.readlines():
        if line.startswith(">"):
            node_info = line.split("_")
            #node_num = int(node_info[1])
            #node_len = int(node_info[3])
            node_cov = float(node_info[5])
            if node_cov > threshold:
                write_down = True
                out += line 
            else:
                write_down = False
        elif write_down:
            out += line
    return out
     

if __name__ == "__main__":

    fasta = sys.argv[1]
    threshold = float(sys.argv[2])

    print(remove_low_coverage_nodes(fasta, threshold))  
