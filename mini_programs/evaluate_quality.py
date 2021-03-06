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
    input_data.add_arg("--fastq-fwd", "path", description="[Required] raw forward reads (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="[Required] raw reverse reads (.fastq)")
    input_data.add_arg("--output", "dir", description="[Required] path to the output folder")
    input_data.add_arg("--kraken-db", "path", description="[Required] path to the (mini)kraken database")
    input_data.add_arg("--memory-mapped", "flag", description="add this flag if you don't want to load the (mini)kraken db in RAM (so, when using a ramdisk)")
    input_data.add_arg("--just-kraken", "flag", description="add this flag if you just want to run kraken/bracken (if you have, decontamined reads for example)")
    input_data.add_arg("--trimmomatic-args", "text", description="override default trimmomatic settings, write this field as a single string\n\t\tcare that this code will be interpreted direcly by the bash shell, adding ;, |, &&, etc.. may break the execution\n\t\tby default we use: SLIDINGWINDOW:5:20 ILLUMINACLIP:TruSeq2-PE.fa:2:30:10")
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(fastq_fwd, fastq_rev, output_dir):
    check_files([fastq_fwd, fastq_rev])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core function

def run_quality_evaluation(fastq_fwd, fastq_rev, output_dir, kraken_db, memory_mapped, just_kraken, trimmomatic_args):
    # sanity check
    sanity_check(fastq_fwd, fastq_rev, output_dir)
    
    if not just_kraken:
        args = {
            "fastq_fwd" : fastq_fwd,
            "fastq_rev" : fastq_rev,
            "trimmomatic_args" : trimmomatic_args
        }
        trimming = TrimFastq("fastq_trimming", output_dir)
        trimmed_reads = trimming.run(args)
        trimming.delete_checkpoint()

        kraken_out = kraken("kraken", output_dir, kraken_db, memory_mapped, fastq1=trimmed_reads["trimmed_fwd"], fastq2=trimmed_reads["trimmed_rev"])
        bracken("bracken", output_dir, kraken_out["kraken_report"], kraken_db) 
        return trimmed_reads
    else:
        kraken_out = kraken("kraken_direct", output_dir, kraken_db, memory_mapped, fastq1=fastq_fwd, fastq2=fastq_rev)
        bracken("bracken_direct", output_dir, kraken_out["kraken_report"], kraken_db) 
        return {}
     
# --- caller function

def evaluate_quality(args):
    in_manager = prepare_input(args)

    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    output_dir = in_manager["--output"]["value"]
    kraken_db = in_manager["--kraken-db"]["value"]
    memory_mapped = in_manager["--memory-mapped"]["value"]
    just_kraken = in_manager["--just-kraken"]["value"]
    trimmomatic_args = in_manager["--trimmomatic-args"]["value"]
    
    output = run_quality_evaluation(fastq_fwd, fastq_rev, output_dir, kraken_db, memory_mapped, just_kraken, trimmomatic_args)

    print("task completed successfully")
    if not just_kraken:
        print("trimmed reads are at the following locations:")
        print("\t" + "trimmed_fwd" + " : " + output["trimmed_fwd"])
        print("\t" + "trimmed_rev" + " : " + output["trimmed_rev"])
    print("check " + output_dir + " for kraken and bracken outputs")

    return output

if __name__ == "__main__":
    evaluate_quality(sys.argv[1:])