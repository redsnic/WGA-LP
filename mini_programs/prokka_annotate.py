#!/usr/bin/env python3

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from WGALP.blocks.prokka import prokka

def prepare_input(args):
    input_data = InputManager("Wrapper to easily run prokka in NCBI compliant mode")
    input_data.add_arg("--contigs", "path", description="assembled contigs or scaffolds (.fasta)")
    input_data.add_arg("--output", "dir", description="path to the output folder") 
    input_data.parse(args)
    return input_data

def sanity_check(contigs, output_dir):
    check_files([contigs])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)


def run_annotation(contigs, output_dir):
    # sanity check
    sanity_check(contigs, output_dir)
    out = prokka("prokka", output_dir, contigs)
    return(out)
     
if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

    contigs = in_manager["--contigs"]["value"]
    output_dir = in_manager["--output"]["value"]
    
    output = run_annotation(contigs, output_dir)

    print("task completed successfully")
    print("the annotated assembly is at the following locations:")
    print("\t" + "FORMAT" + "\t" + "PATH")
    print("\t" + "ffn" + "\t" + output["ffn"])
    print("\t" + "faa" + "\t" + output["faa"])
    print("\t" + "gbk" + "\t" + output["gbk"])
    print("\t" + "gff" + "\t" + output["gff"])
    print("\t" + "tsv" + "\t" + output["tsv"])
    print("other formats are available in the output folder " + output_dir)
    