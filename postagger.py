import transrules as rules
import re 

class POSTagger:

    #TODO: Design decision: split per special character and merge as needed, or split chunks at once and split when needed?
    #First option is good when special characters are lined up, e.g ("% but it costs more computation as it splits everything.
    #Second option need less computation, but need to mitigate cases where special cases are lined up. 
    #TODO: Add string and comment merging mechanism.

    def __init__(self):
        pass

    def tokenize(self, text):
        splitter = re.compile(r"(\W+)")    
        non_ws = re.compile(r"\S+")
        #Filter empty tokens.
        return list(filter(lambda token: len(token) > 0, splitter.split(text)))    

    def tag(self, text):
        if True in (text.startswith(token) for token in rules.comments):
            pass

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js