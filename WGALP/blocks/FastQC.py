# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
Run FastQC
"""
input_description = """
a fastq file of reads
"""
output_description = """
an html report with quality control
"""

### Wrapper
def FastQC(name, rootpath, fastq_file, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(FastQC_runner)
    step_args = {
        "fastq_file" : fastq_file
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

# Example bash command
# 
# fastqc *.trimmed.fastq -t 8 -o fastqc_$directory
def FastQC_runner(step, args):
    """
    run fastQC on a fastq file
    input: 
    {
        "fastq_file" (full path)
        (aux) "n_threads"  
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["fastq_file"]

    basenamef1 = os.path.basename(f1)

    n_threads = multiprocessing.cpu_count()
    if "n_threads" in args:
        n_threads = args["n_threads"]
    
    command = "fastqc " + f1 + " -t " + str(n_threads) + " -o " + step.outpath 

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = {
        "html_report" : os.path.splitext(basenamef1)[0] + "_fastqc.html"
    }    

    return step