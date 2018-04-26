import transrules as rules
import re 

class POSTagger:

    def __init__(self):
        self.rules = rules.TranslationHelper()

        self.rule_ws_incl = re.compile(r"(\s+)")
        self.rule_ws = re.compile(r"\s+")
        self.rule_alphanum = re.compile(r"\w+")
        pass

    def extract_special_tokens(self, string):
        """
        Splits and returns valid symbol tokens from a string of symbol characters.
        Unknown symbols will be treated as single-character token.
        
        For example, "++);" would return ["++", ")", ";"]
        """
        result = []
        while len(string) > 0:

            #If the string starts with a sequence of known token, e.g ++, +=, cut as needed.
            #Otherwise treat the first character as a standalone symbol.
            for token in self.rules.multichar_symbol_tokens:
                if(string.startswith(token)):
                    cut_len = len(token)
                    break
            else:
                cut_len = 1
            
            next_token, string = string[:cut_len], string[cut_len:]
            result.append(next_token)

        return result

    def rebuild_tokens(self, tokens):
        """
        Accepts these as parameter:
        1. List of tokenized single or multi-line comment.
        2. List of tokenized statement containing single or double quotes.

        Returns the same list, but with some parts merged (when needed)
        """
        if self.rules.is_singlecomment(tokens):
            return [tokens[0], "".join(tokens[1:])] 
        elif self.rules.is_multicomment(tokens):
            return [tokens[0], "".join(tokens[1:-1]), tokens[-1]]
        else:
            #If it's not a comment statement, assume it's a statement containing a string. 
            return self.merge_string(tokens)

    def merge_string(self, tokens):
        """
        Merges every tokens between single or double quotes (including the quotes) into one. 
        Leave the rest as it is, except that whitespaces outside quotes is removed.
        
        Will handle escaped quotes, but fails silently if there is non-even number of quotes 
        (all tokens after the last quote will be dumped)
        """
        in_string = False
        
        cur_string = ""
        cur_string_delimiter = None
        result_tokens = []

        for token in tokens:
            if in_string:
                #If the current token is the same as the one starting the string
                #(either single or double quote)
                if token == cur_string_delimiter:
                    #If the last character in current string is backslash, it means
                    #that the delimiter is escaped; continue.
                    if cur_string[-1] == "\\":
                        cur_string += token
                    #else it means that the current string is ending. Reset all flags.
                    else:
                        in_string = False
                        cur_string_delimiter = None
                        
                        cur_string += token
                        result_tokens.append(cur_string)
                        cur_string = ""
                else:
                    cur_string += token
            else:
                #If we're not currently in string and we stumble upon a quote, 
                #set in_string flag 
                if token == "'" or token == '"':
                    in_string = True
                    cur_string_delimiter = token
                    cur_string += token
                #Else add to result tokens if it isn't whitespace.
                else:
                    if self.rule_ws.match(token):
                        pass #do nothing
                    else:
                        result_tokens.append(token)
        
        return result_tokens

    def tokenize(self, text, preserve_whitespace=False):
        """
        Tokenizes a given string into strings of whitespace, alphanumeric, and valid symbol tokens in C.
        If preserve_whitespace is set to True, all whitespaces will be treated as tokens; 
        otherwise whitespaces will be skipped.
        """

        splitter = re.compile(r"(\w+|\s+)")
        
        result = []

        #Filter empty tokens, and loop through it.
        for token in filter(lambda token: len(token) > 0, splitter.split(text)):
            if(self.rule_ws.match(token)):
                if preserve_whitespace:
                    result.append(token)
            elif(self.rule_alphanum.match(token)):
                result.append(token)
            #it's neither alphanumeric or whitespace, assume it's a symbol string.
            else:
                result.extend(self.extract_special_tokens(token))

        return result

    def tag(self, statement):
         #TODO: Add string and comment merging mechanism.
         #TODO: Consider escaped single-quote & double-quote.

        #Check if there is single-quote/double-quote token in the statement.
        quote_exists = '"' in statement or "'" in statement
        #If there's quote in the statement, or it's a comment statement, set as True.
        is_ws_sensitive = quote_exists or self.rules.is_singlecomment(statement) or self.rules.is_multicomment(statement)
        
        tokens = self.tokenize(statement, preserve_whitespace=is_ws_sensitive)

        if is_ws_sensitive:
            tokens = self.rebuild_tokens(tokens)

        return tokens
        

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js