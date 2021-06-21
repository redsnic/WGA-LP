#!/usr/bin/env python3

# MAIN PROGRAM 


import sys

# todo import pipeline programs (they take in input just the args!)
from mini_programs.evaluate_quality import evaluate_quality
from mini_programs.decontamination_workflow import decontamination_workflow
from mini_programs.assemble_with import assemble_with
from mini_programs.check_coverage import check_coverage
from mini_programs.order_contigs import order_contigs
from mini_programs.filter_fasta import select_contigs
from mini_programs.prokka_annotate import prokka_annotate
from mini_programs.run_recycle import run_recycle
from mini_programs.eval_WGA_quality import WGA_quality_check

def help():
    out = " --- wgalp: a pipeline for bacterial Whole Genome Assembly ---\n\n"
    out += "This programs is an helper to run the sub procedures of wgalp\n"
    out += "usage: wgalp <program> [args]\n\n"
    out += "the following is a list of all the available programs:\n"
    out += "\ttrim : trim reads and/or assess contaminations with kraken2\n"
    out += "\tdecontaminate : remove reads mapping to a contaminant non ambiguosly\n"
    out += "\tassemble : assemble reads into scaffolds or contigs\n"
    out += "\tcheck-coverage : compute coverage statistics of an assembled genome\n"
    out += "\treorder : reorder a whole genome assembly using a reference genome\n"
    out += "\tfilter-contigs : select contigs by ID\n"
    out += "\t                 (to be used with the webapp: https://redsnic.shinyapps.io/ContigCoverageVisualizer/)\n"
    out += "\tannotate : run prokka annotation with NCBI standard\n"
    out += "\tplasmid : extract putative plasmids using recycler\n"
    out += "\tquality : evaluate assembly quality using checkM, merqury and quast\n"
    out += "\thelp : show this message (equivalent to --help or -h)\n"
    out += "\nRun wgalp <program> --help for specific information about the selected program.\n"
    return out

if __name__ == "__main__":

    options = {
        "trim" : evaluate_quality,
        "decontaminate" : decontamination_workflow,
        "assemble" : assemble_with,
        "check-coverage" : check_coverage,
        "reorder" : order_contigs,
        "filter-contigs" : select_contigs,
        "annotate" : prokka_annotate,
        "plasmid" : run_recycle,
        "quality" : WGA_quality_check 
    }

    if len(sys.argv) == 1:
        print(help())
        exit()

    if sys.argv[1] in ["help", "--help", "-h"]:
        print(help())
        exit()

    try:
        options[sys.argv[1]]
    except KeyError:
        print("ERROR: invalid program " + sys.argv[1] + ". Please choose a valid option from the list\n")
        print(help())

    # run program
    options[sys.argv[1]](sys.argv[2:])





