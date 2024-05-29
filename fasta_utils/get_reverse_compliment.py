translation_table = str.maketrans("ATCGN", "TAGCN")


def get_reverse_compliment(sequence):
    return sequence[::-1].translate(translation_table)