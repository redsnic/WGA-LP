# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
Run checkM
"""
input_description = """
a fasta file of the WGA
"""
output_description = """
A log file
"""

### Wrapper
def checkM_lineage(name, rootpath, fasta_file, reduced_tree=True, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(checkM_lineage_runner)
    step_args = {
        "fasta_file" : fasta_file,
        "reduced_tree" : reduced_tree
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

# Example bash command
# 
# fastqc *.trimmed.fastq -t 8 -o fastqc_$directory
def checkM_lineage_runner(step, args):
    """
    run checkM on a fasta file
    input: 
    {
        "fasta_file" (full path)
        "reduced_tree" (use reduced tree, True by default)
        (aux) "n_threads"  
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["fasta_file"]

    n_threads = multiprocessing.cpu_count()
    if "n_threads" in args:
        n_threads = args["n_threads"]
    
    try:
        extension = os.path.splitext( os.path.basename(f1) )[1][1:]
    except Exception:
        extension = os.path.splitext( os.path.basename(f1) )[1]

    command = "mkdir " + os.path.join(step.outpath, "bin") + "; cp " + f1 + " " + os.path.join(step.outpath, "bin") + " && "
    command += "checkm lineage_wf -x " + extension + " -t" + str(n_threads) + " " + os.path.join(step.outpath, "bin") + " " + os.path.join(step.outpath, "checkm") + " "
    if args["reduced_tree"]:
        command += "--reduced_tree "
    command += "> " + os.path.join(step.outpath, "report_table.txt")

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = {
        "checkm_report_table" : "report_table.txt"
    }    

    return step