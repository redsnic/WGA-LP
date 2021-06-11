import sys
import os
from WGALP.utils.input_manager import InputManager
from sub_workflows.decontamination import Decontamination
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders


def prepare_input(args):
    input_data = InputManager(program_description="Remove reads that map to a contaminant reference, but not to a target reference" + "\n" + "references must be in .fasta format and BWA indexed (command: bwa index path/to/file.fasta)")
    input_data.add_arg("--fastq", "path", description="single raw read file to be cleaned (.fastq) [use only with NON paired end data]")
    input_data.add_arg("--fastq-fwd", "path", description="forward raw reads (.fastq) [use only with paired end data]")
    input_data.add_arg("--fastq-rev", "path", description="revese raw reads (.fastq) [use only with paired end data]")
    input_data.add_arg("--references", "list", description="list of the possible references for the sequenced genome (.fasta, BWA indexed)")
    input_data.add_arg("--contaminants", "list", description="list of the contaminant")
    input_data.add_arg("--output", "dir", description="the folder in which the output will be saved")
    input_data.parse(args)
    return input_data

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
    out = dec.run(args)
    dec.delete_checkpoint()
    return out

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
    out = dec.run(args)
    dec.delete_checkpoint()
    return out

if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

    fastq = in_manager["--fastq"]["value"]
    fastq_fwd = in_manager["--fastq-fwd"]["value"]
    fastq_rev = in_manager["--fastq-rev"]["value"]
    references = in_manager["--references"]["value"]
    contaminants = in_manager["--contaminants"]["value"]
    output_dir = in_manager["--output"]["value"]

    if fastq is not None and (fastq_fwd is not None and fastq_rev is not None):
        raise Exception("Choose either PE [--fastq-rev and --fastq-fwd] or non PE [--fastq] mode, use --help for more information")

    if fastq is None and not (fastq_fwd is not None and fastq_rev is not None):
        raise Exception("For PE mode both fwd and rev fastq files must be specified, use --help for more information")
    
    
    if fastq is None:
        output = run_decontaminationPE(fastq_fwd, fastq_rev, references, contaminants, output_dir)
        print("task completed successfully")
        print("decontaminated reads are at the following locations:")
        print("\t" + "cleaned_fastq_fwd" + " : " + output["cleaned_fastq_fwd"])
        print("\t" + "cleaned_fastq_rev" + " : " + output["cleaned_fastq_rev"])
    else:
        output = run_decontamination(fastq, references, contaminants, output_dir)
        print("task completed successfully")
        print("decontaminated reads are at the following locations:")
        print("\t" + "cleaned_fastq" + " : " + output["cleaned_fastq"])

    