# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
Run quast
"""
input_description = """
a fasta file of the WGA
"""
output_description = """
Html report
"""

### Wrapper
def quast(name, rootpath, fasta_file, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(quast_runner)
    step_args = {
        "fasta_file" : fasta_file,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

# Example bash command
# 
# fastqc *.trimmed.fastq -t 8 -o fastqc_$directory
def quast_runner(step, args):
    """
    run checkM on a fasta file
    input: 
    {
        "fasta_file" (full path)
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["fasta_file"]

    command = "quast " + f1 + " -o " + os.path.join(step.outpath, "quast")

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = {
        "quast_report_html" : "quast/report.html"
    }    

    return step