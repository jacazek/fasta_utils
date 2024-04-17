import csv


def load_fasta_index_file(fasta_index_file):
    data = None
    with open(fasta_index_file) as file:
        reader = csv.reader(file, delimiter="\t")
        # convert everything but the first column into a number
        return list(map(lambda row: [row[0]] + [int(value) for value in row[1:]], reader))