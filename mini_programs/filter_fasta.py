from bisect import bisect_left
import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_files
from WGALP.utils.input_manager import check_folders

def binary_search(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return None

def filter_fasta( fasta_file_path, selected_contigs, out_file_name):
    """
    Filter unwanted reads from a fasta files
    selected_contigs should point to a file with a newline separated list of contig IDs
    :param fasta_file_path: path to a fasta_file
    :param selected_contigs: path to the file with the IDs of the selected contigs 
    :param out_file_name: name of the .fasta file created after this filtering
    """

    # open input files
    fasta_file = open(fasta_file_path, "r")
    selected_contigs_file = open(selected_contigs, "r")

    # read selected_contigs and sort them
    selected_contigs = selected_contigs_file.read().split()
    selected_contigs.sort()

    out_file = open(out_file_name, "w")

    to_be_printed = False
    for line in fasta_file:
        if line.startswith(">"):
            # check if read ID is in the bad list
            contig_id = line.split()[0][1:].strip()
            print(contig_id)
            if(binary_search(selected_contigs, contig_id)):
                to_be_printed = True
            else:
                to_be_printed = False
        if(to_be_printed):
            # if it is not, print the read
            out_file.write(line)

    fasta_file.close()
    selected_contigs_file.close()
    out_file.close()

    return out_file_name
        

def prepare_input(args):
    input_data = InputManager("Select only listed contigs from a Whole Genom Assembly")
    input_data.add_arg("--contigs", "path", description="assembled contigs or scaffolds (.fasta)")
    input_data.add_arg("--selected-contigs", "path", description="a file containing the ids of the selected contigs (each id is in its own line)")
    input_data.add_arg("--output", "dir", description="path to the output folder") 
    input_data.parse(args)
    return input_data

def sanity_check(output_dir, contigs, selected_contigs):
    check_files([contigs, selected_contigs])
    try:
        check_folders([output_dir])
    except Exception:
        if os.path.isfile(output_dir):
            raise Exception("--output argument must be a directory and not a file")
        else:
            os.mkdir(output_dir)


def reorder_contigs(output_dir, contigs, selected_contigs):
    # sanity check
    sanity_check(output_dir, contigs, selected_contigs)
    out = filter_fasta(contigs, selected_contigs, os.path.join(output_dir, "filtered_contigs.fasta") )
    return(out)
     
if __name__ == "__main__":
    
    in_manager = prepare_input(sys.argv[1:])

    contigs = in_manager["--contigs"]["value"]
    selected_contigs = in_manager["--selected-contigs"]["value"]
    output_dir = in_manager["--output"]["value"]
    
    output = reorder_contigs(output_dir, contigs, selected_contigs)

    print("task completed successfully")
    print("filtered .fasta is at the followinf location:")
    print("\t" + "filtered_fasta" + " : " + output)
    







    
