import itertools

import tokendicts

from charrange import CharRange
from collections import namedtuple

TEMPFILE_PATH = "temp/source.txt"

class Deformatter:

    def get_bracket_end(self, text):
        """
        Returns an index where the first bracket set of the text ends, 
        Works even if there is nested brackets present.
        Returns -1 if the first bracket set is not complete/no bracket sets are found. 
        """
        open_brackets = self.get_occurrences(text, "(")
        close_brackets = self.get_occurrences(text, ")")

        result = -1
        offset = 1 #Length of closing bracket (")")

        if open_brackets and close_brackets: #Do only if both is not empty, if either is empty means the statement doesn't end yet
            for closing_count, closing_pos in enumerate(close_brackets, 1):
                #Count how many opening brackets are present before the currently checked closing bracket. 
                opening_count = len(list(filter(lambda pos: pos < closing_pos, open_brackets)))
                if(closing_count == opening_count):
                    result = closing_pos
                    break

        return result + offset if result > -1 else -1

    def get_declaration_end(self, text):
        """
        Returns an index where the declaration statement ends. Returns -1 if the statement isn't ending yet.
        Declaration could mean a variable or function declaration,
        and the function will adapt depending on what it assumes the declaration is.
        """        
        curlybrace_pos = self.get_statement_end(text, "{")
        semicolon_pos = self.get_statement_end(text, ";")

        if curlybrace_pos > 0 and curlybrace_pos < semicolon_pos:
            return self.get_bracket_end(text)
        else:
            return semicolon_pos

    def _exception_tokens(self, text):
        """
        Returns a list of index of every occurrence of ', ", //, and /*.
        (Which may sign a start of exception range)

        Returns empty list if none are found.
        """
        quotes_pos = self._search(tokendicts.string_identifiers, text)
        comment_start_pos = self._search(tokendicts.comments, text)

        result = list(itertools.chain.from_iterable((quotes_pos, comment_start_pos)))
        return sorted(result)

    def get_occurrences(self, text, separator, do_exception_checking=True):
        """
        separator := str
        Returns the list of index of every separator occurrence in text. Returns empty list if no occurence of separator is found.
        (The list are sorted from the smallest to largest)
        
        if do_exception_checking is set to True, the function will call get_parsing_exceptions(),
        and any occurrence found within the ranges returned by that function will be considered invalid and excluded from the result.
        """

        to_ignore = self.get_parsing_exceptions(text) if do_exception_checking else []
        #If x is present in any CharRange from to_ignore, ignore it.
        ignored = lambda x: True in (x in char_range for char_range in to_ignore)

        sep_pos = self._search(separator, text)
        
        if sep_pos and to_ignore:
            sep_pos = list(filter(lambda pos: not ignored(pos), sep_pos))

        return sorted(sep_pos)

    def get_parsing_exceptions(self, text):
        """
        Returns a list of CharRanges of every strings and comments in the text.
        Returns empty list if no strings or comments are found.
        """
        ranges = []

        exception_tokens_pos = self._exception_tokens(text)

        while exception_tokens_pos:
            except_start = exception_tokens_pos[0]
            except_length = self.stmt_cutter(text[except_start:])

            #if there is no separator found (the except_length is -1), that means the exception
            #continues to the next line.
            if except_length == -1:
                except_end = len(text)
            else:
                except_end = except_start + except_length

            new_range = CharRange(except_start, except_end)
            ranges.append(new_range)

            #Dump every exception tokens inside the defined range.
            exception_tokens_pos = list(filter(lambda pos: pos > except_end, exception_tokens_pos))

        return ranges

    def get_statement_end(self, text, separator, do_exception_checking=True):
        """
        Returns an index in which the current statement ends, or -1 if no separator are found in the text.
        The index is the first separator occurrence in the text from get_occurrences.

        The do_exception_checking is forwarded to get_occurrences, see the function's docstring for more infromation.
        """
        
        valid_sep_pos = -1

        sep_pos = self.get_occurrences(text, separator, do_exception_checking)
        if sep_pos:
            #use the first instance of the separator found (the one with smallest index)
            valid_sep_pos = min(sep_pos)
        
        offset = len(separator) #Determine the offset, because we want to cut AFTER the separator.
        cut_pos = valid_sep_pos + offset if valid_sep_pos > -1 else -1
        return cut_pos

    def lines(self):
        """Reads temporary file per-line."""

        with open(TEMPFILE_PATH) as file:
            for line in file:
                yield line

    def _extract_substmt(self, text):
        """
        Extracts comments inserted inside a statement.
        Returns the statement (and any comments found) as a list.
        """

        no_substmts = [tokendicts.single_comment, tokendicts.multi_comment, tokendicts.preprocessor]
        substmts = []

        #if it's comments or include statements, no need to reanalyze statement.
        if self._starts_with(no_substmts, text):
            pass
        else:
            while self._first(tokendicts.comments, text) > -1:
                start_cut = self._first(tokendicts.comments, text)
                cut_len = self.stmt_cutter(text[start_cut:])
                end_cut = start_cut + cut_len
                #text on the left side are right-stripped and the text on the right are left-stripped,
                #to cut any extra whitespace/next lines between them.
                comment, text = text[start_cut:end_cut], text[:start_cut].rstrip() + " " + text[end_cut:].lstrip()
                substmts.append(comment)

        substmts.append(text)
        return map(lambda text: text.strip(), substmts)

    def stmt_cutter(self, text):
        """Returns a number, which is where the current statement ends. Returns -1 if the statement isn't ending in the text."""

        line = str(text).lstrip()
        whitespace_offset = len(text) - len(line)

        end_pos = -1
        #if it's one-line comment or include statement...
        if (self._starts_with(tokendicts.single_comment, line) 
            or self._starts_with(tokendicts.preprocessor, line)):
            end_pos = self.get_statement_end(line, '\n', do_exception_checking=False)
        #if it's one line comment...
        elif self._starts_with(tokendicts.multi_comment, line):
            end_pos = self.get_statement_end(line, '*/', do_exception_checking=False)
        #If it's string...
        elif self._starts_with(tokendicts.string_identifiers, line):
            end_pos = self.get_string_length(line)
        #if it's a start of new code block...
        elif self._starts_with(tokendicts.curly_left, line):
            end_pos = self.get_statement_end(line, '{')
        #if it's the end of a code block...
        elif self._starts_with(tokendicts.curly_right, line):
            end_pos = self.get_statement_end(line, '}')
        #if it's a declaration...
        elif self._starts_with(tokendicts.datatypes, line):
            end_pos = self.get_declaration_end(line)
        #if it's conditionals...
        elif self._starts_with(tokendicts.conditionals, line):
            end_pos = self.get_bracket_end(line)
        #if it's do loop....
        elif self._starts_with(tokendicts.dowhile_loop, line):
            end_pos = self.get_statement_end(line, "do")
        #if it's while loop....
        elif self._starts_with(tokendicts.while_loop, line):
            end_pos = self.get_declaration_end(line)
        #if it's for loop....
        elif self._starts_with(tokendicts.for_loop, line):
            end_pos = self.get_bracket_end(line)
        #If it isn't everything, default to semicolon
        else:
            end_pos = self.get_statement_end(line, ';')

        cut_pos = whitespace_offset + end_pos if end_pos > -1 else -1
        return cut_pos

    def read(self, filepath):
        """
        Reads file and rewrites it
        into the designated temporary file path.
        """

        with open(filepath, "r") as file_input:
            
            raw_input = file_input.read()
            with open(TEMPFILE_PATH, "w") as temp_file:
                temp_file.write(raw_input)

    def statements(self, filepath=None):
        """Returns temporary file contents as an iterable of separated C statements."""

        #Prepare the temporary file
        if filepath:
            self.read(filepath)

        prev_line = ""

        for line in self.lines():
            cur_line = prev_line + line
            while len(cur_line) > 0:
                cut_pos = self.stmt_cutter(cur_line)  

                if cut_pos == -1:
                    break
                else:
                    next_stmt, cur_line = cur_line[:cut_pos], cur_line[cut_pos:]
                    for stmt in self._extract_substmt(next_stmt.strip()):
                        #Scrap empty strings.
                        if len(stmt) > 0:
                            yield stmt
            
            prev_line = cur_line

        if len(prev_line) > 0:
            yield prev_line.strip()

        raise StopIteration 


    def _search(self, token, text):
        """
        Find all instances of token(s) in text. Supports single (string) and multiple (list, dictionary) tokens.
        Returns a list of indexes in which the token start. If there is no token instance in the text, it returns empty list.
        (Supports overlapping cases)
        """
        if isinstance(token, str):
            return self._list(token, text)
        if isinstance(token, dict):
            results = [self._list(token_item, text) for key, token_item in token.items()]
        elif isinstance(token, list):
            results = [self._list(token_item, text) for token_item in token]

        flattened_results = list(itertools.chain.from_iterable(results))
        flattened_results.sort() 
        return flattened_results

    def _list(self, token, text):
        """
        Find all instances of token in text. Only supports a token string.
        Returns a list of indexes in which the token start. If there is no token instance in the text, it returns empty list.
        (Supports overlapping cases)
        """

        result = []
        token_len = len(token)
        for i in range(len(text)):
            if token == text[i:i+token_len]:
                result.append(i)

        return result 

    def _first(self, tokens, text):
        """
        Find the first instance of any token from the tokens dictionary on the text string.
        Returns -1 when there is no instance of any token in the string.
        """

        findall = [text.find(token) for key, token in tokens.items()]
        found = list(filter(lambda pos: pos > -1, findall))

        return min(found) if found else -1

    def _starts_with(self, tokens, statement):
        """
        Returns True if a string statement starts with the tokens variable
        (tokens might be a dict, list, or string)
        """

        if isinstance(tokens, dict):
            return True in (statement.startswith(token) for token in tokens.values())
        elif isinstance(tokens, list):
            return True in (statement.startswith(token) for token in tokens)
        elif isinstance(tokens, str):
            return statement.startswith(tokens)

        return ValueError("Token is not a string, list, or dictionary")

    def get_string_length(self, text):
        """
        Returns an index in which the first string in the text ends. Returns -1 if no string are ending.
        (The text parameter must start with either single or double quotes)
        """
        
        #Do a sanity check; is the text really a string?
        if(not self._starts_with(tokendicts.string_identifiers, text)):
            print(f"ERROR! The text ({text}) is not a string, but skip_text() is called on it.")
            return -1

        #What we're looking for is either single or double token; check the first character to determine which.
        cur_string_delimiter = text[0]
        found = False

        #Start from one to account for the first character (the first single/double quote)
        for idx, char in enumerate(text[1:], 1):
            #If the current token is the same as the one starting the string
            #(either single or double quote)
            if char == cur_string_delimiter:
                #If the last character in current string is backslash, it means
                #that the delimiter is escaped; continue.
                if text[idx-1] == "\\":
                    pass
                #else it means that the current string is ending. Break from loop
                else:
                    found = True
                    break
        
        return idx if found else -1

