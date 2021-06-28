#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from WGALP.utils.genericUtils import binary_search

# --- input arguments

def prepare_input(args):
    input_data = InputManager("Select only listed contigs from a Whole Genom Assembly")
    input_data.add_arg("--contigs", "path", description="assembled contigs or scaffolds (.fasta)")
    input_data.add_arg("--selected-contigs", "path", description="a file containing the ids of the selected contigs (each id is in its own line)")
    input_data.add_arg("--complement", "flag", description="if set, keeps contigs not in list") 
    input_data.add_arg("--output", "dir", description="path to the output folder") 
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(output_dir, contigs, selected_contigs, complement):
    check_files([contigs, selected_contigs])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core functions

def filter_fasta( fasta_file_path, selected_contigs, out_file_name, keep=True):
    """
    Filter unwanted reads from a fasta files
    selected_contigs should point to a file with a newline separated list of contig IDs
    :param fasta_file_path: path to a fasta_file
    :param selected_contigs: path to the file with the IDs of the selected contigs 
    :param out_file_name: name of the .fasta file created after this filtering
    """

    # open input files
    fasta_file = open(fasta_file_path, "r")
    selected_contigs_file = open(selected_contigs, "r")

    # read selected_contigs and sort them
    selected_contigs = selected_contigs_file.read().split()
    selected_contigs.sort()

    out_file = open(out_file_name, "w")

    to_be_printed = False
    for line in fasta_file:
        if line.startswith(">"):
            # check if read ID is in the bad list
            contig_id = line.split()[0][1:].strip()
            
            if(binary_search(selected_contigs, contig_id) is not None):
                to_be_printed = keep
            else:
                to_be_printed = not keep
        if(to_be_printed):
            # if it is not, print the read
            out_file.write(line)

    fasta_file.close()
    selected_contigs_file.close()
    out_file.close()

    return out_file_name

def select_contigs_aux(output_dir, contigs, selected_contigs, complement):
    # sanity check
    sanity_check(output_dir, contigs, selected_contigs, complement)
    out = filter_fasta(contigs, selected_contigs, os.path.join(output_dir, "filtered_contigs.fasta"), keep=not complement)
    return out
     
# --- caller function

def select_contigs(args):
    in_manager = prepare_input(args)

    contigs = in_manager["--contigs"]["value"]
    selected_contigs = in_manager["--selected-contigs"]["value"]
    output_dir = in_manager["--output"]["value"]
    complement = in_manager["--complement"]["value"]
    
    output = select_contigs_aux(output_dir, contigs, selected_contigs, complement)

    print("task completed successfully")
    print("filtered .fasta is at the followinf location:")
    print("\t" + "filtered_fasta" + " : " + output)
    return output

if __name__ == "__main__":
    select_contigs(sys.argv[1:])
    
    







    
