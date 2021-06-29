# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """ 
Run bazam to convert .bam file back to fastq format
"""
input_description = """
an indexed bam file
"""
output_description = """
a .fastq file
"""

### Wrapper
def bazam(name, rootpath, bamfile, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(bazam_runner)
    step_args = {
        "input_bam": bamfile,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

### Runner
def bazam_runner(step, args):
    """
    input:
        input_bam : path (bam must be indexed)
        (aux) outfile_name : string
    output:
        fastqfile : path
    """

    f1 = args["input_bam"]

    outfile = os.path.splitext(os.path.basename(f1))[0] + ".fastq"  
    if "output_filename" in args:
        outfile = args["output_filename"]

    command = "bazam -bam " + f1 + " > " + os.path.join(step.outpath, outfile)

    if step.execution_mode != "read":
        run_sp(step, command)

    step.outputs = {
        "fastqfile" : outfile
    }

    return step


