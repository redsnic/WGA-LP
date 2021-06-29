# --- default imports ---
import os
import pandas as pd

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run samtools depth to compute coverage statistics
"""
input_description = """
A bam file from which to extract the statistics
"""
output_description = """
.depth and .depth.summary files, the fisrt is the direct output of samtools depth, 
the latter is a semplification, useful to run node selection 
"""

### Wrapper
def samtools_depth(name, rootpath, bamfile, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(samtools_depth_runner)
    step_args = {
        "input_bam": bamfile,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

def summarise_depth(depth_file, out_file):
    """
    prepare .depth.summary file
    """
    df = pd.read_csv(depth_file, sep='\t', names=["Name", "Position", "NReads"])
    df = df.groupby(["Name"])["NReads"].agg(Length="count",Coverage="mean",Sd="std").reset_index()
    df.to_csv(out_file, sep="\t")

### Runner
def samtools_depth_runner(step, args):
    """
    input:
        input_bam : path
    output:
        depth_file : direct ouptut tsv from samtools depth
        depth_summary : summarized ouptut for node distribution analysis
    """

    f1 = args["input_bam"]
    
    out_filename = os.path.splitext(os.path.basename(f1))[0] + ".depth"

    command  = "samtools depth " + f1 + " " + " > " + os.path.join(step.outpath, out_filename) 

    if step.execution_mode != "read":
        run_sp(step, command)
        summarise_depth(os.path.join(step.outpath, out_filename), os.path.join(step.outpath, out_filename + ".summary"))


    step.outputs = {
        "depth_file" : out_filename,
        "depth_summary" : out_filename + ".summary"
    }

    return step 