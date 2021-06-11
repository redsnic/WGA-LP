# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

# Run trimming operations with TrimmomaticPE

description = """
Run Prokka annotation
"""
input_description = """
a fasta file of contigs
"""
output_description = """
the annotated genome (in many formats, .gff will be the default)
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

# Example bash command:
#
# TrimmomaticPE $f1.fastq $f2.fastq \
#        $f1.trimmed.fastq $f1.discarded.fastq \
#        $f2.trimmed.fastq $f2.discarded.fastq \
#        SLIDINGWINDOW:5:20 \
#        ILLUMINACLIP:TruSeq2-PE.fa:2:30:10
def recycler_runner(step, args):
    """
    run recycler for plasmid extraction
    input:
    {
        "realignment_to_graph" a bam file representing the alignment of the reads with the assembly
        "assembly_graph" an assembly graph (usually from SPAdes)
        "kmer_length" max kmer length used by the aligner (127 for SPAdes)
    }
    :param args: a dictionary of the arguments
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