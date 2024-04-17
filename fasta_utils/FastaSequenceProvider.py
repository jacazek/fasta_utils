from fasta_utils import FastaFileReader
import threading
import re

chromosome_regex = re.compile(r'^(chr)?\d+$', re.IGNORECASE)
def file_reader_iterator(fasta_file_readers):
    for fasta_file_reader in fasta_file_readers:
        with fasta_file_reader:
            indices = [index for index, entry in enumerate(fasta_file_reader.index_table) if chromosome_regex.match(entry[0])]
            for header, sequence in fasta_file_reader.read_indices(indices):
                yield header, sequence

class FastaSequenceProvider():
    def __init__(self, fasta_files):
        self.lock = threading.Lock()
        # for each fasta file, create tuple of the fasta file, index file, and index table
        self.file_readers = [FastaFileReader(fasta_file) for fasta_file in fasta_files]
        self.fasta_files_iterator = file_reader_iterator(self.file_readers)
        # self.fasta_file_indices = [(fasta_file, f"{fasta_file}.fai", utils.load_fasta_file_index(f"{fasta_file}.fai")) for fasta_file in fasta_files]
        # self.readers = []
        # # for each fasta file, index, and index table
        # #
        # for fasta_file, fasta_file_index, index_table in self.fasta_file_indices:
        #     self.readers += [utils.read_fasta_file(fasta_file, fasta_file_index=fasta_file_index, index=index) for index, entry in enumerate(index_table) if not entry[0].startswith("scaf")]
        #
        # self.length = len(self.readers)
        # self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # for entry in self.readers:
        with self.lock:
            return next(self.fasta_files_iterator)
        # if (self.index < self.length):
        #     item = self.readers[self.index]
        #     self.index += 1
        #     return item
        # else:
        #     raise StopIteration


