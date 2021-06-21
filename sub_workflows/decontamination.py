import os
from hashlib import md5 
from WGALP.workflow import Workflow

from WGALP.blocks.BWA import BWA
from WGALP.blocks.samtools_VSI import samtools_VSI
from WGALP.blocks.bazam import bazam
from WGALP.blocks.fastq_bam_difference import fastq_bam_difference

from WGALP.tools.filter_fastq import filter_fastq_reads 
from WGALP.tools.filter_fastq import make_read_set

def smd5(s):
    return md5(s.encode()).hexdigest()

def decontamination(rootpath, references, contaminants, fastq):

    bad_reads_sets = []
    # garbage collection stores possibly bad fastq steps to allow further cleanup
    garbage_collection = []
    for contaminant in contaminants:
        # create bad read sets
        suf = "_" + smd5(contaminant)
        align_to_contaminant = BWA("contaminant_align" + suf, rootpath, contaminant, fastq1=fastq)
        extract_possibly_bad_reads = samtools_VSI("possibly_bad_reads" + suf, rootpath, align_to_contaminant["samfile"], view_flags="-F 4")
        return_to_fastq = bazam("bazam_possibly_bad_reads" + suf, rootpath, extract_possibly_bad_reads["bamfile"])
        bad_reads_sets.append(return_to_fastq["fastqfile"])
        garbage_collection.append(return_to_fastq)

        # cleanup
        align_to_contaminant.delete()
        extract_possibly_bad_reads.delete()
        return_to_fastq.delete_non_output_files()

    # merge the bad sets
    merged_possibly_bad_reads = os.path.join(rootpath, "possibly_bad_ids.txt")
    make_read_set(bad_reads_sets, merged_possibly_bad_reads)

    # clean possibly bad fastqs
    for rtfq in garbage_collection:
        rtfq.delete()

    pb_fastq = os.path.join(rootpath, "possibly_bad.fastq")

    filter_fastq_reads(fastq, merged_possibly_bad_reads, pb_fastq, keep=True)

    for reference in references:
        # refine bad read set
        suf = "_" + "_" + smd5(reference)
        remap_to_reference = BWA("ref_bad_align" + suf, rootpath, reference, fastq1=pb_fastq)
        extract_good_reads = samtools_VSI("bad_reads" + suf, rootpath, remap_to_reference["samfile"], view_flags="-F 4", index=False)
        filter_bad_reads = fastq_bam_difference("remove_good_reads_fwd" + suf, rootpath, pb_fastq, extract_good_reads["bamfile"])
        # put results in rootpath
        os.rename(filter_bad_reads["filtered_fastq"], os.path.join(rootpath, "discarded_reads.fastq"))
        # cleanup
        remap_to_reference.delete()
        extract_good_reads.delete()
        filter_bad_reads.delete()
        # update
        pb_fastq = os.path.join(rootpath, os.path.basename(fastq))

    # final read filtering
    out_fastq = os.path.join(rootpath, "decontaminated.fastq")
    read_set_bad = os.path.join(rootpath, "bad.txt")
    make_read_set([pb_fastq], read_set_bad)
    filter_fastq_reads(fastq, read_set_bad, out_fastq)
    # further cleanup
    os.remove(os.path.join(rootpath, "possibly_bad.fastq"))
    os.remove(os.path.join(rootpath, "bad.txt"))
    os.remove(os.path.join(rootpath, "possibly_bad_ids.txt"))

    return { "cleaned_fastq" : out_fastq }

#
def decontaminationPE(rootpath, references, contaminants, fastq_fwd, fastq_rev):
    """
    alternative version of decontaminationPE that maps only once to the references
    """

    bad_reads_sets = []
    # garbage collection stores possibly bad fastq steps to allow further cleanup
    garbage_collection = []
    for contaminant in contaminants:
        # create bad read sets
        suf = "_" + smd5(contaminant)
        align_to_contaminant = BWA("contaminant_align" + suf, rootpath, contaminant, fastq1=fastq_fwd, fastq2=fastq_rev)
        extract_possibly_bad_reads = samtools_VSI("possibly_bad_reads" + suf, rootpath, align_to_contaminant["samfile"], view_flags="-F 4")
        return_to_fastq = bazam("bazam_possibly_bad_reads" + suf, rootpath, extract_possibly_bad_reads["bamfile"])
        bad_reads_sets.append(return_to_fastq["fastqfile"])
        garbage_collection.append(return_to_fastq)

        # cleanup
        align_to_contaminant.delete()
        extract_possibly_bad_reads.delete()
        return_to_fastq.delete_non_output_files()

    # merge the bad sets
    merged_possibly_bad_reads = os.path.join(rootpath, "possibly_bad_ids.txt")
    make_read_set(bad_reads_sets, merged_possibly_bad_reads)

    # clean possibly bad fastqs
    for rtfq in garbage_collection:
        rtfq.delete()

    pb_fastq_1 = os.path.join(rootpath, "possibly_bad_fwd.fastq")
    pb_fastq_2 = os.path.join(rootpath, "possibly_bad_rev.fastq")

    filter_fastq_reads(fastq_fwd, merged_possibly_bad_reads, pb_fastq_1, keep=True)
    filter_fastq_reads(fastq_rev, merged_possibly_bad_reads, pb_fastq_2, keep=True)

    for reference in references:
        # refine bad read set
        suf = "_" + "_" + smd5(reference)
        remap_to_reference = BWA("ref_bad_align" + suf, rootpath, reference, fastq1=pb_fastq_1, fastq2=pb_fastq_2)
        extract_good_reads = samtools_VSI("bad_reads" + suf, rootpath, remap_to_reference["samfile"], view_flags="-F 4", index=False)
        filter_bad_reads_fwd = fastq_bam_difference("remove_good_reads_fwd" + suf, rootpath, pb_fastq_1, extract_good_reads["bamfile"])
        filter_bad_reads_rev = fastq_bam_difference("remove_good_reads_rev" + suf, rootpath, pb_fastq_2, extract_good_reads["bamfile"])
        # put results in rootpath and update links
        pb_fastq_1 = os.path.join(rootpath, "discarded_reads_fwd.fastq")
        pb_fastq_2 = os.path.join(rootpath, "discarded_reads_rev.fastq")
        os.rename(filter_bad_reads_fwd["filtered_fastq"], pb_fastq_1)
        os.rename(filter_bad_reads_rev["filtered_fastq"], pb_fastq_2)
        # cleanup
        remap_to_reference.delete()
        extract_good_reads.delete()
        filter_bad_reads_fwd.delete()
        filter_bad_reads_rev.delete()

    # final read filtering
    out_fastq_fwd = os.path.join(rootpath, "decontaminated_fwd.fastq")
    out_fastq_rev = os.path.join(rootpath, "decontaminated_rev.fastq")
    read_set_bad_fwd = os.path.join(rootpath, "bad_fwd.txt")
    read_set_bad_rev = os.path.join(rootpath, "bad_rev.txt")
    make_read_set([pb_fastq_1], read_set_bad_fwd)
    make_read_set([pb_fastq_2], read_set_bad_rev)
    filter_fastq_reads(fastq_fwd, read_set_bad_fwd, out_fastq_fwd)
    filter_fastq_reads(fastq_rev, read_set_bad_rev, out_fastq_rev)
    # further cleanup
    os.remove(os.path.join(rootpath, "possibly_bad_fwd.fastq"))
    os.remove(os.path.join(rootpath, "possibly_bad_rev.fastq"))
    os.remove(os.path.join(rootpath, "possibly_bad_ids.txt"))
    os.remove(os.path.join(rootpath, "bad_fwd.txt"))
    os.remove(os.path.join(rootpath, "bad_rev.txt"))

    return { "cleaned_fastq_fwd" : out_fastq_fwd, "cleaned_fastq_rev" : out_fastq_rev }


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


    