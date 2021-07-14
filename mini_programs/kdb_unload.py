#!/usr/bin/env python3

# --- imports

import sys
import subprocess
from WGALP.utils.input_manager import InputManager
from WGALP.utils.input_manager import check_folders

# --- input arguments

def prepare_input(args):
    input_data = InputManager(program_description="Unload kraken-db from RAM\nThis command requires root privileges.")
    input_data.add_arg("--mount-point", "path", description="path where the kraken_db was mounted")
    input_data.parse(args)
    return input_data


# --- input sanity checks

def sanity_check(mount_point):
    check_folders([mount_point])

# --- core functions

def kdb_unload_aux(mount_point):
    # sanity check
    sanity_check(mount_point)
    subprocess.run("umount " + mount_point, shell=True, check=True, executable="/bin/bash")

# --- caller function

def kdb_unload(args):

    in_manager = prepare_input(args)

    mount_point = in_manager["--mount-point"]["value"]

    kdb_unload_aux(mount_point)
    
    print("task completed successfully")
    print("Kraken2 database unloaded")


if __name__ == "__main__":
    kdb_unload(sys.argv[1:])    


    