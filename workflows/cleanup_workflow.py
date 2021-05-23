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
from WGALP.blocks.FastQC import FastQC
from WGALP.blocks.TrimmomaticPE import TrimmomaticPE
from WGALP.blocks.kraken import kraken
from WGALP.blocks.bracken import bracken
from WGALP.blocks.BWA import BWA
from WGALP.blocks.samtools_VSI import samtools_VSI
from WGALP.blocks.bazam import bazam
from WGALP.blocks.fastq_bam_difference import fastq_bam_difference
from WGALP.blocks.load_krakendb_ramdisk import load_krakendb_ramdisk
from WGALP.blocks.unload_krakendb_ramdisk import unload_krakendb_ramdisk
from WGALP.blocks.SPAdes import SPAdes
from WGALP.blocks.minia import minia
from WGALP.blocks.prokka import prokka

# Requirements:
# ~ 1 GB per genome of disk space, ~ 9 GB RAM



def run_fastq_cleanup(rootpath, fastq_fwd = None, fastq_rev = None):
    # FastQC initial  
    FastQC("fastqc_raw_fwd", rootpath, fastq_fwd)
    FastQC("fastqc_raw_rev", rootpath, fastq_rev)
    # TrimmomaticPE
    trimming_step = TrimmomaticPE("TrimmomaticPE", rootpath, fastq_fwd, fastq_rev, execution_mode="on_demand")
    # FastQC
    FastQC("fastqc_trimmed_fwd", rootpath, trimming_step["trimmed_fwd"])
    FastQC("fastqc_trimmed_rev", rootpath, trimming_step["trimmed_rev"])
    
    # cleanup -- remove discarded read files --
    trimming_step.delete_key("discarded_fwd")
    trimming_step.delete_key("discarded_rev")

    # return 
    return {
        "reads" : (trimming_step["trimmed_fwd"], trimming_step["trimmed_rev"]),
        "trimming_step" :  trimming_step 
    }

def run_kraken(rootpath, prefix, kraken_db, memory_mapped, fastq_fwd = None, fastq_rev = None):
    kraken_step = kraken(prefix + "kraken", rootpath, kraken_db, memory_mapped, fastq_fwd, fastq_rev)    
    bracken_step = bracken(prefix + "bracken", rootpath, kraken_step["kraken_report"], kraken_db)
    # cleanup
    kraken_step.delete_key("kraken_log") 
    bracken_step.delete_key("bracken_log")


def remove_contaminant(rootpath, reference, contaminant, fastq_fwd = None, fastq_rev = None):
    align_to_contaminant = BWA("contaminant_align", rootpath, contaminant, fastq1=fastq_fwd, fastq2=fastq_rev)
    extract_possibly_bad_reads = samtools_VSI("possibly_bad_reads", rootpath, align_to_contaminant["samfile"], view_flags="-F 4")
    return_to_fastq = bazam("bazam_possibly_bad_reads", rootpath, extract_possibly_bad_reads["bamfile"])
    remap_to_reference = BWA("ref_bad_align", rootpath, reference, fastq1=return_to_fastq["fastqfile"])
    extract_bad_reads = samtools_VSI("bad_reads", rootpath, remap_to_reference["samfile"], view_flags="-f 4", index=False)
    
    filter_bad_reads_fwd = fastq_bam_difference("remove_bad_reads_fwd", rootpath, fastq_fwd, extract_bad_reads["bamfile"])
    filter_bad_reads_rev = fastq_bam_difference("remove_bad_reads_rev", rootpath, fastq_rev, extract_bad_reads["bamfile"])

    # cleanup 
    align_to_contaminant.delete()
    extract_possibly_bad_reads.delete()
    return_to_fastq.delete()
    remap_to_reference.delete()
    extract_bad_reads.delete()

    return (filter_bad_reads_fwd["filtered_fastq"], filter_bad_reads_rev["filtered_fastq"])


def load_fastq_files(directory):
    files = os.listdir(directory)

    if len(files) != 2:
        print("ERROR: input directories must contain forwad and reverse reads only")
        print("INFO: the files should match the following regular expressions")
        print("INFO: *_R1_*.fastq and *_R2_*.fastq respectively")

    out = {}
    for f in files:
        if re.match(r".*_R1_.*\.fastq", f):
            out["raw_reads_fwd"] = os.path.join(directory, f)
        elif re.match(r".*_R2_.*\.fastq", f):
            out["raw_reads_rev"] = os.path.join(directory, f)
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

def check_execution(step_id, base_path, identifier):
    return os.path.isdir(os.path.join(base_path, identifier, step_id))

def check_execution_all(step_id, base_path, dir_names, identifiers):
    return all(check_execution(step_id, base_path, identifiers[dir_name]) for dir_name in dir_names)
    
if __name__ == "__main__":

    # usage: python3 workflow.py outputdir reference_table reference_location_table input_dir1 input_dir2 ...
    in_manager = prepare_input(sys.argv[1:])
    
    # base_root = "/home/redsnic/WGA_batteri/PythonWorkflow/test_dir/" 
    base_root = in_manager["--output"]["value"]
    path_to_reference_table = in_manager["--ref-table"]["value"]
    path_to_reference_location = in_manager["--ref-location-table"]["value"]
    input_data_directories = in_manager["--input"]["value"]

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

    
    status = {} # this dictionary will keep track of the operations 
    identifiers = {} # this dictionary will help in translating directories to task identifiers 
    for directory in input_data_directories:
        if not os.path.isdir(directory):
            print("ERROR: invalid input directory " + directory)
            raise FileNotFoundError
        identifier = os.path.basename(directory)
        status[directory] = load_fastq_files(directory)
        identifiers[directory] = identifier

    karaken_db_on_disk_location = in_manager["--kraken-db"]["value"]
    
    # Main Execution
    
    # --- FastQC/Trimming loop

    
    for directory in input_data_directories:
        # execution folder
        root = os.path.join(base_root, identifiers[directory]) 
        if not os.path.isdir(root):
            os.mkdir(root)  
        # checkpoint
        checkpoint = load_checkpoint(root, "fastq_cleanup.pickle")
        if checkpoint == None:
            # input
            raw_fastq_fwd = status[directory]["raw_reads_fwd"]
            raw_fastq_rev = status[directory]["raw_reads_rev"]
            # get trimmed reads
            status[directory] = run_fastq_cleanup(root, fastq_fwd = raw_fastq_fwd, fastq_rev = raw_fastq_rev)
            make_checkpoint(root, "fastq_cleanup.pickle", status[directory])
        else:
            print("INFO: loaded previous checkpoint for fastq_cleanup: " + identifiers[directory])
            status[directory] = checkpoint

    # --- run kraken before cleanup

    # load ramdisk  

    print(check_execution_all("before_cleanup_kraken", base_root, input_data_directories, identifiers))
    if not check_execution_all("before_cleanup_kraken", base_root, input_data_directories, identifiers):
        ramdisk_load_step = load_krakendb_ramdisk("kraken_ramdisk", base_root, karaken_db_on_disk_location, execution_mode="force")
        for directory in input_data_directories:
            root = os.path.join(base_root, identifiers[directory]) 
            try:
                run_kraken(root, "before_cleanup_", ramdisk_load_step["kraken_ram_db"], True, fastq_fwd = status[directory]["reads"][0], fastq_rev = status[directory]["reads"][1]) 
            except Exception as excp:
                ramdisk_unload_step = unload_krakendb_ramdisk("unload_ramdisk", root, ramdisk_load_step["kraken_ramdisk"], execution_mode = "force")
                ramdisk_unload_step.delete()
                ramdisk_load_step.delete()
                raise excp
        # unload ramdisk
        ramdisk_unload_step = unload_krakendb_ramdisk("unload_ramdisk", root, ramdisk_load_step["kraken_ramdisk"], execution_mode = "force")
        ramdisk_unload_step.delete()
        ramdisk_load_step.delete() 
    
    # --- run cleanup

    for directory in input_data_directories:
        root = os.path.join(base_root, identifiers[directory]) 
        checkpoint = load_checkpoint(root, "decontamination.pickle")
        if checkpoint == None:
            # Collect reference/contaminant data
            try:
                reference = get_reference(identifiers[directory], path_to_reference_table, path_to_reference_location) 
                contaminant = get_contaminant(path_to_reference_location, "Pediococcus_acidilactici") 
                
                # Run cleaning 
                filtered_fastqs = remove_contaminant(
                    root,
                    reference, 
                    contaminant,
                    fastq_fwd = status[directory]["reads"][0],
                    fastq_rev = status[directory]["reads"][1]) 
            except:
                print("INFO: skipping decontamination for " + directory)
                filtered_fastqs = (status[directory]["reads"][0], status[directory]["reads"][1])
            # cleanup 
            # status[directory]["trimming_step"].delete() 
            status[directory] = filtered_fastqs
            make_checkpoint(root, "decontamination.pickle", status[directory])
        else:
            print("INFO: loaded previous checkpoint for decontamination: " + identifiers[directory])
            status[directory] = checkpoint
    
    # --- run kraken after cleanup



    # load karaken ramdisk (again)
    if not check_execution_all("after_cleanup_kraken", base_root, input_data_directories, identifiers):
        ramdisk_load_step = load_krakendb_ramdisk("kraken_ramdisk", root, karaken_db_on_disk_location, execution_mode="force")
        
        for directory in input_data_directories:
            root = os.path.join(base_root, identifiers[directory]) 
            try:
                print("KRAKEN")
                print(status[directory][0])
                print(status[directory][1])
                run_kraken(root, "after_cleanup_", ramdisk_load_step["kraken_ram_db"], True, fastq_fwd = status[directory][0], fastq_rev = status[directory][1]) 
            except Exception as excp:
                ramdisk_unload_step = unload_krakendb_ramdisk("unload_ramdisk", root, ramdisk_load_step["kraken_ramdisk"], execution_mode = "force")
                ramdisk_unload_step.delete()
                ramdisk_load_step.delete()
                raise excp
        
        ramdisk_unload_step = unload_krakendb_ramdisk("unload_ramdisk", root, ramdisk_load_step["kraken_ramdisk"], execution_mode = "force")
        ramdisk_unload_step.delete()
        ramdisk_load_step.delete()

    # --- run genome assemblers

    assembler_status = {} 
    assembler_checkpoints = []

    # SPAdes
    for directory in input_data_directories:

        root = os.path.join(base_root, identifiers[directory]) 
        checkpoint = load_checkpoint(root, "SPAdes.pickle")
        if checkpoint == None:
            name = "SPAdes"
            step = SPAdes(name, root, fastq_fwd=status[directory][0], fastq_rev=status[directory][1])
            step.delete_non_output_files()
            step_plasmid = SPAdes(name + "_plasmid", root, fastq_fwd=status[directory][0], fastq_rev=status[directory][1], plasmid=True)    
            step_plasmid.delete_non_output_files()
            this_assembler_status = {}
            this_assembler_status[name] = step.outputs
            this_assembler_status[name + "_plasmid"] = step_plasmid.outputs
            make_checkpoint(root, "SPAdes.pickle", this_assembler_status)
            assembler_status = merge_two_dicts(assembler_status, this_assembler_status)
        else: 
            print("INFO: loaded previous checkpoint for SPAdes: " + identifiers[directory])
            assembler_status = merge_two_dicts(assembler_status, checkpoint.files)
        assembler_checkpoints.append("SPAdes.pickle")


    # TODO think!
    for directory in input_data_directories:
        root = os.path.join(base_root, identifiers[directory]) 
        checkpoint = load_checkpoint(root, "minia.pickle")
        kmer_size = 63
        if checkpoint == None:
            step = minia("minia_" + str(kmer_size), root, kmer_size, status[directory][0], fastq_rev=status[directory][1])
            this_assembler_status = { "minia_" + str(kmer_size) : step.outputs }
            make_checkpoint(root, "minia.pickle", this_assembler_status)
            assembler_status = merge_two_dicts(assembler_status, this_assembler_status)
        else: 
            print("INFO: loaded previous checkpoint for minia: " + identifiers[directory])
            assembler_status = merge_two_dicts(assembler_status, checkpoint.files)
        assembler_checkpoints.append("minia.pickle")

    print(assembler_checkpoints)

    for directory in input_data_directories:
        root = os.path.join(base_root, identifiers[directory])
        complete_status = {}
        for checkpoint in assembler_checkpoints:        
            sub_checkpoint = load_checkpoint(root, checkpoint)
            complete_status = merge_two_dicts(complete_status, sub_checkpoint.files)
        
        print(complete_status)
        for tool, outputs in complete_status.items():
            step = prokka(tool + "_prokka", root, os.path.join(root, tool, outputs["contigs"]))
            step.delete_non_output_files()

    print("INFO: Tadaaa! Now have fun understanding the output")

    