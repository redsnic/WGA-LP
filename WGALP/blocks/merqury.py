# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run merqury to asses WGA quality
"""
input_description = """
the original fastq files and an assembly
"""
output_description = """
quality reports and plots that will be available in the output folder
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
    input:
        assembly : path (.fasta)
        fastq1 : path
        fastq2 : path
        kmer : number (kmer length used by the assembler)
    output:
        merqury_output_dir : just a link to the output folder 
    """
    assembly = os.path.abspath(args["assembly"])
    f1 = os.path.abspath(args["fastq1"])
    f2 = os.path.abspath(args["fastq2"])
    k = str(args["kmer"])
    
    # running merqury requires to run meryl
    command =  "cd " + step.outpath + " && "
    command += "meryl k=" + k + " count output FWD.maryl " + f1 + " && "
    command += "meryl k=" + k + " count output REV.maryl " + f2 + " && "
    command += "meryl union-sum output UNION.maryl FWD.maryl REV.maryl && "  
    command += "$MERQURY/merqury.sh UNION.maryl " + assembly + " " + os.path.splitext(os.path.basename(assembly))[0] + " ; "

    if step.execution_mode != "read":
        run_sp(step, command)


    print(command)
    # organize output

    step.outputs = {
        "merqury_output_dir" : ""
    }

    return step