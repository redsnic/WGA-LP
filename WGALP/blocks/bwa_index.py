# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """ 
Run bwa index
"""
input_description = """
a fasta file to be indexed
"""
output_description = """
nothing
"""

### Wrapper
def bwa_index(name, rootpath, fasta, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(bwa_index_runner)
    step_args = {
        "fasta": fasta,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    step.delete()
    # nothing to return 

### Runner
def bwa_index_runner(step, args):
    """
    run bwa index on a fasta file
    input:
    {
        "fasta" (full path)
    }
    :param args: a dictionary of the arguments
    """

    f1 = args["fasta"]

    command = "bwa index " + f1 

    if step.execution_mode != "read":
        run_sp(step, command)

    return {}


