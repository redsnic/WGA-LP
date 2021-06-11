# --- default imports ---
import os
import re

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.utils.genericUtils import *
from WGALP.step import Step

description = """
Run mauve to reorder contigs
"""
input_description = """
the reference and the assembled genome to be ordered
"""
output_description = """
the ordered reference 
"""

### Wrapper
def mauve_contig_sorting(name, rootpath, reference, contigs, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(mauve_contig_sorting_runner)
    step_args = {
        "reference": reference,
        "contigs" : contigs
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description) 
    return step

### Runner
def mauve_contig_sorting_runner(step, args):
    """
    run BWA alignment on a pair or a single fastq file
    input:
    {
        "reference" (full path)
        "contigs" (full path)
    }
    :param args: a dictionary of the arguments
    """
    contig = args["contigs"]
    ref = args["reference"]

    command = "mauveContigOrderer -output " + step.outpath + " -ref " +  ref + " -draft " + contig + " "   
    
    if step.execution_mode != "read":
        run_sp(step, command)

    # get most accurate fasta file
    if not step.outpath.endswith("/"):
        outdir = "alignment" + str(max([ int(x[0][len(step.outpath)+1:].replace("alignment", "")) for x in list(os.walk(step.outpath))[1:] ]))
    else:
        outdir = "alignment" + str(max([ int(x[0][len(step.outpath):].replace("alignment", "")) for x in list(os.walk(step.outpath))[1:] ]))
    
    # check if there is a less "hard coded" approach
    # outfile = [f for f in os.listdir(os.path.join(step.outpath, outdir)) if re.match(r".*\.fasta$", f)][0]
    outfile = os.path.splitext(os.path.basename(contig))[0] + ".fasta"

    # organize output

    step.outputs = {
        "contigs" : os.path.join(outdir, outfile) 
    }
 
    return step