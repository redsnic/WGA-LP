# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Easily run samtools view, sort and index workflow
"""
input_description = """
A sam file plus the options for samtools' programs
"""
output_description = """
A sorted .bam file
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
    view and index component can be skipped
    input:
        input_sam : path
        (aux) view_flags : text (e.g. "-F 4")
        index : flag
        (aux) outfile_name : text
    output:
        bamfile : sorted bam file as specified
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