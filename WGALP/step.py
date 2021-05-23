# class to cope with the basic building blocks of a pipeline.

import os
import shutil
from WGALP.utils.genericUtils import get_files_recursively
 
class Step():

    def __init__(self, name, rootpath, execution_mode = "on_demand"):
        """
        execution_mode:
        "force" : always reruns the step
        "on_demand" : computes the step if it wasn't already computed (only checks if outpath exists)
        "read" : checks if outpath exists, otherwise throws an exception (FileNotFoundError)
        """
        # path and output dir
        self.name = name
        self.rootpath = rootpath
        self.outpath = os.path.join(rootpath, name)
        self.execution_mode = execution_mode
            
        # prepare output directory
        outpath_exists = os.path.isdir(self.outpath)
        # check what to do if mode is "on_demand"
        if self.execution_mode == "on_demand":
            if not outpath_exists:
                self.execution_mode = "force"
            else:
                self.execution_mode = "read"

        print(self.execution_mode, outpath_exists )
        
        if self.execution_mode == "force":
            # force
            if outpath_exists:
                print("WARNING: erasing an old output directory") 
                shutil.rmtree(self.outpath)
            os.mkdir(self.outpath)
        else:
            # read only
            if not outpath_exists:
                raise FileNotFoundError("ERROR: cannot find directory " + self.outpath)
        
        # comments
        self.has_description = False
        self.description = None
        self.input_description = None
        self.output_description = None

        # IO
        if self.execution_mode == "read":
            print("INFO: running step " + self.name + " in read mode")
        self.has_run = (self.execution_mode == "read")
        self.inputs = None
        self.command = None
        self.outputs = None
        

    def delete(self):
        """
        delete the output folder associated to this Step
        """
        if os.path.isdir(self.outpath):
            shutil.rmtree(self.outpath)
        self.outpath = None


    def __str__(self): 
        """
        print a brief description of this Step
        """
        out = ""
        out += ">> Step:" + self.name + "\n"
        if self.has_description:
            out += self.description + "\n"
            out += "=== INPUT ===" + "\n"
            out += self.input_description + "\n"
            out += "=== OUTPUT ===" + "\n"
            out += self.output_description + "\n"
        else:
            out += "No description available for this Step" + "\n"
        return out

    def set_description(self, description, input_description, output_description):
        """
        add printable comments to this step
        """
        self.has_description = True
        self.description = description
        self.input_description = input_description
        self.output_description = output_description

    def set_command(self, command):
        """
        add a command to this Step, 
        the command is a function that should be of the form
        fun(step_object, inputs)
        where inputs is a dictionary 
        """
        self.command = command

    def run(self, inputs):
        """
        run this step (if not in read mode)
        """
        if( self.command == None):
            raise Exception("ERROR: No command defined for this Step: " + self.name)

        self.outputs = {}
        self.inputs = inputs
        
        print("INFO:", "Step", self.name)
        print("INFO:", "Running on", self.inputs)
        
        try:
            self.command(self, inputs)
            print("INFO:", "With outputs", self.outputs)
            self.has_run = True
        except:
            print("ERROR:", "Execution of Step", self.name, "Failed!")
            raise

    def __getitem__(self, arg):
        """
        Read an output value from this step
        :param arg: path to output element file
        """
        if self.has_run:
            return(os.path.join(self.outpath, self.outputs[arg]))
    
        raise Exception("ERROR: Run this step before accessing its outputs. Step name:" + self.name)
    
    def access_file(self, filename):
        """
        Get a file path searching in the output directory of this Step
        :param filename: file to be searched (rises FileNotFoundError if not exists)
        """
        path = os.path.join(self.outpath, filename) 
        if os.path.isfile(path):
            return(path)
        
        raise FileNotFoundError(filename)

    def delete_file(self, path):
        """
        Permanently deletes a file or a subfolder of this step
        :param path: path to be deleted
        """
        del_path = os.path.join(self.outpath, path)
        if os.path.isfile(del_path):
            os.remove(del_path)
        elif os.path.isdir(del_path):
            shutil.rmtree(del_path)

    def delete_key(self, key):
        """
        Permanently deletes a file or a subfolder of this step (reading path from the output dict)
        :param path: path to be deleted
        """
        if key in self.outputs:
            del_path = os.path.join(self.outpath, self.outputs[key])
            if os.path.isfile(del_path):
                os.remove(del_path)
            elif os.path.isdir(del_path):
                shutil.rmtree(del_path)
            
    def delete_non_output_files(self):
        """
        permanently delete all files of this step that are not specified as outputs
        """
        for f in get_files_recursively(self.outpath):
            to_be_deleted = True
            for _, out in self.outputs.items():
                # avoid to delete files in a folder that 
                # is returned as output
                if f.startswith(out):
                    to_be_deleted = False
            if to_be_deleted:
                print(self.outpath, f)
                os.remove(os.path.join(self.outpath, f))
            

    def copy(self, new_name, new_rootpath=None):
        """
        Copy constructor, creates a new (and not run) Step with the 
        same description and command of the original one

        :param new_name: name of the new Step
        :param new_rootpath: name of the rootpath of the new Step. The same of the original if None.
        """
        if(new_rootpath == None):
            new_rootpath = self.rootpath
        
        new_step = Step(new_name, new_rootpath)

        # comments
        new_step.has_description = self.has_description
        new_step.description = self.description
        new_step.input_description = self.input_description
        new_step.output_description = self.output_description

        # IO
        new_step.command = self.command

        return new_step

    def get_files(self):
        out = {}
        for key, value in self.outputs.items():
            out[key] = os.path.join(self.rootpath, self.name, value)
        return out 



        


        

    





