import numpy as np
from WGALP.simulations.fastq import FASTQ
from tqdm import tqdm

def str_take(s, a, b):
    assert a<=b, "Invalid slice: " + str(a) + " " + str(b)
    if a > len(s):
        return s[a-len(s):b-len(s)]
    elif b < len(s):
        return s[a:b]
    else:
        return s[a:len(s)-1] + s[0:b-len(s)]

class FASTA():

    def __init__(self):
        """
        initialize an empty fasta file
        """
        self.sequences = []
        self.descriptions = []
        self.full_sequencce = ""

    def read(self, path):
        """
        read a fasta file from disk, and load it into this object
        """
        f = open(path, "r")
        current_sequence = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                self.sequences += [current_sequence]
                current_sequence = ""
                self.descriptions += [line]
            else:
                current_sequence += line
        self.sequences += [current_sequence]
        self.full_sequencce = "".join(self.sequences)
        f.close()

    def global_sample(self, n, mean_read_length, sd_read_length, mean_quality, sd_quality, PE_distance_mean, PE_distance_sd,  annotation = "SIMULATED_READ"):
        """
        
        """

        read_lengths = [ round(max(x,1)) for x in np.random.normal(mean_read_length, sd_read_length, n)]
        rev_read_lengths = [ round(max(x,1)) for x in np.random.normal(mean_read_length, sd_read_length, n)]
        distances = [ round(max(x,1)) for x in np.random.normal(PE_distance_mean, PE_distance_sd, n)]

        out_fastq_fwd = FASTQ()
        out_fastq_rev = FASTQ()

        # for each read
        for i in tqdm(range(n)):
            qual_fwd = [ round(max(x,0)) for x in np.random.normal(mean_quality, sd_quality, read_lengths[i])] 
            qual_rev = [ round(max(x,0)) for x in np.random.normal(mean_quality, sd_quality, rev_read_lengths[i])] 
            seq = self.extract_sequence(read_lengths[i], rev_read_lengths[i], distances[i])
            out_fastq_fwd.add(annotation + ":" + str(i) + "/1", seq[0], qual_fwd)
            out_fastq_rev.add(annotation + ":" + str(i) + "/2", seq[1], qual_rev)

        return(out_fastq_fwd, out_fastq_rev)


    def extract_sequence(self, fwd_len, rev_len, dist):
        p1 = np.random.randint(0,len(self.full_sequencce) - 1)

        fwd = str_take(self.full_sequencce, p1, p1+fwd_len )
        rev = str_take(self.full_sequencce, p1+dist, p1+dist+rev_len)

        return (fwd, rev)





if __name__ == "__main__":

    reference = FASTA()
    reference.read("/home/redsnic/WGA_batteri/simulation_references/rhamnosus_reference_96_149_165_196.fasta")
    out = reference.global_sample(1000000, 100, 1, 25, 1, 500, 5)

    print(str(out[0]))

    print("=======================================================")
    print("=======================================================")
    print("=======================================================")

    print(str(out[1]))


            


    
            

    

        

            