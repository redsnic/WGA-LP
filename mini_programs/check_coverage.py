#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from sub_workflows.compute_coverage import ComputeCoverage

# --- input arguments

def prepare_input(args):
    input_data = InputManager("Program to extract coverage statistics from a Whole Genome Assembly")
    input_data.add_arg("--fastq-fwd", "path", description="[Required] raw forward reads (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="[Required] raw reverse reads (.fastq)") 
    input_data.add_arg("--contigs", "path", description="[Required] assembled contigs (.fasta)") 
    input_data.add_arg("--output", "dir", description="[Required] output folder")
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(output_dir, fastq_fwd, fastq_rev, contigs):
    check_files([fastq_fwd, fastq_rev, contigs])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core function

def run_coverage_computation(output_dir, fastq_fwd, fastq_rev, contigs):
    # sanity check
    sanity_check(output_dir, fastq_fwd, fastq_rev, contigs)
    args_dict = {
        "fastq_fwd" : fastq_fwd, 
        "fastq_rev" : fastq_rev, 
        "contigs" : contigs
    }
    step = ComputeCoverage("compute_coverage", output_dir)
    out = step.run(args_dict)
    step.delete_checkpoint()

    return out

# --- caller function

def check_coverage(args):

    in_manager = prepare_input(args)

    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    contigs = in_manager["--contigs"]["value"]
    output_dir = in_manager["--output"]["value"] 

    output = run_coverage_computation(output_dir, fastq_fwd, fastq_rev, contigs)

    print("task completed successfully")
    print("the file with the read depth for each base of the assembled genome is available at this location:")
    print("\t" + "depth_file" + " : " + output["depth_file"])
    print("\t" + "depth_summary" + " : " + output["depth_summary"])

    return output
     
if __name__ == "__main__":
    check_coverage(sys.argv[1:])
    
    

    

    