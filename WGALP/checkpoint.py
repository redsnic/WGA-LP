# object to save the intermediate status of the pipeline
import pickle 
import os

def pickle_load(filename):
    """
    load a pickle file from disk
    """
    handle = open(filename, "rb")
    out = pickle.load(handle)
    handle.close()
    return out

def pickle_write(filename, obj):
    """
    write an object to a pickle file
    """
    handle = open(filename, "wb")
    pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

def make_checkpoint(base_root, filename, obj):
    """
    factory to create meaningful checkpoints
    """
    ckp = CheckPoint()
    ckp.set_content(obj)
    ckp.write(base_root, filename)

def load_checkpoint(base_root, filename):
    """
    load the files related to a specific checkpoint
    """
    ckp = CheckPoint()
    ckp.load(base_root, filename)
    if ckp.is_loaded():
        return ckp
    return None



class CheckPoint():
    """
    the checkpoint class is useful to manage task that combine multiple 
    simplier blocks. It creates a file that stores the pointers to 
    the files produced by the task, making it possible to resume
    the pipeline without having to make recomputations. 
    """

    def __init__(self):
        self.files = {}
        self.base_root = None
        self.filename = None

    def load(self, base_root, filename):
        """
        load from disk if possible
        """
        self.base_root = base_root
        self.filename = filename
        try:
            self.files = pickle_load(os.path.join(base_root, filename))
        except FileNotFoundError:
            self.files = None

    def set_content(self, obj):
        """
        add the object associated with this ceckpoint
        """
        self.files = obj
    
    def write(self, base_root, filename):
        """
        write the checkpoint to the disk
        """
        self.base_root = base_root
        self.filename = filename
        pickle_write(os.path.join(base_root, filename), self.files)
            
    def __getitem__(self, arg):
        """
        get one of the stored files by ID
        """
        return self.files[arg]

    def __setitem__(self, name, value):
        """
        set one of the stored files by ID
        """
        self.files[name] = value 

    def is_loaded(self):
        """
        check if this checkpoint was initialized,
        useful when loading it from disk
        """
        return self.files != None

    def __str__(self):
        return str(self.files)

    def delete(self):
        """
        remove the file associated to this checkpoint
        """
        try:
            os.remove(os.path.join(self.base_root, self.filename))
        except:
            pass


