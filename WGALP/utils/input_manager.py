import os 
import sys

def is_flag(arg):
    return arg.startswith("-")

def check_files(file_list):
    for f in file_list:
        if not os.path.isfile(f):
            raise FileNotFoundError("File not found: " + f)

def check_folders(folder_list):
    for f in folder_list:
        if not os.path.isdir(f):
            raise FileNotFoundError("Directory not found: " + f)

class InputManager():

    def __init__(self, program_description=""):
        self.program_description = program_description
        self.flags = {}
        self.descritptions = {}

    def parse(self, args):
        i = 0
        if len(args) == 0:
            print("--- no arguments given, printing help message ---")
            print(self.help())
            sys.exit(2) 
        while i < len(args):
            if args[i] == "--help":
                print(self.help())
                sys.exit(2)
            if is_flag(args[i]):
                try:
                    flag = self.flags[args[i]]
                    if flag["type"] == "flag":
                        flag["value"] = True
                        i = i + 1
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
                    elif flag["type"] == "path":
                        if i+1 <= len(args) and (os.path.isdir(args[i+1]) or os.path.isfile(args[i+1])):
                            flag["value"] = args[i+1]
                            i = i + 2
                        else:
                            raise Exception("Malformed input for flag: " + args[i])
                    elif flag["type"] == "dir":
                        if args[i+1].startswith("--"):
                            raise Exception("missing path for argument" + args[i])
                        if not os.path.isdir(args[i+1]):
                            os.mkdir(args[i+1])
                        flag["value"] = args[i+1]
                        i = i + 2
                    elif flag["type"] == "text":
                        flag["value"] = args[i+1]
                        i = i + 2
                        
                    
                except KeyError:
                    print("ERROR: unknown flag " + args[i])
                    print(self.help())
                    raise


    def add_arg(self, name, type_, description = ""):
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




