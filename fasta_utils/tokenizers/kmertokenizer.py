import math


translation_table = str.maketrans("ATCGN", "TAGCN")


def get_compliment(sequence):
    return sequence[::-1].translate(translation_table)


class KmerTokenizer:
    """
    KmerTokenizer breaks a sequence up into set of tokens
    Problem with current implementation is that if the last token is not of size kmer_size, it will
    become an unknown token.  The last token could be really important though.
    """
    def __init__(self, kmer_size, stride, include_compliement=False):
        """
        Construct a new tokenizer that will tokenize an input sequence
        :param kmer_size: The size of tokens
        :param stride: The relative offset of subsequent tokens
        """
        self.kmer_size = kmer_size
        self.stride = stride
        self.include_compliment = include_compliement

    def get_id_string(self):
        return f"{self.kmer_size}mer-s{self.stride}"

    def tokenize(self, sequence):
        """
        Lazy API to tokenize the sequence into tokens of length kmer_size
        at stride
        :param sequence: The sequence to tokenize
        :return: tuples of sequence and reversed sequence
        """
        sequence_length = len(sequence)
        # return the sequence if kmer_size is larger
        if sequence_length < self.kmer_size:
            if self.include_compliment:
                return sequence, reversed_sequence
            else:
                return sequence

        if self.stride == 0:
            kmer_count = sequence_length - 1
        else:
            kmer_count = math.ceil(((len(sequence) - self.kmer_size) / self.stride) + 1)

        if self.include_compliment:
            reversed_sequence = get_compliment(sequence)
            for index in range(kmer_count):
                start = min(index * self.stride, sequence_length - self.kmer_size)
                end = start + self.kmer_size
                yield sequence[start: end], reversed_sequence[start: end]
        else:
            for index in range(kmer_count):
                start = min(index * self.stride, sequence_length - self.kmer_size)
                end = start + self.kmer_size
                yield sequence[start: end]

    def tokenize_list(self, sequence):
        """
        Eager API to tokenize the sequence into tokens of length kmer_size
        at stride
        :param sequence: The sequence to tokenize
        :return: a list of kmers
        """
        return list(self.tokenize(sequence))




