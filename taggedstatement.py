import copy

class TaggedStatement:
    def __init__(self, tagged_tokens):
        #Ensure copy
        self.tagged_tokens = copy.copy(tagged_tokens)

    def __len__(self):
        return len(self.tagged_tokens)
