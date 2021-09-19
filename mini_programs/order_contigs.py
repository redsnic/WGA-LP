#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from WGALP.blocks.mauve import mauve_contig_sorting

# --- input arguments

def prepare_input(args):
    input_data = InputManager("Reorder contigs using mauve and a reference genome")
    input_data.add_arg("--contigs", "path", description="[Required] assembled contigs or scaffolds (.fasta)")
    input_data.add_arg("--reference", "path", description="[Required] a reference for the genome (.fasta)")
    input_data.add_arg("--output", "dir", description="[Required] path to the output folder") 
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(output_dir, reference, contigs):
    check_files([contigs, reference])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core functions

def reorder_contigs(output_dir, reference, contigs):
    # sanity check
    sanity_check(output_dir, reference, contigs)
    out = mauve_contig_sorting("mauve_reorder", output_dir, reference, contigs)
    return(out)

# --- caller function

def order_contigs(args):
    in_manager = prepare_input(args)

    contigs = in_manager["--contigs"]["value"]
    reference = in_manager["--reference"]["value"]
    output_dir = in_manager["--output"]["value"]
    
    output = reorder_contigs(output_dir, reference, contigs)

    print("task completed successfully")
    print("the reordered assembly is at the following location:")
    print("\t" + "contigs" + " : " + output["contigs"])
    print("other formats are available in the output folder " + output_dir)

    return output

if __name__ == "__main__":
    order_contigs(sys.argv[1:])
    
    