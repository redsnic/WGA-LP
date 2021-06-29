#!/usr/bin/env python3

import sys

# this short script removes newlines in .fasta files,
# without breaking comments

# usage: python3 clean_space_in_fasta.py file.fasta

def clean_spaces(f):
    """
    remove newlines in lines non starting with >
    """
    out = ""
    for line in f:
        if line.startswith(">"):
            out += line
        else:
            out += line[:len(line)-1]

    return out

if __name__ == "__main__":
    f = open(sys.argv[1], "r")
    print(clean_spaces(f))
    f.close()
        