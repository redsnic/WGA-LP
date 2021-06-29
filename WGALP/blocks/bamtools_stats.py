# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
Run bamtools stats tool
"""
input_description = """
a bam file, representing an alignment
"""
output_description = """
a summary, containing some statistics about the alignment 
"""

### Wrapper
def bamtools_stats(name, rootpath, bamfile, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(bamtools_stats_runner)
    step_args = {
        "input_bam": bamfile,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

### Runner
def bamtools_stats_runner(step, args):
    """ 
    input:
        input_bam : path
    output:
        txt_report : path
    """

    f1 = args["input_bam"]

    command  = "bamtools stats -in " + f1 + " " + " > " + os.path.join(step.outpath, "bamtools.stats") 

    if step.execution_mode != "read":
        run_sp(step, command)

    step.outputs = {
        "txt_report" : "bamtools.stats"
    }

    return step 