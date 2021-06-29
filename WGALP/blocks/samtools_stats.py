# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run samtools stats and plot-bamstats
"""
input_description = """
a sam file of an alignmente
"""
output_description = """
reports with sam file statistics and plots
"""

def samtools_stats(name, rootpath, samfile, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(samtools_stats_runner)
    step_args = {
        "input_sam": samfile,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

def samtools_stats_runner(step, args):
    """
    input:
        input_sam : path
    output:
        html_report : plot-bamstats html report
        txt_report : textual report of samtools stats
    """

    f1 = args["input_sam"]
    stats_dir = "plots/"

    command  = "samtools stats " + f1 + " " + " > " + os.path.join(step.outpath, "samtools.stats") + " && "
    command += "plot-bamstats " + os.path.join(step.outpath, "samtools.stats") + " -p " + os.path.join(step.outpath, stats_dir) 

    if step.execution_mode != "read":
        run_sp(step, command)

    step.outputs = {
        "html_report" : os.path.join(stats_dir, "index.html"),
        "txt_report" : "samtools.stats"
    }

    return step 