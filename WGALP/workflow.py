from WGALP.checkpoint import CheckPoint
import os


class Workflow():
    """
    This class helps in the creation of "super steps"
    that combine multiple simplier steps.
    """

    def __init__(self, name, root):
        self.name = name
        self.root = root
        self.checkpoint = None

    def task(self, args_dict):
        """
        This function must be defined by creating a subclass of Workflow
        """
        raise NotImplementedError("No task defined for this Workflow")

    def run(self, args_dict, force = False):
        """
        Run the task and create a checkpoint to keep track of the work already done
        """
        self._load()
        if (self.checkpoint.files is not None) and not force:
            return self.checkpoint.files
        output = self.task(args_dict)
        self.checkpoint.set_content(output)
        self.checkpoint.files["root"] = self.root # root always contains who produced this output
        self.checkpoint.files["root_id"] = os.path.basename(self.root)
        self.checkpoint.write(self.root, self.name + ".checkpoint")
        return self.checkpoint.files
        
    def _load(self):
        """
        load this Workflow from the checkpoint
        """
        self.checkpoint = CheckPoint()
        self.checkpoint.load(self.root, self.name + ".checkpoint")

    def delete_checkpoint(self):
        """
        erase the checkpoint file.
        Useful to force the execution for subsequent calls.
        """
        self.checkpoint.delete()
        


