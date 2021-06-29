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
A .depth file resulting from samtools depth 
"""
output_description = """
A folder containing plots in .png format
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
    input:
        depthfile : path (.depth file)
        nodes :  text list (a list of node IDs)
        mode : text (currently view or view-all)
    output:
        output_dir : just a link to the output directory
    """
    f1 = args["depthfile"]
    mode = args["mode"]
    nodes = args["nodes"]

    script_path = os.path.split(os.path.realpath(__file__))[0]
    script_path = os.path.join(script_path, "../../RScripts/pileupVisualizer.R")

    if mode == "view":
        command = "Rscript " + script_path + " --args " + mode + " " + f1 + " " + step.outpath + " " + " ".join(nodes) + " "
    else:
        command = "Rscript " + script_path + " --args " + mode + " " + f1 + " " + step.outpath + " "

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = { 
        "output_dir" : ""
    }