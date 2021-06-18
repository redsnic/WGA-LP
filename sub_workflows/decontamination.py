import os
from hashlib import md5 
from WGALP.workflow import Workflow

from WGALP.blocks.BWA import BWA
from WGALP.blocks.samtools_VSI import samtools_VSI
from WGALP.blocks.bazam import bazam
from WGALP.blocks.fastq_bam_difference import fastq_bam_difference

def smd5(s):
    return md5(s.encode()).hexdigest()


def decontamination(rootpath, references, contaminants, fastq):

    for contaminant in contaminants:
        suf = "_" + smd5(contaminant)
        align_to_contaminant = BWA("contaminant_align" + suf, rootpath, contaminant, fastq1=fastq)
        extract_possibly_bad_reads = samtools_VSI("possibly_bad_reads" + suf, rootpath, align_to_contaminant["samfile"], view_flags="-F 4")
        return_to_fastq = bazam("bazam_possibly_bad_reads" + suf, rootpath, extract_possibly_bad_reads["bamfile"])

        for reference in references:
            suf = "_" + smd5(contaminant) + "_" + smd5(reference)
            remap_to_reference = BWA("ref_bad_align" + suf, rootpath, reference, fastq1=return_to_fastq["fastqfile"])
            extract_bad_reads = samtools_VSI("bad_reads" + suf, rootpath, remap_to_reference["samfile"], view_flags="-f 4", index=False)
            filter_bad_reads = fastq_bam_difference("remove_bad_reads" + suf, rootpath, fastq, extract_bad_reads["bamfile"])
            # put results in rootpath
            os.rename(filter_bad_reads["filtered_fastq"], os.path.join(rootpath, os.path.basename(fastq)))
            # cleanup
            remap_to_reference.delete()
            extract_bad_reads.delete()
            filter_bad_reads.delete()
            # return
            fastq = os.path.join(rootpath, os.path.basename(fastq))

        # cleanup
        align_to_contaminant.delete()
        extract_possibly_bad_reads.delete()
        return_to_fastq.delete()

    return { "cleaned_fastq" : fastq }

#
def decontaminationPE_alt(rootpath, references, contaminants, fastq_fwd, fastq_rev):
    """
    alternative version of decontaminationPE that maps only once to the references
    """
    first_run = True
    bad_reads_sets = []
    last_fastq = None
    for contaminant in contaminants:
        suf = "_" + smd5(contaminant)
        if first_run:
            align_to_contaminant = BWA("contaminant_align" + suf, rootpath, contaminant, fastq1=fastq_fwd, fastq2=fastq_rev)
            first_run = False
        else:
            align_to_contaminant = BWA("contaminant_align" + suf, rootpath, contaminant, fastq1=last_fastq)
        extract_possibly_bad_reads = samtools_VSI("possibly_bad_reads" + suf, rootpath, align_to_contaminant["samfile"], view_flags="-F 4")
        return_to_fastq = bazam("bazam_possibly_bad_reads" + suf, rootpath, extract_possibly_bad_reads["bamfile"])
        bad_reads_sets.append(return_to_fastq["fastqfile"])
        last_fastq = return_to_fastq["fastqfile"]
        # return
        fastq_fwd = os.path.join(rootpath, os.path.basename(fastq_fwd))
        fastq_rev = os.path.join(rootpath, os.path.basename(fastq_rev))

        # cleanup
        align_to_contaminant.delete()
        extract_possibly_bad_reads.delete()
        return_to_fastq.delete()


    merge_possibly_bad_reads_fastq =  merge_fastq[]

    for reference in references:
        suf = "_" + "_" + smd5(reference)
        remap_to_reference = BWA("ref_bad_align" + suf, rootpath, reference, fastq1=contaminant_mapping_read["fastqfile"])
        extract_bad_reads = samtools_VSI("bad_reads" + suf, rootpath, remap_to_reference["samfile"], view_flags="-f 4", index=False)
        filter_bad_reads_fwd = fastq_bam_difference("remove_bad_reads_fwd" + suf, rootpath, fastq_fwd, extract_bad_reads["bamfile"])
        filter_bad_reads_rev = fastq_bam_difference("remove_bad_reads_rev" + suf, rootpath, fastq_rev, extract_bad_reads["bamfile"])
        # put results in rootpath
        os.rename(filter_bad_reads_fwd["filtered_fastq"], os.path.join(rootpath, os.path.basename(fastq_fwd)))
        os.rename(filter_bad_reads_rev["filtered_fastq"], os.path.join(rootpath, os.path.basename(fastq_rev)))
        # cleanup
        remap_to_reference.delete()
        extract_bad_reads.delete()
        filter_bad_reads_fwd.delete()
        filter_bad_reads_rev.delete()
        # return
        fastq_fwd = os.path.join(rootpath, os.path.basename(fastq_fwd))
        fastq_rev = os.path.join(rootpath, os.path.basename(fastq_rev))

        # cleanup
        align_to_contaminant.delete()
        extract_possibly_bad_reads.delete()
        return_to_fastq.delete()

    return { "cleaned_fastq_fwd" : fastq_fwd, "cleaned_fastq_rev" : fastq_rev }

def decontaminationPE(rootpath, references, contaminants, fastq_fwd, fastq_rev):

    for contaminant in contaminants:
        suf = "_" + smd5(contaminant)
        align_to_contaminant = BWA("contaminant_align" + suf, rootpath, contaminant, fastq1=fastq_fwd, fastq2=fastq_rev)
        extract_possibly_bad_reads = samtools_VSI("possibly_bad_reads" + suf, rootpath, align_to_contaminant["samfile"], view_flags="-F 4")
        return_to_fastq = bazam("bazam_possibly_bad_reads" + suf, rootpath, extract_possibly_bad_reads["bamfile"])

        for reference in references:
            suf = "_" + smd5(contaminant) + "_" + smd5(reference)
            remap_to_reference = BWA("ref_bad_align" + suf, rootpath, reference, fastq1=return_to_fastq["fastqfile"])
            extract_bad_reads = samtools_VSI("bad_reads" + suf, rootpath, remap_to_reference["samfile"], view_flags="-f 4", index=False)
            filter_bad_reads_fwd = fastq_bam_difference("remove_bad_reads_fwd" + suf, rootpath, fastq_fwd, extract_bad_reads["bamfile"])
            filter_bad_reads_rev = fastq_bam_difference("remove_bad_reads_rev" + suf, rootpath, fastq_rev, extract_bad_reads["bamfile"])
            # put results in rootpath
            os.rename(filter_bad_reads_fwd["filtered_fastq"], os.path.join(rootpath, os.path.basename(fastq_fwd)))
            os.rename(filter_bad_reads_rev["filtered_fastq"], os.path.join(rootpath, os.path.basename(fastq_rev)))
            # cleanup
            remap_to_reference.delete()
            extract_bad_reads.delete()
            filter_bad_reads_fwd.delete()
            filter_bad_reads_rev.delete()
            # return
            fastq_fwd = os.path.join(rootpath, os.path.basename(fastq_fwd))
            fastq_rev = os.path.join(rootpath, os.path.basename(fastq_rev))

        # cleanup
        align_to_contaminant.delete()
        extract_possibly_bad_reads.delete()
        return_to_fastq.delete()

    return { "cleaned_fastq_fwd" : fastq_fwd, "cleaned_fastq_rev" : fastq_rev }

class Decontamination(Workflow):
    
    def task(self, args_dict):
        
        root = self.root
        
        references = args_dict["references"] 
        contaminants = args_dict["contaminants"] 

        try:
            # Non PE
            fastq = args_dict["fastq"]

            # Run cleaning 
            filtered_fastqs = decontamination(
                root,
                references, 
                contaminants,
                fastq)  
        except KeyError:
            # PE
            fastq_fwd = args_dict["fastq_fwd"]
            fastq_rev = args_dict["fastq_rev"]

            filtered_fastqs = decontaminationPE(
                root,
                references, 
                contaminants,
                fastq_fwd,
                fastq_rev)  

        return filtered_fastqs


    