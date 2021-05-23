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
def prokka(name, rootpath, assembled_seqence, execution_mode="on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(prokka_runner)
    step_args = {
        "assembled_seqence" : assembled_seqence
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
def prokka_runner(step, args):
    """
    run TrimmomaticPE to clean .fastq data
    input:
    {
        "assembled_seqence" a fasta file containing the output of an assembler
    }
    :param args: a dictionary of the arguments
    """
    f1 = args["assembled_seqence"]

    command = "prokka --force --centre NCBI --compliant --outdir " + step.outpath + " --prefix prokka_annotated_genome " + f1 + " " 

    if step.execution_mode != "read":
        run_sp(step, command)

    step.inputs = args

    # organize output

    step.outputs = { 
        "ffn":"prokka_annotated_genome.fnn",
        "faa":"prokka_annotated_genome.faa",
        "gbk":"prokka_annotated_genome.gbk",
        "gff":"prokka_annotated_genome.gff",
        "tsv":"prokka_annotated_genome.tsv"
    }