import sys
import os
from WGALP.utils.input_manager import InputManager
from sub_workflows.decontamination import Decontamination



def prepare_input(args):
    input_data = InputManager()
    input_data.add_arg("--fastq", "path")
    input_data.add_arg("--fastq-fwd", "path")
    input_data.add_arg("--fastq-rev", "path")
    input_data.add_arg("--references", "list")
    input_data.add_arg("--contaminants", "list")
    input_data.add_arg("--output", "path")
    input_data.parse(args)
    return input_data


def check_files(file_list):
    for f in file_list:
        if not os.path.isfile(f):
            raise FileNotFoundError("File not found: " + f)

def check_folders(folder_list):
    for f in folder_list:
        if not os.path.isdir(f):
            raise FileNotFoundError("Directory not found: " + f)

def run_decontamination(fastq, references, contaminants, output_dir):
    # sanity check
    check_files([fastq])
    check_files(references)
    check_files(contaminants)
    check_folders([output_dir])
    # 
    fastq_basename = os.path.splitext(os.path.basename(fastq))[0]
    args = {
        "references" : references,
        "contaminants" : contaminants,
        "fastq" : fastq,
    }
    dec = Decontamination(fastq_basename, output_dir)
    dec.run(args)
    dec.delete_checkpoint()

def run_decontaminationPE(fastq_fwd, fastq_rev, references, contaminants, output_dir):
    # sanity check
    check_files([fastq_fwd])
    check_files([fastq_rev])
    check_files(references)
    check_files(contaminants)
    check_folders([output_dir])
    # 
    fastq_basename = os.path.splitext(os.path.basename(os.path.commonprefix([fastq_fwd, fastq_rev])))[0]
    args = {
        "references" : references,
        "contaminants" : contaminants,
        "fastq_fwd" : fastq_fwd,
        "fastq_rev" : fastq_rev
    }
    dec = Decontamination(fastq_basename, output_dir)
    dec.run(args)
    dec.delete_checkpoint()

if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

    fastq = in_manager["--fastq"]["value"]
    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    references = in_manager["--references"]["value"]
    contaminants = in_manager["--contaminants"]["value"]
    output_dir = in_manager["--output"]["value"]

    if fastq is not None and (fastq_fwd is not None and fastq_rev is not None):
        raise Exception("Choose either PE [--fastq-rev and --fastq-fwd] or non PE [--fastq] mode")

    if fastq is None and not (fastq_fwd is not None and fastq_rev is not None):
        raise Exception("For PE mode both fwd and rev fastq files must be specified")
    
    if fastq is None:
        run_decontaminationPE(fastq_fwd, fastq_rev, references, contaminants, output_dir)
    else:
        run_decontamination(fastq, references, contaminants, output_dir)