from WGALP.workflow import Workflow

from WGALP.blocks.SPAdes import SPAdes
from WGALP.blocks.minia import minia
# and others when possible

class RunAssemblers(Workflow):
    
    def task(self, args_dict):
        
        fastq_fwd = args_dict["fastq_fwd"]
        fastq_rev = args_dict["fastq_rev"]

        root = self.root
        out_dict = {}
        # SPAdes
        step = SPAdes("SPAdes", root, fastq_fwd=fastq_fwd, fastq_rev=fastq_rev)
        out_dict["SPAdes"] = step["contigs"]
        step = SPAdes("SPAdes_plasmid", root, fastq_fwd=fastq_fwd, fastq_rev=fastq_rev, plasmid=True)  
        out_dict["SPAdes_plasmid"] = step["contigs"]
        # minia
        for kmer_size in [31,61,91,121]: 
            try:
                step = minia("minia_" + str(kmer_size), root, kmer_size, fastq_fwd, fastq_rev=fastq_rev)
                out_dict["minia_" + str(kmer_size)] = step["contigs"]
            except:
                pass
        

        return out_dict



