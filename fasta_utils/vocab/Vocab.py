import pickle


class Vocab():
    def __init__(self, tokens, specials=[]):

        for special in specials:
            tokens[special] = 1

        self.default_index = -1
        self.token_to_index = {}
        self.index_to_token = []
        for index, (key,value) in enumerate(tokens.items()):
            self.token_to_index[key] = index
            self.index_to_token.append(key)
        self.num_tokens = len(self.index_to_token)

    def __len__(self):
        return self.num_tokens

    def __getitem__(self, token):
        return self.get_index_for_token(token)

    def get_token_for_index(self, index):
        return self.index_to_token[index] if index > 0 and index < self.num_tokens else self.index_to_token[self.default_index]

    def get_index_for_token(self, token):
        return self.token_to_index.get(token, self.default_index)

    def set_default_index(self, index):
        self.default_index = index

    @staticmethod
    def save(vocab, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(vocab, file)

    @staticmethod
    def load(file_name):
        with open(file_name, "rb") as file:
            return pickle.load(file)
