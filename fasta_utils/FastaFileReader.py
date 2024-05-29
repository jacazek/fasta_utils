import math
import re
import os
import gzip
from fasta_utils import load_fasta_index_file
from fasta_utils import get_reverse_compliment

prefix_regex = re.compile("^>")


class FastaFileReader():
    SEQUENCE_OFFSET = 2
    SEQUENCE_LENGTH = 1
    SEQUENCE_BASES = 3
    LINE_WIDTH = 4

    def __init__(self, fasta_file, index_file=None):
        self.fasta_file = fasta_file
        self.is_gzipped = self.fasta_file.endswith(".gz")
        self.index_file = index_file if index_file is not None else fasta_file + ".fai"

    def __enter__(self):
        self.file = open(self.fasta_file) if not self.is_gzipped else gzip.open(self.fasta_file, "rt")
        self.index_table = load_fasta_index_file(self.index_file) if os.path.exists(self.index_file) else None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def get_index_table_length(self):
        return len(self.index_table)

    def read_at_index(self, index, reverse_compliment=False):
        if self.index_table is None:
            raise Exception("cannot read to index when no fasta index found")

        sequence = ""

        if index != 0:
            previous_entry = self.index_table[index - 1]
            previous_lines = int(
                math.ceil(previous_entry[self.SEQUENCE_LENGTH] / previous_entry[self.SEQUENCE_BASES])) - 1
            previous_bytes = previous_lines * (previous_entry[self.LINE_WIDTH])
            previous_last_line = previous_bytes + previous_entry[self.SEQUENCE_OFFSET]
            self.file.seek(previous_last_line)
            self.file.readline()  # discard the last line

        header = self.file.readline().rstrip()
        line = self.file.readline()

        while not prefix_regex.match(line):
            sequence += line.strip()
            line = self.file.readline()

        if reverse_compliment:
            yield header, get_reverse_compliment(sequence)
        else:
            yield header, sequence

    def read_indices(self, indices, reverse_compliment=False):
        for index in indices:
            for value in self.read_at_index(index, reverse_compliment=reverse_compliment):
                yield value

    def read_all(self, reverse_compliment=False):
        header = ""
        sequence = ""
        self.file.seek(0)
        line = self.file.readline()
        while line != "":
            if prefix_regex.match(line):
                if header != "":  # is there an existing header?
                    if reverse_compliment:
                        yield header, get_reverse_compliment(sequence)
                    else:
                        yield header, sequence  # if so, yield the prior header and sequence before prepping for new sequence
                header = line.strip()  # set the header
                sequence = ""  # reset the sequence
            else:
                sequence += line.strip()
            line = self.file.readline()