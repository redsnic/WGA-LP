from WGALP.workflow import Workflow

from WGALP.blocks.BWA import BWA
from WGALP.blocks.samtools_VSI import samtools_VSI
from WGALP.blocks.bazam import bazam
from WGALP.blocks.fastq_bam_difference import fastq_bam_difference

def remove_contaminant(rootpath, reference, contaminant, fastq_fwd = None, fastq_rev = None):
    align_to_contaminant = BWA("contaminant_align", rootpath, contaminant, fastq1=fastq_fwd, fastq2=fastq_rev)
    extract_possibly_bad_reads = samtools_VSI("possibly_bad_reads", rootpath, align_to_contaminant["samfile"], view_flags="-F 4")
    return_to_fastq = bazam("bazam_possibly_bad_reads", rootpath, extract_possibly_bad_reads["bamfile"])
    remap_to_reference = BWA("ref_bad_align", rootpath, reference, fastq1=return_to_fastq["fastqfile"])
    extract_bad_reads = samtools_VSI("bad_reads", rootpath, remap_to_reference["samfile"], view_flags="-f 4", index=False)
    
    filter_bad_reads_fwd = fastq_bam_difference("remove_bad_reads_fwd", rootpath, fastq_fwd, extract_bad_reads["bamfile"])
    filter_bad_reads_rev = fastq_bam_difference("remove_bad_reads_rev", rootpath, fastq_rev, extract_bad_reads["bamfile"])

    # cleanup 
    align_to_contaminant.delete()
    extract_possibly_bad_reads.delete()
    return_to_fastq.delete()
    remap_to_reference.delete()
    extract_bad_reads.delete()

    return { "fastq_fwd" : filter_bad_reads_fwd["filtered_fastq"],  "fastq_rev" : filter_bad_reads_rev["filtered_fastq"] }

class RemoveContaminant(Workflow):
    
    def task(self, args_dict):
        
        root = self.root
        try:
            reference = args_dict["reference"] 
            contaminant = args_dict["contaminant"] 
            fastq_fwd = args_dict["fastq_fwd"]
            fastq_rev = args_dict["fastq_rev"]

            # Run cleaning 
            filtered_fastqs = remove_contaminant(
                root,
                reference, 
                contaminant,
                fastq_fwd = fastq_fwd,
                fastq_rev = fastq_rev) 
        except:
            print("INFO: skipping decontamination for " + self.root)
            print("INFO: reference " + reference)
            filtered_fastqs = { "fastq_fwd" : fastq_fwd,  "fastq_rev" : fastq_rev }
        
        return filtered_fastqs


    