from WGALP.workflow import Workflow
from WGALP.blocks.BWA import BWA
from WGALP.blocks.samtools_VSI import samtools_VSI
from WGALP.blocks.recycler import recycler
from WGALP.blocks.bwa_index import bwa_index

# prepare the steps necessary to correctly run recycler

class Recycler(Workflow):
    
    def task(self, args_dict):
        
        fastq_fwd = args_dict["fastq_fwd"]
        fastq_rev = args_dict["fastq_rev"]
        contigs = args_dict["contigs"]
        assembly_graph = args_dict["assembly_graph"]
        kmer_length = args_dict["kmer_length"]

        # FastQC initial  
        bwa_index("bwa_index_recycler", self.root, contigs)
        out_bwa = BWA("bwa_realign_contigs", self.root, contigs, fastq1=fastq_fwd, fastq2=fastq_rev)
        out_vsi = samtools_VSI("vsi_realign_contigs", self.root, out_bwa["samfile"], index=True)
        out_bwa.delete()
        out_recycler = recycler("recycler", self.root, out_vsi["bamfile"], assembly_graph, kmer_length)
        out_vsi.delete()
        
        # return 
        return out_recycler.get_files()