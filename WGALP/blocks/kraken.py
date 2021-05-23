
# --- default imports ---
import os
import multiprocessing

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

# Wrapper
def kraken(name, rootpath, kraken_db, memory_mapped, fastq1 = None, fastq2 = None, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(kraken_runner)
    step_args = {
        "kraken_db": kraken_db,
        "fastq1" : fastq1,
        "memory_mapped" : memory_mapped
    }
    if fastq2 != None:
        step_args["fastq2"] = fastq2
    step.run(step_args)
    step.set_description("Run kracken and Bracken", "...", "...")
    return step

### Runner
def kraken_runner(step, args):
    """
    given a pair of fastq files, compute the possible origin of the DNA sequences
    input:
    {
        "fastq1" (full path)
        (aux) "fastq2" (full path)
        "kraken_db" (full path)
        "memory_mapped" (boolean) [highly recommanded]
        (aux) "n_threads" 
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["fastq1"]
    paired_end_mode = "fastq2" in args
    if paired_end_mode:
        f2 = args["fastq2"]

    db = args["kraken_db"]

    n_threads = multiprocessing.cpu_count()
    if "n_threads" in args:
        n_threads = args["n_threads"]

    if paired_end_mode:
        command  = "kraken2 --db " + db + " --threads " + str(n_threads) + " "
        command += "--paired " + f1 + " " + f2 + " "
        command += "--output " + os.path.join(step.outpath, "kraken.log") + " "
        command += "--report " + os.path.join(step.outpath, "kraken.report") + " "
    else:
        command  = "kraken2 --db " + db + " --threads " + str(n_threads) + " "
        command += f1 + " "
        command += "--output " + os.path.join(step.outpath, "kraken.log") + " "
        command += "--report " + os.path.join(step.outpath, "kraken.report") + " "

    if args["memory_mapped"]:
        command += " --memory-mapping "

    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {
        "kraken_log" : "kraken.log",
        "kraken_report" : "kraken.report"
    }

    return step

