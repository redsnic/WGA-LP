# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

# Run trimming operations with TrimmomaticPE

description = """
Run Prokka annotation (in NCBI compliant mode)
"""
input_description = """
A fasta file resulting from a WGA (possibly filtered and ordered)
"""
output_description = """
the prokka annotated genome in many different formats
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

### Runner
def prokka_runner(step, args):
    """
    run Prokka annotation
    input:
        assembled_seqence : a fasta file containing the output of an assembler
    output:
        ffn : annotated genome in this format
        faa : annotated genome in this format
        gbk : annotated genome in this format
        gff : annotated genome in this format
        tsv : annotated genome in this format
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