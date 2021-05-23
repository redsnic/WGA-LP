# simple util to run a command line program
import subprocess
import os
import stat 

def run_sp(step, cmd):
    """
    run command and check execution
    :param cmd: a bash compatible command
    """
    print("INFO:"  + "running >> " + cmd)
    try:
        subprocess.run(cmd, shell=True, check=True, executable="/bin/bash")
    except Exception as excp:
        try:
            # delete last step's folder
            step.delete()
        except:
            pass
        raise excp


