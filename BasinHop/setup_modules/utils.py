def seq_from_fasta(filepath):
    fastaFile = open(filepath)
    seq = ""
    for line in fastaFile:
        parsedLine = line.strip()
        if parsedLine.startswith('>'):
            continue
        seq+=parsedLine
    return seq

trueVals = [1, "true", "True", "T" , "t", "y", "Y", "yes", "Yes"]
def getTrueValues():
    return trueVals
