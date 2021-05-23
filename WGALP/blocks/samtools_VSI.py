# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run samtools (view, sort, index)
"""
input_description = """
a sam file plus the options for samtools
"""
output_description = """
a sorted .bam file
"""

### Wrapper
# NOTE: VSI stands for View, Sort and Index, the passages used to produce .bam from .sam files
def samtools_VSI(name, rootpath, samfile, view_flags=None, index=True, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(samtools_VSI_runner)
    step_args = {
        "input_sam": samfile,
        "index" : index
    }
    if view_flags != None:
        step_args["view_flags"] = view_flags
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

### Runner
def samtools_VSI_runner(step, args):
    """
    execute the triple (view, sort, index) to 
    prepare a .bam file from a sam file. 
    view and index component can be skipped
    input:
    {
        "input_sam" (full path)
        (aux) "view_flags" (e.g. "-F 4")
        "index" (boolean)
        (aux) "outfile_name"
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["input_sam"]

    outfile = os.path.splitext(os.path.basename(f1))[0] + ".bam"  
    if "output_filename" in args:
        outfile = args["output_filename"]
    
    command = ""
    if "view_flags" in args:
        command += "samtools view -b " + args["view_flags"] + " " + f1 +  " | " 
        command += "samtools sort -o " + os.path.join(step.outpath, outfile) + " - ; "
    else:
        command += "samtools sort -o " + os.path.join(step.outpath, outfile) + " " + f1 + " ; "

    if args["index"]:
        command += "samtools index " + os.path.join(step.outpath, outfile) 

    if step.execution_mode != "read":
        run_sp(step, command)

    step.outputs = {
        "bamfile" : outfile
    }

    return step