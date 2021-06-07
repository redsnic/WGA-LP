import sys
import os
import subprocess
import pandas
import re
from WGALP.utils.input_manager import InputManager
from WGALP.checkpoint import make_checkpoint
from WGALP.checkpoint import load_checkpoint
from WGALP.utils.genericUtils import merge_two_dicts

# import tools for this pipeline 
from sub_workflows.fastq_trimming import TrimFastq
from sub_workflows.kraken_bracken import KrakenBracken
from sub_workflows.remove_contaminant import RemoveContaminant
from sub_workflows.run_assemblers import RunAssemblers 
from sub_workflows.reorder_and_annotate import ReorderAndAnnotate
from WGALP.blocks.mauve import mauve_contig_sorting

# Requirements:
# ~ 1 GB per genome of disk space, ~ 9 GB RAM

def rename_key(dict_, key_, new_key_):
    dict_[new_key_] = dict_[key_]
    dict_[key_] = None
    return dict_

def load_fastq_files(directory):
    files = os.listdir(directory)

    if len(files) != 2:
        print("ERROR: input directories must contain forwad and reverse reads only")
        print("INFO: the files should match the following regular expressions")
        print("INFO: *_R1_*.fastq and *_R2_*.fastq respectively")

    out = {}
    for f in files:
        if re.match(r".*_R1_.*\.fastq", f):
            out["fastq_fwd"] = os.path.join(directory, f)
        elif re.match(r".*_R2_.*\.fastq", f):
            out["fastq_rev"] = os.path.join(directory, f)
        else:
            print("ERROR: bad file in input folder: " + f)
            print("INFO: the files should match the following regular expressions")
            print("INFO: *_R1_*.fastq and *_R2_*.fastq respectively")
            raise FileNotFoundError

    return out

def prepare_input(args):
    input_data = InputManager()
    input_data.add_arg("--input", "list")
    input_data.add_arg("--output", "path")
    input_data.add_arg("--ref-table", "path")
    input_data.add_arg("--ref-location-table", "path")
    input_data.add_arg("--kraken-db", "path")
    input_data.parse(args)
    return input_data

def get_reference(dir_id, metadata, position):
    metadata_df = pandas.read_table(metadata, header = 0)
    position_df = pandas.read_table(position, header = 0)
    organism = metadata_df.query('Folder == "' + dir_id + '"')["Organism"].iloc[0]
    path = position_df.query('Reference == "' + organism + '"')["Location"].iloc[0]
    return path

def get_contaminant(position, contaminant):
    position_df = pandas.read_table(position, header = 0)
    organism = contaminant
    path = position_df.query('Reference == "' + organism + '"')["Location"].iloc[0]
    return path
    
if __name__ == "__main__":

    # usage: python3 workflow.py outputdir reference_table reference_location_table input_dir1 input_dir2 ...
    in_manager = prepare_input(sys.argv[1:])
    
    # base_root = "/home/redsnic/WGA_batteri/PythonWorkflow/test_dir/" 
    base_root = in_manager["--output"]["value"]
    path_to_reference_table = in_manager["--ref-table"]["value"]
    path_to_reference_location = in_manager["--ref-location-table"]["value"]
    input_data_directories = in_manager["--input"]["value"]
    karaken_db_on_disk_location = in_manager["--kraken-db"]["value"]

    # input checks

    if os.path.isfile(base_root):
        print("ERROR: cannot use a file as output directory")
        raise FileExistsError
    if os.path.isdir(base_root):
        print("INFO: working on an already existing directory")
    else:
        os.mkdir(base_root)
        print("INFO: created output directory " + base_root)

    try:
        reference_table = pandas.read_table(path_to_reference_table, header=0)
        # file must have the "Folder" and "Organism" columns 
        if not "Folder" in reference_table.columns or not "Organism" in reference_table.columns:
            raise Exception("Wrong structure of reference table file")
    except:
        print("ERROR: invalid reference table file")
        raise 

    try:
        reference_location_table = pandas.read_table(path_to_reference_location, header=0)
        # file must have the "Reference" and "Location" columns 
        if not "Reference" in reference_location_table.columns or not "Location" in reference_location_table.columns:
            raise Exception("Wrong structure of reference location table file")
    except:
        print("ERROR: invalid reference table file")
        raise 


    # this command requires root to run certain programs 
    print("Root is required to run kraken2/bracken efficently, creating a ramdisk for krakendb")
    try:
        subprocess.run("sudo echo 'Root premissions granted'", shell=True, check=True)
    except:
        print("Failed to gain root permissions... try again")
        raise
    
    # Main Execution
    
    # --- FastQC/Trimming loop

    output_directories = {}
    sample_identifiers = {}
    for directory in input_data_directories:
        out_dir = os.path.join(base_root, os.path.basename(directory))
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        output_directories[directory] = out_dir 
        sample_identifiers[directory] = os.path.basename(directory)

    trimmed_reads = {}
    for directory in input_data_directories:
        # execution folder
        root = output_directories[directory]
        raw_reads = load_fastq_files(directory)
        trimmed_reads[directory] = TrimFastq("fastq_trimming", root).run(raw_reads)
        rename_key(trimmed_reads[directory], 'trimmed_fwd', 'fastq_fwd')
        rename_key(trimmed_reads[directory], 'trimmed_rev', 'fastq_rev')

    # --- run kraken before cleanup

    kraken_input = {}
    kraken_input["input_fastq"] = trimmed_reads
    kraken_input["prefix"] = "before_cleanup_"
    kraken_input["kraken_db"] = karaken_db_on_disk_location
    KrakenBracken("before_cleanup_kraken", base_root).run(kraken_input)

    # run filtering

    filtered_reads = {}
    for directory in input_data_directories:
        try:
            # execution folder
            root = output_directories[directory]
            raw_reads = load_fastq_files(directory)
            # get reference and contaminant
            reference = get_reference(sample_identifiers[directory], path_to_reference_table, path_to_reference_location) 
            contaminant = get_contaminant(path_to_reference_location, "Pediococcus_acidilactici") 
            # set input arguments
            input_args = {}
            input_args["fastq_fwd"] = trimmed_reads[directory]["fastq_fwd"]
            input_args["fastq_rev"] = trimmed_reads[directory]["fastq_rev"]
            input_args["reference"] = reference
            input_args["contaminant"] = contaminant
            filtered_reads[directory] = RemoveContaminant("remove_contaminant", root).run(input_args)
        except Exception as e:
            print("INFO: skipping decontamination for " + sample_identifiers[directory])
            filtered_reads[directory] = trimmed_reads[directory] 

    # run kraken after filtering

    raise Exception("STOPPING AFTER DECONTAMINATION")

    if filtered_reads != trimmed_reads:
        kraken_input = {}
        kraken_input["input_fastq"] = filtered_reads
        kraken_input["prefix"] = "after_cleanup_"
        kraken_input["kraken_db"] = karaken_db_on_disk_location
        KrakenBracken("after_cleanup_kraken", base_root).run(kraken_input)

    # run assembly phase

    assembled_contigs = {}
    for directory in input_data_directories:
        root = output_directories[directory]
        assembler_inputs = filtered_reads[directory]
        assembled_contigs[directory] = RunAssemblers("run_assemblers", root).run(assembler_inputs)
    

    # run prokka on all assembler outputs

    # output:
    # -- directory
    # -- -- tool
    # -- -- -- output_dict

    reorder_annotate_output = {}
    for directory in input_data_directories:
        root = output_directories[directory]
        outputs = {}
        for tool, contig in assembled_contigs[directory].items():
            if tool not in ["root", "root_id"]:
                try:
                    reference = get_reference(sample_identifiers[directory], path_to_reference_table, path_to_reference_location)
                except:
                    reference = None
                reorder_annotate_args = {} 
                reorder_annotate_args["contig"] = contig
                reorder_annotate_args["reference"] = reference
                if reference != None:
                    outputs[tool] = ReorderAndAnnotate(tool + "_reorder_annotate", root).run(reorder_annotate_args)
                else:
                    outputs[tool] = None
        reorder_annotate_output[directory] = outputs


    print("INFO: Tadaaa! Now have fun understanding the output")

    