from WGALP.workflow import Workflow
from WGALP.blocks.BWA import BWA
from WGALP.blocks.samtools_VSI import samtools_VSI
from WGALP.blocks.samtools_depth import samtools_depth
from WGALP.blocks.bwa_index import bwa_index

# --- Run the steps necessary to extract coverage information from fastq and reference files

class ComputeCoverage(Workflow):
    
    def task(self, args_dict):
        
        fastq_fwd = args_dict["fastq_fwd"]
        fastq_rev = args_dict["fastq_rev"]
        contigs = args_dict["contigs"]

        # FastQC initial  
        bwa_index("bwa_index_recycler", self.root, contigs)
        out_bwa = BWA("bwa_realign_contigs_depth", self.root, contigs, fastq1=fastq_fwd, fastq2=fastq_rev)
        out_vsi = samtools_VSI("vsi_realign_contigs_depth", self.root, out_bwa["samfile"], index=False)
        out_bwa.delete()
        out_recycler = samtools_depth("samtools_depth", self.root, out_vsi["bamfile"])
        out_vsi.delete()
        
        # return 
        return out_recycler.get_files()