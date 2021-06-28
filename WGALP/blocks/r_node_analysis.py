# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

# Compute coverage statistics using an R script

description = """
Compute coverage statistics using an R script
"""
input_description = """
.depth file
"""
output_description = """
plots in png format
"""

### Wrapper
def view(name, rootpath, depthfile, nodes, pick_all=False, execution_mode="force"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(view_runner)
    step_args = {
        "depthfile" : depthfile,
        "nodes" : nodes,
        "mode" : "view" if not pick_all else "view-all"
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

def view_runner(step, args):
    """
    run recycler for plasmid extraction
    input:
    {
        "depthfile"
        "nodes" 
        "mode"
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["depthfile"]
    mode = args["mode"]
    nodes = args["nodes"]

    if mode == "view":
        command = "Rscript RScripts/pileupVisualizer.R --args " + mode + " " + f1 + " " + step.outpath + " " + " ".join(nodes) + " "
    else:
        command = "Rscript RScripts/pileupVisualizer.R --args " + mode + " " + f1 + " " + step.outpath + " "

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = { 
        "output_dir" : ""
    }