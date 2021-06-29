# DEPRECATED!

# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step


description = """
remove kraken2 database ramdisk
"""
input_description = """
mounting point of kraken2 database's ramsdisk
"""
output_description = """
No output
"""

### Wrapper
def unload_krakendb_ramdisk(name, rootpath, kraken_ramdisk, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(unload_krakendb_ramdisk_runner)
    step_args = {
        "kraken_ramdisk": kraken_ramdisk,
    }
    step.run(step_args)
    step.set_description(description, input_description, output_description)
    return step

### Runner
def unload_krakendb_ramdisk_runner(step, args):
    """
    unload the krakendb ramdisk
    [better to be run with "force"]
    The output folder of this step has no use and can be safely deleted
    input:
        kraken_ramdisk : path
    output:
        None
    """
    ramdisk_path = args["kraken_ramdisk"]

    command  = "sudo umount " + ramdisk_path

    # note that this command requies to be root (may prompt to get a password)
    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {}

    return step