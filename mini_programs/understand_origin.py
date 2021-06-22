#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from sub_workflows.fastq_trimming import TrimFastq
from WGALP.blocks.kraken import kraken
from WGALP.blocks.bracken import bracken

# --- input arguments 

def prepare_input(args):
    input_data = InputManager("Run quality evaluation of raw reads, prepare trimmed reads and assess contaminations")
    input_data.add_arg("--fastq-fwd", "path", description="raw forward reads (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="raw reverse reads (.fastq)")
    input_data.add_arg("--fasta", "path", description="altenatively, you can input a .fasta file")
    input_data.add_arg("--output", "dir", description="path to the output folder")
    input_data.add_arg("--kraken-db", "path", description="path to the (mini)kraken database")
    input_data.add_arg("--memory-mapped", "flag", description="add this flag if you don't want to load the (mini)kraken db in RAM (so, when using a ramdisk)")
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(fastq_fwd, fastq_rev, fasta, output_dir, kraken_db, memory_mapped):

    check_folders([kraken_db])
    if fasta is None and (fastq_fwd is None and fastq_rev is None):
        raise Exception("no input defined, use --fasta or --fastq-fwd/--fastq-rev arguments")
    if fasta is not None and (fastq_fwd is not None or fastq_rev is not None):
        raise Exception("cannot use --fasta and --fastq-fwd/--fastq-rev arguments together")
    if fasta is None:
        check_files([fastq_fwd, fastq_rev])
    else:
        check_files([fasta])

    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core function

def run_quality_evaluation(fastq_fwd, fastq_rev, fasta, output_dir, kraken_db, memory_mapped):
    # sanity check
    sanity_check(fastq_fwd, fastq_rev, fasta, output_dir, kraken_db, memory_mapped)

    kraken_out = kraken("kraken", output_dir, kraken_db, memory_mapped, fastq1=fastq_fwd, fastq2=fastq_rev, fasta=fasta)
    return kraken_out
     
# --- caller function

def understand_origin(args):
    in_manager = prepare_input(args)

    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    fasta = in_manager["--fasta"]["value"]
    output_dir = in_manager["--output"]["value"]
    kraken_db = in_manager["--kraken-db"]["value"]
    memory_mapped = in_manager["--memory-mapped"]["value"]
    
    output = run_quality_evaluation(fastq_fwd, fastq_rev, fasta, output_dir, kraken_db, memory_mapped)

    print("task completed successfully:")
    print("\tlog : " + output["kraken_log"])
    print("check " + output_dir + " for the full kraken output")
    print("you can use the following command to easly extract the nodes:")
    print("cat " + output["kraken_log"] + " | cut -d$'\t' -f 2,3 | grep <your_taxa>")
    print("you can use grep -v to extract the elements not matching to a taxa of your choice, for example:")
    print("cat " + output["kraken_log"] + " | cut -d$'\\t' -f 2,3 | grep -v casei")
    return output

if __name__ == "__main__":
    understand_origin(sys.argv[1:])