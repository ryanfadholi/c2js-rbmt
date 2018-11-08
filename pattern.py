class Pattern:
    def __init__(self, tag, start=None, end=None, carryover=True, ignored=None):
        #Default arguments
        if start is None:
            start = []
        if end is None:
            end = []
        if ignored is None:
            ignored = []
        
        self.tag = tag
        self.start = [] + start
        self.end = [] + end
        self.ignored = [] + ignored

        self.carryover = carryover

    def fit(self, tags):
        """Matches the length of the pattern to the length of tags"""
        target_length = len(tags) - (len(self.start) + len(self.end))
        return self.start + ([None] * target_length) + self.end

    def trace(self, tags):
        """Compares the pattern to the tag"""

        #Remove ignored tags (if exists)
        if self.ignored:
            result = []
            for tag in tags:
                if tag in self.ignored:
                    continue
                result.append(tag)
            tags = result

        for ptrn, tag in zip(self.fit(tags), tags):
            if ptrn is None:
                match = True
            elif isinstance(ptrn, (list, dict)):
                match = tag in ptrn
            else:
                match = ptrn == tag

            if not match:
                return False
            
        return True