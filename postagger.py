import transrules as rules
import re 

from collections import namedtuple
from itertools import repeat

class POSTagger:

    def __init__(self):
        self.rules = rules.TranslationHelper()

        self.rule_digit = re.compile(r"^\d+$")
        self.rule_ws = re.compile(r"^\s+$")
        self.rule_alphanum = re.compile(r"^\w+$")

    #Check if there is single-quote/double-quote token in the statement.
    quote_token_exists = lambda self, tokens: '"' in tokens or "'" in tokens
    dot_token_exists = lambda self, tokens: '.' in tokens

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

    def generate_tag(self, token, token_type):
        """
        Returns a dictionary containing token and token type.
        """
        return {
            "token" : token,
            "type"  : token_type
        }


    def rebuild_tokens(self, tokens):
        """
        Accepts these as parameter:
        1. List of tokenized single or multi-line comment.
        2. List of tokenized statement containing single or double quotes.
        3. List of tokenized statement containing dots.

        Returns the same list, but with some parts merged (when needed)
        """
        if self.rules.is_singlecomment(tokens):
            return [tokens[0], "".join(tokens[1:])] 
        elif self.rules.is_multicomment(tokens):
            return [tokens[0], "".join(tokens[1:-1]), tokens[-1]]
        else:
            #If it's not a comment statement, assume it's a statement containing a string or dots.
            if self.quote_token_exists(tokens): 
                tokens = self.merge_string(tokens)    
            
            if self.dot_token_exists(tokens):
                tokens = self.merge_float(tokens)

            return tokens

    def create_taggedtoken(self, token, token_type):
        return {"token" : token, "type" : token_type}

    def merge_float(self, tokens):
        """
        Merges every digit, dot, digit token sequence into one.
        """
        index = 0
        last_check = len(tokens) - 2 #Check until there is two remaining tokens.
        result = []

        #Check until the last three tokens. (Checking further than this will cause index error :) )
        while index < last_check:
            #TODO: Fix floats that ends with dot, e.g: "2.", "100."
            #Merge dots of floating-point numbers (e.g "3.", "4.14")
            if tokens[index+1] == "." and self.rule_digit.match(tokens[index]):
                #At this point, there's a number followed by a dot.
                to_join = 2 #Number of token to join
                if self.rule_digit.match(tokens[index+2]):
                    #If the dot is in turn followed by a digit, assume that it's the decimal part of the float
                    to_join = 3

                result.append("".join(tokens[index:index+to_join]))
                index += to_join
            #Merge dots of library names in include statements.
            elif tokens[0] == "#" and tokens[index+1] == ".":
                result.append("".join(tokens[index:index+3]))
                index += 3                
            else:
                result.append(tokens[index])
                index += 1

        #After the checking is done, append the remaining last three tokens.
        while index < len(tokens):
            result.append(tokens[index])
            index += 1

        return result

    def merge_string(self, tokens):
        """
        Merges every tokens between single or double quotes (including the quotes) into one. 
        Leave the rest as it is, except that whitespaces outside quotes is removed.
        
        Will handle escaped quotes correctly, but fails silently if there is non-even number of quotes 
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

    def split_statement(self, text, preserve_whitespace=False):
        """
        Splits a given string into strings of whitespace, alphanumeric, and valid symbol tokens in C.
        If preserve_whitespace is set to True, all whitespaces will be treated as tokens; 
        otherwise whitespaces will be skipped.
        """

        splitter = re.compile(r"(\w+|\s+)")
        
        result = []

        #Filter empty tokens, and loop through it.
        for token in filter(lambda token: len(token) > 0, splitter.split(text)):
            if self.rule_ws.match(token):
                if preserve_whitespace:
                    result.append(token)
            elif self.rule_alphanum.match(token):
                result.append(token)
            #it's neither alphanumeric or whitespace, assume it's a symbol string.
            else:
                result.extend(self.extract_special_tokens(token))

        return result

    def tokenize(self, statement):
        """
        Tokenizes C statement given as parameter into tagging-ready tokens.
        """

        #If there's quote in the statement, or it's a comment statement, set as True.
        is_ws_sensitive = self.quote_token_exists(statement) or self.rules.is_singlecomment(statement) or self.rules.is_multicomment(statement)
        
        tokens = self.split_statement(statement, preserve_whitespace=is_ws_sensitive)

        if is_ws_sensitive or self.dot_token_exists(statement):
            tokens = self.rebuild_tokens(tokens)

        return tokens

    def tag(self, statement):
        tokens = self.tokenize(statement)
        
        #Only matches known tokens
        matched_tokens = list(map(lambda x: self.create_taggedtoken(x, self.rules.match(x)), tokens))
        return self.rules.identify(matched_tokens)

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js