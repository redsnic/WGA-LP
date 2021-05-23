# --- default imports ---
import os
import multiprocessing

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

# Run trimming operations with TrimmomaticPE

description = """
Run TrimmomaticPE
"""
input_description = """
two fastq files of paired raw reads
"""
output_description = """
two fastq files of paired trimmed reads
"""

### Wrapper
def TrimmomaticPE(name, rootpath, raw_fwd, raw_rev, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(TrimmomaticPE_runner)
    step_args = {
        "raw_fwd" : raw_fwd,
        "raw_rev" : raw_rev
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

# Example bash command:
#
# TrimmomaticPE $f1.fastq $f2.fastq \
#        $f1.trimmed.fastq $f1.discarded.fastq \
#        $f2.trimmed.fastq $f2.discarded.fastq \
#        SLIDINGWINDOW:5:20 \
#        ILLUMINACLIP:TruSeq2-PE.fa:2:30:10
def TrimmomaticPE_runner(step, args):
    """
    run TrimmomaticPE to clean .fastq data
    input:
    {
        "raw_fwd" (full path)
        "raw_rev" (full path) 
        (aux) "slidingwindow" [windowSize,requiredQuality]
        (aux) "illuminaclip" [fastaWithAdaptersEtc,seed mismatches,palindrome clip threshold,simple clip threshold]
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["raw_fwd"]
    f2 = args["raw_rev"]

    basenamef1 = os.path.basename(f1)
    basenamef2 = os.path.basename(f2)

    out_FT = add_tag("trimmed", basenamef1) 
    out_FD = add_tag("discarded", basenamef1)
    out_RT = add_tag("trimmed", basenamef2)
    out_RD = add_tag("discarded", basenamef2)

    defaults_slidingwindow = ["5", "20"]
    defaults_illuminaclip = ["TruSeq2-PE.fa", "2", "30", "10"]

    command = (
        "TrimmomaticPE " + f1 + " " + f2 + " "
        "" + os.path.join(step.outpath, out_FT) + " " + os.path.join(step.outpath, out_FD) + " "
        "" + os.path.join(step.outpath, out_RT) + " " + os.path.join(step.outpath, out_RD) + " "
        "SLIDINGWINDOW:" + ":".join([default(args, "slidingwindow", defaults_slidingwindow[i], i) for i in range(len(defaults_slidingwindow))]) + " "
        "ILLUMINACLIP:" + ":".join([default(args, "illuminaclip", defaults_illuminaclip[i], i) for i in range(len(defaults_illuminaclip))]) + " "
    )

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = {
        "trimmed_fwd" : out_FT,
        "trimmed_rev" : out_RT,
        "discarded_fwd" : out_FD,
        "discarded_rev" : out_RD
    }