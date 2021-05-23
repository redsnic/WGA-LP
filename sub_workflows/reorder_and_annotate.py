from WGALP.workflow import Workflow

from WGALP.blocks.prokka import prokka
from WGALP.blocks.mauve import mauve_contig_sorting
# and others when possible

class ReorderAndAnnotate(Workflow):
    
    def task(self, args_dict):
        
        contig = args_dict["contig"]
        reference = args_dict["reference"]
        root = self.root

        try:
            # Mauve
            if reference == None:
                raise Exception
            step = mauve_contig_sorting(self.name + "_mauve", root, reference, contig)
            contig = step["contigs"]
        except:
            print("skipping contigs reordering for " + contig)
            raise 
        # prokka
        step = prokka(self.name + "_prokka", root, contig)

        return step.get_files()
