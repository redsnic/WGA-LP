# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run samtools depth 
"""
input_description = """
a bam file
"""
output_description = """
coverage file 
"""

def samtools_depth(name, rootpath, bamfile, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(samtools_depth_runner)
    step_args = {
        "input_bam": bamfile,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

def samtools_depth_runner(step, args):
    """
    run samtools depth
    input:
    {
        "input_bam" (full path)
    }
    :param args: a dictionary of the arguments
    """

    f1 = args["input_bam"]
    
    out_filename = os.path.splitext(os.path.basename(f1))[0] + ".depth"

    command  = "samtools depth " + f1 + " " + " > " + os.path.join(step.outpath, out_filename) 

    if step.execution_mode != "read":
        run_sp(step, command)

    step.outputs = {
        "depth_file" : out_filename
    }

    return step 