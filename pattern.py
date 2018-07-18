class Pattern:
    def __init__(self, start=[], end=[]):
        if not isinstance(start, list):
            start = []
            print("Start parameter is not list, using empty list instead")
        elif not isinstance(end, list):
            end = []
            print("End parameter is not list, using empty list instead")
        
        self.start = [] + start
        self.end = [] + end

    def fit(self, tags):
        target_length = len(tags) - (len(self.start) + len(self.end))
        return self.start + ([None] * target_length) + self.end

    def trace(self, tags):
        for ptrn, tag in zip(self.fit(tags), tags):
            if ptrn is None:
                match = True
            elif isinstance(ptrn, list) or isinstance(ptrn, dict):
                match = True in (tag == item for item in ptrn)
            else:
                match = ptrn == tag

            if not match:
                return False
            
        return True