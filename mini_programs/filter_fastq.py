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
    input_data = InputManager("Select reads from a fastq file by ID")
    input_data.add_arg("--fastq", "path", description="fastq reads to be filtered (.fastq)")
    input_data.add_arg("--fastq-fwd", "path", description="fastq reads to be filtered FWD (Paired end mode) (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="fastq reads to be filtered REV (Paired end mode) (.fastq)")
    input_data.add_arg("--selected-reads", "path", description="a file containing the ids of the selected reads (each id is in its own line)")
    input_data.add_arg("--complement", "flag", description="if set, selected reads are instead removed from the original fastq")
    input_data.add_arg("--output", "dir", description="path to the output folder") 
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(output_dir, fastq, fastq_fwd, fastq_rev, selected_reads, complement):
    if fastq is not None and (fastq_fwd is not None and fastq_rev is not None):
        raise Exception("Choose either PE [--fastq-rev and --fastq-fwd] or non PE [--fastq] mode, use --help for more information")

    if fastq is None and not (fastq_fwd is not None and fastq_rev is not None):
        raise Exception("For PE mode both fwd and rev fastq files must be specified, use --help for more information")

    # files/dirs check 
    check_files([selected_reads])
    if fastq is None:
        check_files([fastq_fwd, fastq_rev])
    else:
        check_files([fastq])

    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core functions

def select_fastq_aux(output_dir, fastq, fastq_fwd, fastq_rev, selected_reads, complement):
    # sanity check
    sanity_check(output_dir, fastq, fastq_fwd, fastq_rev, selected_reads, complement)
    if fastq is None:
        filter_fastq_reads(fastq_fwd, selected_reads, os.path.join(output_dir, "filtered_fwd.fastq"), keep=not complement)
        filter_fastq_reads(fastq_rev, selected_reads, os.path.join(output_dir, "filtered_rev.fastq"), keep=not complement)
    else:
        filter_fastq_reads(fastq, selected_reads, os.path.join(output_dir, "filtered.fastq"), keep=not complement)
    
     
# --- caller function

def select_fastq(args):
    in_manager = prepare_input(args)

    fastq = in_manager["--fastq"]["value"]
    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    selected_reads = in_manager["--selected-reads"]["value"]
    output_dir = in_manager["--output"]["value"]
    complement = in_manager["--complement"]["value"]
    
    select_fastq_aux(output_dir, fastq, fastq_fwd, fastq_rev, selected_reads, complement)

    print("task completed successfully")
    print("The filtered .fastq is at the following location:")
    if not fastq is None:
        print("\t" + "filtered_fastq" + " : " + os.path.join(output_dir, "filtered.fastq"))
        return {"filtered_fastq" : os.path.join(output_dir, "filtered.fastq")}
    else:
        print("\t" + "filtered_fastq_fwd" + " : " + os.path.join(output_dir, "filtered_fwd.fastq"))
        print("\t" + "filtered_fastq_rev" + " : " + os.path.join(output_dir, "filtered_rev.fastq"))
        return {"filtered_fastq_fwd" : os.path.join(output_dir, "filtered_fwd.fastq"), "filtered_fastq_rev" : os.path.join(output_dir, "filtered_rev.fastq")}

if __name__ == "__main__":
    select_fastq(sys.argv[1:])
    
    


