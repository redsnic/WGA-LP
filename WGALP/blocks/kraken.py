
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
A PE pair of fastq files, along with pointers to kraken2 database
"""
output_description = """
A report and a log file. The latter is useful to find the exact imputed origin 
of each node/read evaluated by kraken2
"""

# Wrapper
def kraken(name, rootpath, kraken_db, memory_mapped, fastq1 = None, fastq2 = None, fasta=None, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(kraken_runner)
    step_args = {
        "kraken_db": kraken_db,
        "fastq1" : fastq1,
        "fasta" : fasta,
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
    input:
        fastq1 : path
        (aux) fastq2 : path (PE mode)
        fasta : path (fasta mode)
        kraken_db : path to kraken db folder
        memory_mapped : flag [highly recommanded for multiple calls when kraken_db is stored in a ramdisk]
        (aux) n_threads : number of threads to be used (default: use all available threads) 
    output:
        kraken_log : this log stores, among others, the association between read/nodes and probable organism of origin
        kraken_report : report containing a summary of the fraction of nodes/reads probably belonging to a certain organism
    """
    fasta = args["fasta"]
    f1 = args["fastq1"]
    paired_end_mode = "fastq2" in args
    if paired_end_mode:
        f2 = args["fastq2"]
    
    db = args["kraken_db"]

    n_threads = multiprocessing.cpu_count()
    if "n_threads" in args:
        n_threads = args["n_threads"]

    if fasta is not None:
        command  = "kraken2 --db " + db + " --threads " + str(n_threads) + " "
        command += fasta + " "
        command += "--output " + os.path.join(step.outpath, "kraken.log") + " "
        command += "--report " + os.path.join(step.outpath, "kraken.report") + " "
    else:   
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

    command += "--use-names "

    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {
        "kraken_log" : "kraken.log",
        "kraken_report" : "kraken.report"
    }

    return step

