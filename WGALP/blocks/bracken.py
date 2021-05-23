# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
run kraken tool
"""
input_description = """
...
"""
output_description = """
...
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
    given a pair of fastq files, compute the possible origin of the DNA sequences
    input:
    {
        "kraken_report" (full path)
        "kraken_db" (full path)
    }
    :param args: a dictionary of the arguments
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





    


    