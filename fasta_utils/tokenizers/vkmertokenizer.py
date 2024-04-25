import math
import random
import numpy as np
import reactivex
from reactivex.scheduler.eventloop import AsyncIOScheduler


class VariableKmerTokenizer:
    """
    vKmerTokenizer breaks a sequence up into set of tokens
    Problem with current implementation is that if the last token is not of size kmer_size, it will
    become an unknown token.  The last token could be really important though.
    """

    def __init__(self, min_kmer_size=3, max_kmer_size=7, stride=3):
        self.min_kmer_size = min_kmer_size
        self.max_kmer_size = max_kmer_size
        self.rand_mod = (max_kmer_size - min_kmer_size) + 1
        self.stride = stride
        self.random_count = 1000
        self.random_range = range(self.random_count)
        self._generate_random_indices()

    def get_id_string(self):
        return f"{self.min_kmer_size}mer-{self.max_kmer_size}mer-s{self.stride}"

    def _generate_random_indices(self):
        self.random_indices = [int(random.random() * 10 % self.rand_mod + self.min_kmer_size) for _ in
                               self.random_range]

    def tokenize(self, sequence):
        """
        Lazy API to tokenize the sequence into tokens of length kmer_size
        at stride
        :param sequence: The sequence to tokenize
        :return: a list of kmers
        """
        subscription = reactivex.interval(10).subscribe(on_next=lambda value: self._generate_random_indices())
        sequence_length = len(sequence)
        # return the sequence if kmer_size is larger
        if sequence_length <= self.max_kmer_size:
            return sequence

        final_token_start = sequence_length - self.max_kmer_size
        current = 0
        count = 0
        while current < sequence_length - self.stride:
            # if count == 0:
            #     random_indices = self._generate_random_indices()

            start = current
            if final_token_start <= start:
                end = sequence_length
                current = sequence_length
                subscription.dispose()
            else:
                end = min(start + self.random_indices[count % self.random_count], sequence_length)
                current += self.stride

            count += 1
            yield sequence[start: end]

    def tokenize_list(self, sequence):
        """
        Eager API to tokenize the sequence into tokens of length kmer_size
        at stride
        :param sequence: The sequence to tokenize
        :return: a list of kmers
        """
        return list(self.tokenize(sequence))
