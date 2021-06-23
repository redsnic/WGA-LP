#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from WGALP.blocks.fastq_bam_difference import filter_fastq_reads

# --- input arguments

def prepare_input(args):
    input_data = InputManager("Select only listed reads from a Whole Genom Assembly")
    input_data.add_arg("--fastq", "path", description="fastq reads to be filtered (.fastq)")
    input_data.add_arg("--selected-reads", "path", description="a file containing the ids of the selected reads (each id is in its own line)")
    input_data.add_arg("--complement", "flag", description="if set, selected reads are instead removed from the original fastq")
    input_data.add_arg("--output", "dir", description="path to the output folder") 
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(output_dir, fastq, selected_reads, complement):
    check_files([fastq, selected_reads])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core functions

def select_fastq_aux(output_dir, fastq, selected_reads, complement):
    # sanity check
    sanity_check(output_dir, fastq, selected_reads, complement)
    filter_fastq_reads(fastq, selected_reads, os.path.join(output_dir, "filtered.fastq"), keep=not complement)
     
# --- caller function

def select_fastq(args):
    in_manager = prepare_input(args)

    fastq = in_manager["--fastq"]["value"]
    selected_reads = in_manager["--selected-reads"]["value"]
    output_dir = in_manager["--output"]["value"]
    complement = in_manager["--complement"]["value"]
    
    select_fastq_aux(output_dir, fastq, selected_reads, complement)

    print("task completed successfully")
    print("The filtered .fastq is at the following location:")
    print("\t" + "filtered_fastq" + " : " + os.path.join(output_dir, "filtered.fastq"))
    return os.path.join(output_dir, "filtered.fastq")

if __name__ == "__main__":
    select_fastq(sys.argv[1:])
    
    


