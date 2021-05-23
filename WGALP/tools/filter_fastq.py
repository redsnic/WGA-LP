from bisect import bisect_left

def binary_search(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return None

def filter_fastq_reads( fastq_file_path, bad_reads_list_path, out_file_name):
    """
    Filter unwanted reads from a fastq files
    bad_reads_list_path should point to a file with a newline separated list of read IDs
    :param fastq_file_path: path to a fastq_file
    :param bad_reads_list_path: path to the file with the IDs of the bad reads 
    :param out_file_name: name of the .fastq file created after this filtering
    """

    # open input files
    fastq_file = open(fastq_file_path, "r")
    bad_reads_file = open(bad_reads_list_path, "r")

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
            if(binary_search(bad_reads, read_id)):
                to_be_printed = False
            else:
                to_be_printed = True
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
        
    










    
