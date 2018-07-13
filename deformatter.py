import transrules as rules

import itertools

from charrange import CharRange
from collections import namedtuple

class Deformat:

    _tempfile_path = "temp/source.txt"

    def __init__(self, filepath, debug_mode=False):

        self.debug_mode = debug_mode
        self.rules = rules.TranslationHelper()

        #Prepare the temporary file
        self._filepath = filepath
        self._readfile()

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

    def get_bracket_end(self, text):
        """
        Returns an index where the first bracket set of the text ends. Works even if there is nested brackets present.
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
        Declaration could mean a variable or function declaration, and the function will adapt depending on what it assume the declaration is.
        """        
        curlybrace_pos = self.get_statement_end(text, "{")
        semicolon_pos = self.get_statement_end(text, ";")

        if curlybrace_pos > 0 and curlybrace_pos < semicolon_pos:
            return self.get_bracket_end(text)
        else:
            return semicolon_pos

    def get_exception_tokens(self, text):
        """
        Returns a list of index of every occurrence of ', ", //, and /*.
        (Which may sign as a start of exception range)

        Returns empty list if none are found.
        """
        quotes_pos = self.rules.find_all_string(text)
        comment_start_pos = self.rules.find_all_comment(text)

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

        sep_pos = self.rules.findall(text, separator)

        if(self.debug_mode):
                print(f"ignore range: {to_ignore}")
                print(f"separator positions: {sep_pos}")
        
        if sep_pos and to_ignore:
            sep_pos = list(filter(lambda pos: not ignored(pos), sep_pos))

        return sorted(sep_pos)

    def get_parsing_exceptions(self, text):
        """
        Returns a list of CharRanges of every strings and comments in the text. 
        Returns empty list if no strings or comments are found.
        """
        ranges = []

        exception_tokens_pos = self.get_exception_tokens(text)

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
        separator := str
        Returns an index in which the current statement ends, or -1 if no separator are found in the text.
        The index is the first separator occurrence in the text from get_occurrences.

        The do_exception_checking is forwarded to get_occurrences, see the function's docstring for more infromation.
        """

        if(self.debug_mode):
            print(f"Statement length is {len(text)}, content: {text}")
        
        valid_sep_pos = -1

        sep_pos = self.get_occurrences(text, separator, do_exception_checking)
        if sep_pos:
            #use the first instance of the separator found (the one with smallest index)
            valid_sep_pos = min(sep_pos)
        
        offset = len(separator) #Determine the offset, because we want to cut AFTER the separator.
        cut_pos = valid_sep_pos + offset if valid_sep_pos > -1 else -1
        return cut_pos

    def get_string_length(self, text):
        """
        Returns an index in which the first string in the text ends. Returns -1 if no string are ending.
        (The text parameter must start with either single or double quotes)
        """
        
        #Do a sanity check; is the text really a string?
        if(not self.rules.is_string(text)):
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

    def _extract_substmt(self, text):
        """
        Extracts comments inserted inside a statement.
        Returns the statement (and any comments found) as a list.
        """

        substmts = []

        #if it's comments or include statements, no need to reanalyze statement.
        if self.rules.is_singlecomment(text) or self.rules.is_multicomment(text) or self.rules.is_include(text):
            pass 
        else:
            while self.rules.findcomment(text) > -1:
                start_cut = self.rules.findcomment(text)
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
        if self.rules.is_singlecomment(line) or self.rules.is_include(line):
            end_pos = self.get_statement_end(line, '\n', do_exception_checking=False)
        elif self.rules.is_multicomment(line):
            end_pos = self.get_statement_end(line,  '*/', do_exception_checking=False)
        elif self.rules.is_string(line):
            end_pos = self.get_string_length(line)
        elif self.rules.is_block_start(line):
            end_pos = self.get_statement_end(line, '{')
        elif self.rules.is_block_end(line):
            end_pos = self.get_statement_end(line,  '}')
        elif self.rules.is_declaration(line):
            end_pos = self.get_declaration_end(line)
        elif self.rules.is_conditional(line) or self.rules.is_loop(line):
            end_pos = self.get_bracket_end(line)
        else: 
            end_pos = self.get_statement_end(line,  ';')

        cut_pos = whitespace_offset + end_pos if end_pos > -1 else -1
        return cut_pos

    def _readfile(self):
        """
        Reads file located in self._filepath, and rewrites it
        into the designated path (self._tempfile_path).
        """

        with open(self._filepath, "r") as file_input:
            
            raw_input = file_input.read()
            with open(self._tempfile_path, "w") as temp_file:
                temp_file.write(raw_input)

    def _lines_generator(self):
        """Reads temporary file per-line."""
        with open(self._tempfile_path) as file:
            for line in file:
                yield line

    def _statements_generator(self):
        """Returns temporary file's content as an iterable of separated C statements."""

        prev_line = ""

        for line in self._lines_generator():
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

    @property
    def lines(self):
        return [line for line in self._lines_generator()]

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js