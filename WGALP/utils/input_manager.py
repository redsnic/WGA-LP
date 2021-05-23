import os 

def is_flag(arg):
    return arg.startswith("-")

class InputManager():

    def __init__(self):
        self.flags = {}

    def parse(self, args):
        i = 0
        while i < len(args):
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

                except KeyError:
                    print("ERROR: unknown flag " + args[i])
                    raise


    def add_arg(self, name, type_):
        self.flags[name] = {
            "type" : type_
        } 
        if self.flags[name]["type"] == "flag":
            self.flags[name]["value"] = False
        elif self.flags[name]["type"] == "list":
            self.flags[name]["value"] = []
        elif self.flags[name]["type"] == "path":
            self.flags[name]["value"] = None
        else:
            raise Exception("non valid flag type " + type_)

    def __str__(self):
        return str(self.flags)

    def __getitem__(self, arg):
        return self.flags[arg]




