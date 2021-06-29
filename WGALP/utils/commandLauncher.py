# simple util to run command line program from steps
import subprocess

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
            # delete last step's folder in case of failure
            step.delete()
        except:
            pass
        raise excp


