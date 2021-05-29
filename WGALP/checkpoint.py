# object to save the intermediate status of the pipeline
import pickle 
import os

def pickle_load(filename):
    handle = open(filename, "rb")
    out = pickle.load(handle)
    handle.close()
    return out

def pickle_write(filename, obj):
    handle = open(filename, "wb")
    pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

def make_checkpoint(base_root, filename, obj):
    ckp = CheckPoint()
    ckp.set_content(obj)
    ckp.write(base_root, filename)

def load_checkpoint(base_root, filename):
    ckp = CheckPoint()
    ckp.load(base_root, filename)
    if ckp.is_loaded():
        return ckp
    return None

class CheckPoint():

    def __init__(self):
        self.files = {}
        self.base_root = None
        self.filename = None

    def load(self, base_root, filename):
        self.base_root = base_root
        self.filename = filename
        try:
            self.files = pickle_load(os.path.join(base_root, filename))
        except FileNotFoundError:
            self.files = None

    def set_content(self, obj):
        self.files = obj
    
    def write(self, base_root, filename):
        self.base_root = base_root
        self.filename = filename
        pickle_write(os.path.join(base_root, filename), self.files)
            
    def __getitem__(self, arg):
        return self.files[arg]

    def __setitem__(self, name, value):
        self.files[name] = value 

    def is_loaded(self):
        return self.files != None

    def __str__(self):
        return str(self.files)

    def delete(self):
        try:
            os.remove(os.path.join(self.base_root, self.filename))
        except:
            pass


