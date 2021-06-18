# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run merqury
"""
input_description = """
the original fastq files and an assembly
"""
output_description = """
quality reports are availle in the output folder
"""

### Wrapper
# a kmer size is fine for genomes of 3Mpb (use $MERQURY/best_k.sh <genome_size>) 
def merqury(name, rootpath, reference, fastq1, fastq2, kmer=16, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(merqury_runner)
    step_args = {
        "assembly": reference,
        "fastq1" : fastq1,
        "fastq2" : fastq2,
        "kmer" : kmer
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description) 
    return step

### Runner
def merqury_runner(step, args):
    """
    run merqury
    input:
    {
        "assembly" (.fasta)
        "fastq1" 
        "fastq2"  
    }
    :param args: a dictionary of the arguments
    """
    assembly = args["assembly"]
    f1 = args["fastq1"]
    f2 = args["fastq2"]
    k = str(args["kmer"])
    
    command = "mkdir " + os.path.join(step.outpath, "maryl") + " ; cd " + os.path.join(step.outpath, "maryl") + " && "
    command += "meryl k=" + k + " count output " + os.path.join(step.outpath, "FWD.maryl") + " " + f1 + " && "
    command += "meryl k=" + k + " count output " + os.path.join(step.outpath, "REV.maryl") + " " + f2 + " && "
    command += "meryl union-sum output " + os.path.join(step.outpath, "UNION.maryl") + " " + os.path.join(step.outpath, "FWD.maryl") + " " + os.path.join(step.outpath, "REV.maryl") + " && "  
    command += "$MERQURY/merqury.sh " + os.path.join(step.outpath, "UNION.maryl") + " " + assembly + " merqury;"

    if step.execution_mode != "read":
        run_sp(step, command)


    print(command)
    # organize output

    step.outputs = {
        "merqury_output_dir" : ""
    }

    return step