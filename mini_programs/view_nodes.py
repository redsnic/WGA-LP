#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders
from WGALP.blocks.r_node_analysis import view

# --- input arguments

def prepare_input(args):
    input_data = InputManager("Program to compute coverage plots for specific nodes from a samtools depth file")
    input_data.add_arg("--depth", "path", description="a .depth file from samtools depth")
    input_data.add_arg("--nodes", "list", description="list of node IDs to be considered (node IDs are the same of the original fasta file of the assembly)")
    input_data.add_arg("--all", "flag", description="plot coverage for every node, overrides --nodes")
    input_data.add_arg("--output", "dir", description="output folder")
    input_data.parse(args)
    return input_data

# --- input sanity checks

def sanity_check(depthfile, output_dir, nodes):
    check_files([depthfile])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)

# --- core function

def view_nodes_aux(depthfile, output_dir, nodes, pick_all):
    # sanity check
    sanity_check(depthfile, output_dir, nodes)
    out = view("coverage_plots", output_dir, depthfile, nodes, pick_all=pick_all)
 
    return out

# --- caller function

def view_nodes(args):

    in_manager = prepare_input(args)

    depthfile = in_manager["--depth"]["value"]
    output_dir = in_manager["--output"]["value"] 
    nodes = in_manager["--nodes"]["value"]
    pick_all = in_manager["--all"]["value"]

    output = view_nodes_aux(depthfile, output_dir, nodes, pick_all)

    print("task completed successfully")
    print("the plots of with coverages were saved at this location:")
    print("\t" + "output_dir" + " : " + output["output_dir"])

    return output
     
if __name__ == "__main__":
    view_nodes(sys.argv[1:])
    
    

    

    