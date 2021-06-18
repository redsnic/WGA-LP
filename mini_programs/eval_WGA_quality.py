import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from WGALP.blocks.checkM import checkM_lineage
from WGALP.blocks.quast import quast
from WGALP.blocks.merqury import merqury
from WGALP.utils.genericUtils import merge_two_dicts

def prepare_input(args):
    input_data = InputManager("Run tools to evaluate WGA quality (CheckM ... TODO)")
    input_data.add_arg("--fastq-fwd", "path", description="raw forward reads (.fastq)")
    input_data.add_arg("--fastq-rev", "path", description="raw reverse reads (.fastq)")
    input_data.add_arg("--assembly", "path", description="WGA assembly to evaluate (.fasta)")
    input_data.add_arg("--output", "dir", description="path to the output folder")
    input_data.add_arg("--output", "dir", description="path to the output folder")
    input_data.add_arg("--full-tree", "dir", description="use full tree in checkM instead reduced_tree (requires > 40GB of ram)")
    input_data.add_arg("--kmer-length", "text", description="kmer size to be used in merqury (use 16 for 3Mpb, check with: $MERQURY/best_k.sh <genome_size>)")
    input_data.parse(args)
    return input_data

def sanity_check(fwd_reads, rev_reads, fasta_WGA, output_dir, reduced_tree, kmer):
    try:
        int(kmer)
    except Exception:
        raise Exception("--kmer-size argument must be an integer")
    check_files([fwd_reads, rev_reads, fasta_WGA])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

def eval_WGA_quality(fwd_reads, rev_reads, fasta_WGA, output_dir, reduced_tree=True, kmer="16"):
    # sanity check
    sanity_check(fwd_reads, rev_reads, fasta_WGA, output_dir, reduced_tree, kmer)
    kmer = int(kmer)
    out_checkm = checkM_lineage("checkM_Lineage", output_dir, fasta_WGA, reduced_tree=reduced_tree)
    out_quast = quast("quast", output_dir, fasta_WGA)
    out_merqury = merqury("merqury", output_dir, fasta_WGA, fwd_reads, rev_reads, kmer=kmer)
    
    out = merge_two_dicts(out_checkm.get_files(), out_quast.get_files())
    out = merge_two_dicts(out, out_merqury.get_files())
    return out
     

if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

    fwd_reads = in_manager["--fastq-fwd"]["value"]
    rev_reads = in_manager["--fastq-rev"]["value"]
    fasta_WGA = in_manager["--assembly"]["value"]
    output_dir = in_manager["--output"]["value"]
    reduced_tree = not in_manager["--full-tree"]["value"]
    kmer_length = in_manager["--kmer-length"]["value"]
    
    output = eval_WGA_quality(fwd_reads, rev_reads, fasta_WGA, output_dir, reduced_tree=reduced_tree, kmer=kmer_length)

    print("task completed successfully")
    print("\tcheckm_report_table : " + output["checkm_report_table"])
    print("\tquast_report_html : " + output["quast_report_html"])
    print("\tmerqury_output_dir : " + output["merqury_output_dir"])
    print("check " + output_dir + " for other reports")
