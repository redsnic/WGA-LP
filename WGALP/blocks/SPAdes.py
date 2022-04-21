# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run SPAdes whole genome assembler
"""
input_description = """
A paired end pair of fastq files
"""
output_description = """
The contigs and scaffolds of the assembled genome
"""

### Wrapper
def SPAdes(name, rootpath, fastq_fwd, fastq_rev, plasmid = False, execution_mode = "on_demand", only_assembler = False):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(SPAdes_runner)
    step_args = {
        "fastq_fwd" : fastq_fwd,
        "fastq_rev" : fastq_rev,
        "plasmid" : plasmid,
        "only-assembler" : only_assembler
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

# Example bash command
#
# spades.py -1 $f1.trimmed.fastq -2 $f2.trimmed.fastq -o spades_out_$directory/ --careful 
### Runner
def SPAdes_runner(step, args):
    """
    input:
        fastq_fwd : path 
        fastq_rev : path (fastq_fwd and fastq_rev must have different filenames ...)
        plasmid : flag (run plasmid extraction) 
        only-assembler : avoid using read error correction (useful with low quality reads)  
    output:
        contigs : SPAdes generated contigs
        scaffolds : SPAdes generated scaffolds (links contigs using paired end reads)
        assembly_graphs : SPAdes assembly graph
    """
    f1 = args["fastq_fwd"]
    f2 = args["fastq_rev"]
    only_assembler = args["only-assembler"]

    command = "spades.py -1 " + f1 + " -2 " + f2 + " -o " + step.outpath 

    if only_assembler:
        command += " --only-assembler"
    
    
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