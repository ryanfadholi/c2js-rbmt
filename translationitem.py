from taggedtoken import TaggedToken

class TranslationItem:
    def __init__(self, key, new_key, new_value):
        self.key = key
        self.new_key = new_key
        self.new_value = new_value

    def __iter__(self):
        if isinstance(self.key, str):
            yield (self.key, TaggedToken(self.new_key, self.new_value))
            return
        elif isinstance(self.key, (dict, list)):
            for item in self.key:
                yield(item, TaggedToken(self.new_key, self.new_value))
                