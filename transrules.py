import tokendicts as tokens
import re

from typing import Dict, List

#TODO: When everything's said and done, is it better to spread this file to each project that need each individual function instead?

class TranslationHelper:

    def __init__(self):
        #tokendicts redirects
        self.singlecomment_token = tokens.single_comment
        self.multicomment_token = tokens.multi_comment
        self.multicomment_token_end = tokens.multi_comment_end
        self.multichar_symbol_tokens = tokens.multichar_symbol

    def findall(self, text, token):
        """
        Find all instances of token in text.
        Returns a list of indexes in which the token start.
        (Supports overlapping cases)
        """
        # print(f"Token: {token}; Text: {text}")

        result = []
        token_len = len(token)
        for i in range(len(text)):
            if token == text[i:i+token_len]:
                result.append(i)

        return result 

    def findfirst(self, text, tokens):
        """
        Find the first instance of any token from the tokens list on the text string. 
        Returns -1 when there is no instance of any token in the string.
        """

        if isinstance(tokens, dict):
            findall = [text.find(token) for key, token in tokens.items()]
        elif isinstance(tokens, list):
            findall = [text.find(token) for token in tokens]
        
        found = list(filter(lambda pos: pos > -1, findall))

        return min(found) if len(found) > 0 else -1

    findstring = lambda self, text: self.findfirst(text, tokens.string_identifiers)
    findcomment = lambda self, text: self.findfirst(text, tokens.comments)

    def identify(self, input_tokens):

        id_int = re.compile(r"^\d+$")
        id_float = re.compile(r"^\d+\.(\d+)?$")
        id_var = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

        id_char = re.compile(r"^'.*'$", re.DOTALL)
        id_string = re.compile(r'^".*"$', re.DOTALL)

        for token in input_tokens:
            if token.tag == "unknown":
                token_str = token.token
                #Match library names (stdio.h, conio.h)
                if token_str.lower().endswith(".h"):
                    token.tag = tokens.tag_name_preproc
                #Match integers (1234, 5454, 5)
                elif id_int.match(token_str):
                    token.tag = tokens.tag_val_int
                #Match floating-point (1.1, 3.14, 2.)
                elif id_float.match(token_str):
                    token.tag = tokens.tag_val_float
                #Match variable names (x, result, _hero9, y2)
                elif id_var.match(token_str):
                    token.tag = tokens.tag_name_var
                #Match characters ('a', 'b')
                elif id_char.match(token_str):
                    token.tag = tokens.tag_val_char
                #Match strings ("abc", "def")
                elif id_string.match(token_str):
                    token.tag = tokens.tag_val_string

        return input_tokens

    def match(self, token):
        token_dicts = [ tokens.arithmetic_operator, tokens.bitwise_operator, tokens.relational_operator, 
            tokens.compound_assignment_operator, tokens.logical_operator, tokens.misc_operator, tokens.comments, 
            tokens.conditionals, tokens.datatypes, tokens.loops, tokens.special_functions, tokens.keywords ]

        for token_dict in token_dicts:
            for key, value in token_dict.items():
                if token == value:
                    return key
        
        return "unknown"

    def tokens_validate(self, text_tokens, rule_tokens):
        """
        A template function to check if text_tokens list of string's first element
        is rule_tokens (if it's string), or if it's in rule_tokens if the text starts 
        with any token from the tokens (if it's list or dictionary).
        """
        start_token = text_tokens[0]
        if isinstance(rule_tokens, dict):
            return start_token in rule_tokens.values()
        elif isinstance(rule_tokens, list):
            return start_token in rule_tokens
        elif isinstance(rule_tokens, str):
            return start_token == rule_tokens
        else:
            return False
            
    def text_validate(self, text, tokens):
        """
        A template function to check if text string starts with the tokens (if it's string),
        or if the text starts with any token from the tokens (if it's list or dictionary).
        """
        if isinstance(tokens, dict):
            return True in (text.startswith(token) for token in tokens.values())
        elif isinstance(tokens, list):
            return True in (text.startswith(token) for token in tokens)
        elif isinstance(tokens, str):
            return text.startswith(tokens)
        else:
            return False

    def stmt_validate(self, statement, tokens):
        """
        A template function to check if a statement (either as a string or a list of string)
        starts with the tokens variable (tokens might be a dict, list, or string)
        """
        if isinstance(statement, list):
            return self.tokens_validate(statement, tokens)
        elif isinstance(statement, str):
            return self.text_validate(statement, tokens)
        else:
            raise ValueError("Statement is neither a list or string object")
        
    #Functions to check the type of a statement.
    is_block_end = lambda self, text: self.stmt_validate(text, tokens.curly_right)
    is_block_start = lambda self, text: self.stmt_validate(text, tokens.curly_left)
    is_conditional = lambda self, text: self.stmt_validate(text, tokens.conditionals)
    is_declaration = lambda self, text: self.stmt_validate(text, tokens.datatypes)
    is_include = lambda self, text: self.stmt_validate(text, tokens.preprocessor)
    is_loop = lambda self, text: self.stmt_validate(text, tokens.loops)
    is_multicomment = lambda self, text: self.stmt_validate(text, tokens.multi_comment)
    is_singlecomment = lambda self, text: self.stmt_validate(text, tokens.single_comment)
    is_string = lambda self, text: self.stmt_validate(text, tokens.string_identifiers)