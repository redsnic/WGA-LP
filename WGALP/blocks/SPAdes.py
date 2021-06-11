# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run SPAdes"
"""
input_description = """
a paired end pair of fastq files
"""
output_description = """
the contigs or scaffolds of the assembled genome
"""

### Wrapper
def SPAdes(name, rootpath, fastq_fwd, fastq_rev, plasmid = False, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(SPAdes_runner)
    step_args = {
        "fastq_fwd" : fastq_fwd,
        "fastq_rev" : fastq_rev,
        "plasmid" : plasmid
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

# Example bash command
#
# spades.py -1 $f1.trimmed.fastq -2 $f2.trimmed.fastq -o spades_out_$directory/ --careful 
def SPAdes_runner(step, args):
    """
    run sades on a pair of .fastq files
    input:
    {
        "fastq_fwd" (full path) (it seems that these must have different filenames ...)
        "fastq_rev" (full path)
        "plasmid" (boolean)   
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["fastq_fwd"]
    f2 = args["fastq_rev"]

    command = "spades.py -1 " + f1 + " -2 " + f2 + " -o " + step.outpath 
    
    if args["plasmid"]:
        command += " --plasmid"
    else:
        pass
        # sometimes crashes ...
        # command += " --careful"


    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {
        "contigs" : "contigs.fasta",
        "scaffolds" : "scaffolds.fasta",
        "assembly_graph" : "assembly_graph.fastg"
    }

    return step