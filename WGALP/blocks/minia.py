# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run minia"
"""
input_description = """
a paired end pair of fastq files (or a single one)
"""
output_description = """
the assembler results
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
    {
        "kmer_size" size of the kmer for the assembler
        "fastq_fwd" (full path) (it seems that these must have different filenames ...)
        "fastq_rev" (full path) 
    }
    :param args: a dictionary of the arguments
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