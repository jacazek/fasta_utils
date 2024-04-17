
def read_fasta_file(fasta_file, fasta_file_index=None, index=0):
    with FastaFileReader(fasta_file, fasta_file_index) as fasta_file_reader:
        for header, sequence in fasta_file_reader.read_at_index(index):
            yield header, sequence