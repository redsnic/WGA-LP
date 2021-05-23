from WGALP.checkpoint import CheckPoint
import os

class Workflow():

    def __init__(self, name, root):
        self.name = name
        self.root = root
        self.checkpoint = None

    def task(self, args_dict):
        raise NotImplementedError("No task defined for this Workflow")

    def run(self, args_dict, force = False):
        self._load()
        if (self.checkpoint.files is not None) or force:
            return self.checkpoint.files
        output = self.task(args_dict)
        self.checkpoint.set_content(output)
        self.checkpoint.files["root"] = self.root # root always contains who produced this output
        self.checkpoint.files["root_id"] = os.path.basename(self.root)
        self.checkpoint.write(self.root, self.name + ".checkpoint")
        return self.checkpoint.files
        
    def _load(self):
        self.checkpoint = CheckPoint()
        self.checkpoint.load(self.root, self.name + ".checkpoint")

