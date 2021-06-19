from WGALP.utils.genericUtils import binary_search


def make_read_set(fastq_files, output_path):
    """
    create a non redundant set of the reads IDs from a set of fastq files 
    """
    IDs = []
    
    for f_path in fastq_files:
        f = open(f_path,"r")
        line_count = 0
        for line in f:
            if line_count % 4 == 0:
                IDs.append(line.split()[0][1:])
            line_count +=1
        f.close()
    IDs = list(set(IDs))
    outf = open(output_path, "w")
    outf.writelines("\n".join(IDs))
    outf.close()

def filter_fastq_reads( fastq_file_path, selected_reads, out_file_name, keep=False):
    """
    Filter unwanted reads from a fastq files
    selected_reads should point to a file with a newline separated list of read IDs
    :param fastq_file_path: path to a fastq_file
    :param selected_reads: path to the file with the IDs of the read to selsct
    :param out_file_name: name of the .fastq file created after this filtering
    :param keep: True if the selected reads
    """

    # open input files
    fastq_file = open(fastq_file_path, "r")
    bad_reads_file = open(selected_reads, "r")

    # read bad_reads and sort them
    bad_reads = bad_reads_file.read().split()
    bad_reads.sort()

    out_file = open(out_file_name, "w")

    line_count = 0
    to_be_printed = False
    for line in fastq_file:
        if(line_count == 0):
            # check if read ID is in the bad list
            read_id = line.split()[0][1:]
            if binary_search(bad_reads, read_id) is not None:
                to_be_printed = keep
            else:
                to_be_printed = not keep
        if(to_be_printed):
            # if it is not, print the read
            out_file.write(line)
        line_count += 1
        if(line_count == 4):
            line_count = 0
            to_be_printed = False

    fastq_file.close()
    bad_reads_file.close()
    out_file.close()
        
    










    
