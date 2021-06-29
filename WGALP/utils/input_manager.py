import os 
import sys

def is_flag(arg):
    return arg.startswith("-")

def check_files(file_list):
    """
    Procedure that checks if each folder of a list is valid (exists and was given as output)
    :param file_list list of file paths to be verified for existance:
    """
    for f in file_list:
        if f is None:
            raise Exception("Missing a required argument, use --help for more information")
        if not os.path.isfile(f):
            raise FileNotFoundError("File not found: " + f)

def check_folders(folder_list):
    """
    Procedure that checks if each folder of a list is valid (exists and was given as output)
    :param file_list list of folder paths to be verified for existance:
    """
    for f in folder_list:
        if f is None:
            raise Exception("Missing a required argument, use --help for more information")
        if not os.path.isdir(f):
            raise FileNotFoundError("Directory not found: " + f)

class InputManager():

    def __init__(self, program_description=""):
        self.program_description = program_description
        self.flags = {}
        self.descritptions = {}

    def parse(self, args):
        i = 0
        # by default, the absence of arguments implies the help must be shown
        if len(args) == 0:
            print("--- no arguments given, printing help message ---")
            print(self.help())
            sys.exit(2) 

        # loop to explore the arguments
        while i < len(args):

            # --help interrupts the evaluation and prints the help message
            if args[i] == "--help":
                print(self.help())
                sys.exit(2)

            # if the argument is one of the possible valid options
            if is_flag(args[i]):
                try:
                    flag = self.flags[args[i]]
                    # if it is a flag evaluate it as a boolean set at true
                    if flag["type"] == "flag":
                        flag["value"] = True
                        i = i + 1
                    # if it is a list, incorporate all the following arguments 
                    # in single list, until another known flag is found 
                    elif flag["type"] == "list":
                        j = i + 1
                        arg_list = []
                        while j < len(args) and not is_flag(args[j]):
                            arg_list.append(args[j])
                            j += 1
                        if(len(arg_list) == 0):
                            raise Exception("No arguments associated to this flag: " + args[i])
                        flag["value"] = arg_list
                        i = j
                    # --- these flag types process only the argument after their position
                    # if it is a path, evaluate its correctnes (must exist) 
                    elif flag["type"] == "path":
                        if i+1 <= len(args) and (os.path.isdir(args[i+1]) or os.path.isfile(args[i+1])):
                            flag["value"] = args[i+1]
                            i = i + 2
                        else:
                            raise Exception("Malformed input for flag: " + args[i])
                    # if it is a dir, specifically check that it is actually a dir
                    elif flag["type"] == "dir":
                        if args[i+1].startswith("--"):
                            raise Exception("missing path for argument" + args[i])
                        if not os.path.isdir(args[i+1]):
                            os.mkdir(args[i+1])
                        flag["value"] = args[i+1]
                        i = i + 2
                    # finally, with a text argument no check on the content are performed 
                    elif flag["type"] == "text":
                        flag["value"] = args[i+1]
                        i = i + 2
                except KeyError:
                    print("ERROR: unknown flag " + args[i])
                    print(self.help())
                    raise
            else: 
                raise Exception("ERROR: I don't know how to handle this: " + args[i] + "\nHave you forgotten an argument?")


    def add_arg(self, name, type_, description = ""):
        """
        Add an argument to the input manager. 
        Possible types are:
        flag, list, path, dir and text
        * flag : a boolean value
        * path : a valid and existing path
        * dir : a valid and existing directory
        * text : a non checked value
        * list : a sequence of non checked values

        description is the message that will be printed in the help associated to 
        this input manager
        """
        self.descritptions[name] = description
        self.flags[name] = {
            "type" : type_
        } 
        if self.flags[name]["type"] == "flag":
            self.flags[name]["value"] = False
        elif self.flags[name]["type"] == "list":
            self.flags[name]["value"] = []
        elif self.flags[name]["type"] == "path":
            self.flags[name]["value"] = None
        elif self.flags[name]["type"] == "dir":
            self.flags[name]["value"] = None
        elif self.flags[name]["type"] == "text":
            self.flags[name]["value"] = None
        else:
            raise Exception("non valid flag type " + type_)

    def help(self):
        """
        print the help message for this input manager (automatically generated)
        """
        out = ""
        if self.program_description != "":
            out += self.program_description + "\n"
        out += "--- arguments:" + "\n"
        for name, description in self.descritptions.items():
            out += "\t" + name + " : " + description + "\n"
        out += "\t" + "--help" + " : " + "print this message" + "\n"
        return out
            
    def __str__(self):
        return self.help()

    def __getitem__(self, arg):
        return self.flags[arg]




