# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
Run quast to asses WGA quality
"""
input_description = """
A fasta file resultin from a WGA
"""
output_description = """
An html report with useful data and a cumulative length plot
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

### Runner
def quast_runner(step, args):
    """
    input: 
        fasta_file : path
    output: 
        quast_report_html : quast report
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