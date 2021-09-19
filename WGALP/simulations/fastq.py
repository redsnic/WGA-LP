import numpy as np

def to_phred33(scores):
    return "".join([ chr( min(max(s,0), 42) + 33) for s in scores ])

class READ():

    def __init__(self, description, sequence, quality):
        self.description = description
        self.sequence = sequence
        self.quality = quality
        
    def __str__(self):
        out = ""
        out += "@" + self.description + "\n"
        out += self.sequence + "\n"
        out += "+\n"
        out += to_phred33(self.quality) + "\n"
        return out


class FASTQ():

    def __init__(self):
        self.reads = []

    def __str__(self):
        return "".join(map(str, self.reads))

    def add(self, description, sequence, quality):
        self.reads += [READ(description, sequence, quality)]

