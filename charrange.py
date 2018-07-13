class CharRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, item):
        return self.start <= item <= self.end

    def __repr__(self):
        return f"({self.start}-{self.end})"

    def __str__(self):
        return f"({self.start}-{self.end})"
