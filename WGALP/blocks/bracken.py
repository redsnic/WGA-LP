# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
given a kraken2 report, compute the probability of possible origin of the DNA sequences
"""
input_description = """
A kraken2 report, along with pointers to kraken2 database
"""
output_description = """
A couple of reports, specifing the imputed source of DNA fragments
"""

### Wrapper
def bracken(name, rootpath, kraken_report, kraken_db, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(bracken_runner)
    step_args = {
        "kraken_db": kraken_db,
        "kraken_report" : kraken_report,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

### Runner
def bracken_runner(step, args):
    """
    input:
        kraken_report : path
        kraken_db : path
    output:
        bracken_report : a summary containing the origin of reads/nodes 
        bracken_log : log of the execution 
    """
    f1 = args["kraken_report"]
    db = args["kraken_db"]

    command  = "bracken -d " + db + " -i " + f1 + " "
    command += "-o " + os.path.join(step.outpath, "bracken.log") + " "
    command += "-w " + os.path.join(step.outpath, "bracken.report") + " "

    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {
        "bracken_report" : "bracken.report",
        "bracken_log" : "bracken.log"
    }

    return step





    


    