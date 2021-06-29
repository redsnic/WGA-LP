# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run bwa mem
"""
input_description = """
A reference and the fastq(s) to be aligned to it (can operate with single and PE reads)
"""
output_description = """
A samfile of the alignment
"""

### Wrapper
def BWA(name, rootpath, reference, fastq1=None, fastq2=None, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(BWA_runner)
    step_args = {
        "reference": reference,
        "fastq1" : fastq1
    }
    if fastq2 != None:
        step_args["fastq2"] = fastq2
    step.run(step_args)
    step.set_description(description, input_description, output_description) 
    return step

### Runner
def BWA_runner(step, args):
    """
    input:
        fastq1 : path 
        (aux) fastq2 : path (only for PE alignment)
        reference : path
        (aux) n_threads : number of threads to be used (default, use all the available threads)
        (aux) output_filename : text
    output:
        samfile : a SAM file of the alignment
    """
    f1 = args["fastq1"]
    paired_end_mode = "fastq2" in args
    if paired_end_mode:
        f2 = args["fastq2"]

    ref = args["reference"]

    outfile = "aligned_to_" + os.path.splitext(os.path.basename(ref))[0] + ".sam"  
    if "output_filename" in args:
        outfile = args["output_filename"]

    n_threads = multiprocessing.cpu_count()
    if "n_threads" in args:
        n_threads = args["n_threads"]

    if paired_end_mode:
        command = "bwa mem -t " + str(n_threads) + " " + ref + " " + f1 + " " + f2 + " > " + os.path.join(step.outpath, outfile)    
    else:
        command = "bwa mem -t " + str(n_threads) + " " + ref + " " + f1 + " > " + os.path.join(step.outpath, outfile)


    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {
        "samfile" : outfile
    }

    return step