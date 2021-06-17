import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from WGALP.blocks.checkM import checkM_lineage

def prepare_input(args):
    input_data = InputManager("Run tools to evaluate WGA quality (CheckM ... TODO)")
    input_data.add_arg("--assembly", "path", description="WGA assembly to evaluate (.fasta)")
    input_data.add_arg("--output", "dir", description="path to the output folder")
    input_data.add_arg("--output", "dir", description="path to the output folder")
    input_data.add_arg("--full-tree", "dir", description="use full tree in checkM instead reduced_tree (requires > 40GB of ram)")
    input_data.parse(args)
    return input_data

def sanity_check(fasta_WGA, output_dir):
    check_files([fasta_WGA])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

def eval_WGA_quality(fasta_WGA, output_dir, reduced_tree=True):
    # sanity check
    sanity_check(fasta_WGA, output_dir)
    out = checkM_lineage("checkM_Lineage", output_dir, fasta_WGA, reduced_tree=reduced_tree)
    return out
     

if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

   
    fasta_WGA = in_manager["--assembly"]["value"]
    output_dir = in_manager["--output"]["value"]
    reduced_tree = not in_manager["--full-tree"]["value"]
    
    output = eval_WGA_quality(fasta_WGA, output_dir, reduced_tree=reduced_tree)

    print("task completed successfully")
    print("\treport_table : " + output["report_table"])
    print("check " + output_dir + " for the quality reports")
