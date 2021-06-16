
import sys

def clean_spaces(f):
    
    out = ""
    for line in f:
        if line.startswith(">"):
            out += line
        else:
            out += line[:len(line)-1]

    return out


if __name__ == "__main__":
    f = open(sys.argv[1], "r")
    print(clean_spaces(f))
    f.close()
        