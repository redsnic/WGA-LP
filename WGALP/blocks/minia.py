# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run minia whole genome assembler
"""
input_description = """
one or two fastq files, dependently of the choosen mode (single or PE), and the length of the kmer to be used
"""
output_description = """
the assembled genome
"""

### Wrapper
def minia(name, rootpath, kmer_size, fastq_fwd, fastq_rev=None, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(minia_runner)
    step_args = {
        "kmer_size" : kmer_size,
        "fastq_fwd" : fastq_fwd,
        "fastq_rev" : fastq_rev
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

# Example bash command
#
# spades.py -1 $f1.trimmed.fastq -2 $f2.trimmed.fastq -o spades_out_$directory/ --careful 
def minia_runner(step, args):
    """
    run sades on a pair of .fastq files
    input:
        kmer_size : number (the size of the kmer to be used by the assembler)
        fastq_fwd : path 
        fastq_rev : path (check if these must have different filenames ...)  
    output:
        contigs : the WGA assembly created by minia
    """
    f1 = args["fastq_fwd"]
    f2 = args["fastq_rev"]

    command = ""

    if(f2 != None):
        command += "cat " + f1 + " " + f2 + " > " + os.path.join(step.outpath, "concat.fastq") + " ; "
        f1 = os.path.join(step.outpath, "concat.fastq")

    command += "minia -in " + f1 + " -out " + os.path.join(step.outpath, "out") + " -kmer-size " + str(args["kmer_size"]) +  " ; "

    if(f2 != None):
        command += "rm " + os.path.join(step.outpath, "concat.fastq") + " ; "

    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {
        "contigs" : "out.contigs.fa"
    }

    return step