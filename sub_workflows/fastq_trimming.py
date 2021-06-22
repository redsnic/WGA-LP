from WGALP.workflow import Workflow

from WGALP.blocks.FastQC import FastQC
from WGALP.blocks.TrimmomaticPE import TrimmomaticPE

class TrimFastq(Workflow):
    
    def task(self, args_dict):
        
        fastq_fwd = args_dict["fastq_fwd"]
        fastq_rev = args_dict["fastq_rev"]
        trimmomatic_args = args_dict["trimmomatic_args"]
        # FastQC initial  
        FastQC("fastqc_raw_fwd", self.root, fastq_fwd)
        FastQC("fastqc_raw_rev", self.root, fastq_rev)
        # TrimmomaticPE
        trimming_step = TrimmomaticPE("TrimmomaticPE", self.root, fastq_fwd, fastq_rev, execution_mode="on_demand", trimmomatic_args=trimmomatic_args)
        # FastQC
        FastQC("fastqc_trimmed_fwd", self.root, trimming_step["trimmed_fwd"])
        FastQC("fastqc_trimmed_rev", self.root, trimming_step["trimmed_rev"])
        
        # cleanup -- remove discarded read files --
        trimming_step.delete_key("discarded_fwd")
        trimming_step.delete_key("discarded_rev")

        # return 
        return trimming_step.get_files()