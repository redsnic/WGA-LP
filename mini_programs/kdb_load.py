#!/usr/bin/env python3

# --- imports

import sys
import os
from WGALP.utils.input_manager import InputManager
from WGALP.blocks.load_krakendb_ramdisk import load_krakendb_ramdisk
from WGALP.utils.input_manager import check_folders

# --- input arguments

def prepare_input(args):
    input_data = InputManager(program_description="Load kraken-db into RAM, this step is useful when running kraken multiple times.\nRemember to unload the db after use and to use the --memory-mapped flag when supported (otherwise another copy of the db will be loaded).\nThis command requires root privileges.")
    input_data.add_arg("--db", "path", description="[Required] path to kraken database")
    input_data.add_arg("--mount-point", "text", description="[Required] path where the kraken_db will be mounted")
    input_data.parse(args)
    return input_data


# --- input sanity checks

def check_kraken_db(db):
    files = ["database200mers.kmer_distrib", "database150mers.kmer_distrib", "database100mers.kmer_distrib", "opts.k2d", "hash.k2d", "taxo.k2d", "seqid2taxid.map"]
    for f in files:
        if not os.path.isfile(os.path.join(db, f)):
            raise FileNotFoundError("No file " + f + " in kraken_db folder. Have you picked the right directory?")


def sanity_check(db, mount_point):
    # mode check
    check_folders([db])
    check_kraken_db(db)
    try:
        check_folders([mount_point])
    except Exception:
        if os.path.isfile(mount_point):
            raise Exception("--mount-point argument must be a directory and not a file")
        else:
            os.mkdir(mount_point)
    

# --- core functions

def kdb_load_aux(db, mount_point):
    # sanity check
    sanity_check(db, mount_point)
    # 
    out = load_krakendb_ramdisk("kraken_ramdisk", mount_point, db, execution_mode="force")
    return out

# --- caller function

def kdb_load(args):

    in_manager = prepare_input(args)

    db = in_manager["--db"]["value"]
    mount_point = in_manager["--mount-point"]["value"]

    output = kdb_load_aux(db, mount_point)
    
    print("task completed successfully")
    print("Kraken2 database loaded:")
    print("\t" + "database location (for --db arguments)" + " : " + output["kraken_ram_db"])
    print("\t" + "ramdisk location (for wgalp kdb-unload)" + " : " + output["kraken_ramdisk"])
    print("unload this ramdisk with the following command:")
    print("wgalp kdb-unload --mount-point " + output["kraken_ramdisk"])

    return output


if __name__ == "__main__":
    kdb_load(sys.argv[1:])    


    