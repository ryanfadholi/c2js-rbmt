class Pattern:
    def __init__(self, tag, start=None, end=None, carryover=True):
        if not isinstance(start, list):
            start = []
            print("Start parameter is not list, using empty list instead")
        elif not isinstance(end, list):
            end = []
            print("End parameter is not list, using empty list instead")
        
        self.tag = tag
        self.start = [] + start
        self.end = [] + end

        self.carryover = carryover

    def fit(self, tags):
        """Matches the length of the pattern to the length of tags"""
        target_length = len(tags) - (len(self.start) + len(self.end))
        return self.start + ([None] * target_length) + self.end

    def trace(self, tags):
        """Compares the pattern to the tag"""
        for ptrn, tag in zip(self.fit(tags), tags):
            if ptrn is None:
                match = True
            elif isinstance(ptrn, list) or isinstance(ptrn, dict):
                match = tag in ptrn
            else:
                match = ptrn == tag

            if not match:
                return False
            
        return True