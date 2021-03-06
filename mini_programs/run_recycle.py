#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from sub_workflows.extract_plasmids import Recycler

# --- input arguments

def prepare_input(args):
    input_data = InputManager("Wrapper to easily run recycler and inferr plasmids from genome assembly graphs")
    input_data.add_arg("--fastq-fwd", "path", description="[Required] raw forward reads (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="[Required] raw reverse reads (.fastq)") 
    input_data.add_arg("--contigs", "path", description="[Required] assembled contigs (.fasta)") 
    input_data.add_arg("--assembly-graph", "path", description="[Required] assembly graph (.fastg)")
    input_data.add_arg("--kmer", "text", description="[Required] maximum kmer length used by the assembler (127 for spades)")
    input_data.add_arg("--output", "dir", description="[Required] output folder")
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(output_dir, fastq_fwd, fastq_rev, contigs, assembly_graph, kmer_length):
    check_files([fastq_fwd, fastq_rev, contigs, assembly_graph])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)
    try:
        kmer_length = int(kmer_length)
        if not isinstance(kmer_length, int):
            raise Exception("--kmer must be followed by an integer")
    except Exception:
        print("Error in --kmer argument, use --help for more information:")
        raise
    

# --- core functions

def run_plasmid_extraction(output_dir, fastq_fwd, fastq_rev, contigs, assembly_graph, kmer_length=127):
    # sanity check
    sanity_check(output_dir, fastq_fwd, fastq_rev, contigs, assembly_graph, kmer_length)
    kmer_length = int(kmer_length)
    args_dict = {
        "fastq_fwd" : fastq_fwd, 
        "fastq_rev" : fastq_rev, 
        "contigs" : contigs,
        "assembly_graph" : assembly_graph,
        "kmer_length" : kmer_length
    }
    step = Recycler("recycler", output_dir)
    out = step.run(args_dict)
    step.delete_checkpoint()
    return(out)
     
# --- caller function

def run_recycle(args):
    in_manager = prepare_input(args)

    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    contigs = in_manager["--contigs"]["value"]
    assembly_graph = in_manager["--assembly-graph"]["value"]
    kmer_length = in_manager["--kmer"]["value"]
    output_dir = in_manager["--output"]["value"] 

    output = run_plasmid_extraction(output_dir, fastq_fwd, fastq_rev, contigs, assembly_graph, kmer_length)

    print("task completed successfully")
    print("the fasta file with the inferred plasmids is at the following location:")
    print("\t" + "plasmid_fasta" + " : " + output["plasmid_fasta"])
    return output

if __name__ == "__main__":
    run_recycle(sys.argv[1:])
    

    

    