from WGALP.workflow import Workflow

from WGALP.blocks.kraken import kraken
from WGALP.blocks.bracken import bracken
from WGALP.blocks.load_krakendb_ramdisk import load_krakendb_ramdisk
from WGALP.blocks.unload_krakendb_ramdisk import unload_krakendb_ramdisk

def run_kraken(rootpath, prefix, kraken_db, memory_mapped, fastq_fwd = None, fastq_rev = None):
    kraken_step = kraken(prefix + "kraken", rootpath, kraken_db, memory_mapped, fastq_fwd, fastq_rev)    
    bracken_step = bracken(prefix + "bracken", rootpath, kraken_step["kraken_report"], kraken_db)
    # cleanup
    kraken_step.delete_key("kraken_log") 
    bracken_step.delete_key("bracken_log")

class KrakenBracken(Workflow):
    
    def task(self, args_dict):
        
        # args_dict["prefix"] is the prefix of the output folder
        input_fastqs = args_dict["input_fastq"] # list of dictionaries with keys "fastq_fwd", "fastq_rev", "root" {available by default when using a workflow}
        karaken_db_on_disk_location = args_dict["kraken_db"]
        
        ramdisk_load_step = load_krakendb_ramdisk("kraken_ramdisk", self.root, karaken_db_on_disk_location, execution_mode="force")
        
        for _, fastq_PE in input_fastqs.items():
            root = fastq_PE["root"] 
            try:
                run_kraken(root, args_dict["prefix"], ramdisk_load_step["kraken_ram_db"], True, fastq_fwd = fastq_PE["fastq_fwd"], fastq_rev = fastq_PE["fastq_rev"]) 
            except Exception as excp:
                # unload ramdisk in case of errors
                ramdisk_unload_step = unload_krakendb_ramdisk("unload_ramdisk", root, ramdisk_load_step["kraken_ramdisk"], execution_mode = "force")
                ramdisk_unload_step.delete()
                ramdisk_load_step.delete()
                raise excp
        # unload ramdisk
        ramdisk_unload_step = unload_krakendb_ramdisk("unload_ramdisk", root, ramdisk_load_step["kraken_ramdisk"], execution_mode = "force")
        ramdisk_unload_step.delete()
        ramdisk_load_step.delete() 
        
        return {}