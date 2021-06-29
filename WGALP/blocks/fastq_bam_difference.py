# --- default imports ---
import os

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step
from WGALP.tools.filter_fastq import filter_fastq_reads

description = """
compute the difference between the sets of reads contained in a fastq and a bam files
"""
input_description = """
a fastq and a bam files
"""
output_description = """
the reads resulting from the set difference (in fastq)
"""

### Wrapper
def fastq_bam_difference(name, rootpath, fastq, bam, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(fastq_bam_difference_runner)
    step_args = {
        "fastq": fastq,
        "bam": bam,
        "name": name # necessary to avoid using the same names in SPAdes...
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step


def fastq_bam_difference_runner(step, args):
    """
    input:
        fastq : path
        bam : path
        name : text (remeber that SPAdes can't work with same names and different directories!)
    output:
        filtered_fastq : the fastq containg the reads resulting from the set difference
    """    

    f1 = args["fastq"]
    f2 = args["bam"]

    bad_list = os.path.join(step.outpath, "bad_reads_ids.txt")

    command  = "samtools view " + f2 + " | cut -f 1 | uniq > " + bad_list 

    if step.execution_mode != "read":
        run_sp(step, command)

    # run python script to compute the filtered fastq
    filter_fastq_reads(f1, bad_list, os.path.join(step.outpath, "filtered_reads_" + args["name"] + ".fastq"))

    step.outputs = {
        "filtered_fastq" : "filtered_reads_" + args["name"] + ".fastq"
    }

    return step 

