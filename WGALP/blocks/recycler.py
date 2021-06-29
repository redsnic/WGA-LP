# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

# Run trimming operations with TrimmomaticPE

description = """
Run recycler to extract plasmids
"""
input_description = """
a fasta file with the WGA contigs
"""
output_description = """
the extracted plasmid in fasta format
"""

### Wrapper
def recycler(name, rootpath, realignment, assembly_graph, kmer_length, execution_mode="on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(recycler_runner)
    step_args = {
       "realignment_to_graph" : realignment,
        "assembly_graph" : assembly_graph,
        "kmer_length" : kmer_length
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

### Runner
def recycler_runner(step, args):
    """
    input:
        realignment_to_graph : path (a bam file representing the alignment of the reads with the assembly)
        assembly_graph : path (an assembly graph (usually from SPAdes))
        kmer_length : number (max kmer length used by the aligner (127 for SPAdes))
    ouptut:
        plasmid_fasta : a fasta containing the extracted plasmids
    """
    f1 = args["realignment_to_graph"]
    f2 = args["assembly_graph"]
    kmers = args["kmer_length"]

    command = "recycle.py -g " + f2 + " -k " + str(kmers) + " -b " + f1 + " -i True -o " + step.outpath

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = { 
        "plasmid_fasta" : "assembly_graph.cycs.fasta"
    }