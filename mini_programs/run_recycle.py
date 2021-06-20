#!/usr/bin/env python3

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from sub_workflows.extract_plasmids import Recycler

def prepare_input(args):
    input_data = InputManager("Wrapper to easily run recycler and inferr plasmid from genome assembly graphs")
    input_data.add_arg("--fastq-fwd", "path", description="raw forward reads (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="raw reverse reads (.fastq)") 
    input_data.add_arg("--contigs", "path", description="assembled contigs (.fasta)") 
    input_data.add_arg("--assembly-graph", "path", description="assembly graph (.fastg)")
    input_data.add_arg("--kmer", "text", description="maximum kmer length used by the assembler (127 for spades)")
    input_data.add_arg("--output", "dir", description="output folder")
    input_data.parse(args)
    return input_data

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
     
if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

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

    

    