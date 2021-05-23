# --- default imports ---

# --- load utils ---
from WGALP.utils.commandLauncher import run_sp
from WGALP.step import Step

description = """
load kraken_db in a ramdisk
"""
input_description = """
...
"""
output_description = """
...
"""

### Wrapper
def load_krakendb_ramdisk(name, rootpath, kraken_db, execution_mode = "on_demand"):
    step = Step(name, rootpath, execution_mode=execution_mode)
    step.set_command(krakendb_make_ramdisk_runner)
    step_args = {
        "kraken_db": kraken_db,
    }
    step.run(step_args)
    step.set_description("load kraken_db in a ramdisk", "...", "...")
    return step

### Runner
def krakendb_make_ramdisk_runner(step, args):
    """
    load the krakendb into a ramdisk
    NOTE: this requires 8GB of free RAM, be careful not to forget the ramdisk loaded...
    [better to be run with "force"]
    input:
    {
        "kraken_db" (full path)
    }
    :param args: a dictionary of the arguments
    """
    db = args["kraken_db"]

    # this command works with minikraken db, change ramdisk size if needed...
    command  = "sudo mount -t tmpfs -o size=8G tmpfs " + step.outpath + " && "
    command += "cp -R " + db + " " + step.outpath + "/kraken_db"

    # note that this command requies to be root (may prompt to get a password)
    if step.execution_mode != "read":
        run_sp(step, command)

    # organize output

    step.outputs = {
        "kraken_ram_db" : "kraken_db", 
        "kraken_ramdisk" : ""
    }

    return step
