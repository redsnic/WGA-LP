import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from sub_workflows.fastq_trimming import TrimFastq
from WGALP.blocks.minia import minia
from WGALP.blocks.SPAdes import SPAdes

def prepare_input(args):
    input_data = InputManager("Wrapper to easily run Whole Genome Assemblers")
    input_data.add_arg("--fastq-fwd", "path", description="raw forward reads (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="raw reverse reads (.fastq)")
    input_data.add_arg("--output", "dir", description="path to the output folder")
    input_data.add_arg("--assembler", "text", description="assembler name (from this list) [SPAdes, minia, SPAdes_plasmid]")
    input_data.add_arg("--kmer", "text", description="kmer length (to be used only with minia)")
    input_data.parse(args)
    return input_data

def sanity_check(fastq_fwd, fastq_rev, output_dir, assembler, kmer):
    check_files([fastq_fwd, fastq_rev])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)
    if assembler not in ["SPAdes", "minia", "SPAdes_plasmid"]:
        raise Exception("--assembler option supports only SPAdes or minia")
    if assembler == "minia":
        if kmer == None:
            raise Exception("minia requires --kmer option")
    elif kmer != None:
        raise Exception("--kmer option can be set only with minia assembler")


def run_assembler(fastq_fwd, fastq_rev, output_dir, assembler, kmer):
    # sanity check
    sanity_check(fastq_fwd, fastq_rev, output_dir, assembler, kmer)
    
    if assembler == "SPAdes":
        out = SPAdes("SPAdes", output_dir, fastq_fwd, fastq_rev)
        return out
    elif assembler == "SPAdes_plasmid":
        out = SPAdes("SPAdes", output_dir, fastq_fwd, fastq_rev, plasmid=True)
        return out
    elif assembler=="minia":
        out = minia("minia_" + str(kmer), output_dir, kmer, fastq_fwd, fastq_rev=fastq_rev) 
        return out
    else:
        raise Exception("Invalid assembler")

     
if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    output_dir = in_manager["--output"]["value"]
    assembler = in_manager["--assembler"]["value"]
    try:
        kmer = int(in_manager["--kmer"]["value"])
    except Exception:
        kmer = None
    
    output = run_assembler(fastq_fwd, fastq_rev, output_dir, assembler, kmer)

    print("task completed successfully")
    print("assembled contigs/scaffolds are at the following locations:")
    if assembler == "SPAdes" or assembler == "SPAdes_plasmid":
        print("\t" + "contigs" + " : " + output["contigs"])
        print("\t" + "scaffolds" + " : " + output["scaffolds"])
    if assembler == "minia":
        print("\t" + "contigs" + " : " + output["contigs"])
    print("check " + output_dir + " for assembler specific files")
