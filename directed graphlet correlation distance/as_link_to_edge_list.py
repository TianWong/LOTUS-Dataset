import sys

""""
convert an as_link file to an edge list to be processed
"""
def clean(infile, outfile):
    output = ""
    with open(infile, "r") as fin:
        for line in fin:
            if line[0] == 'D' or line[0] == 'I':
                line_split = line.split()
                output += f"{line_split[1]} {line_split[2]}\n"

    with open(outfile, "w") as fout:
        fout.write(output)

if __name__ == "__main__":
    clean(sys.argv[1], sys.argv[2])