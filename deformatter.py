import itertools

import constants
import tokens as tkn

class Deformatter:

    def _bracket_end(self, text):
        """
        Returns an index where the first bracket set of the text ends, 
        Works even if there is nested brackets present.
        Returns -1 if the first bracket set is not complete/no bracket sets are found. 
        """
        open_brackets = self._search("(", text, do_exception_checking=True)
        close_brackets = self._search(")", text, do_exception_checking=True)

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

    def _declaration_end(self, text):
        """
        Returns an index where the declaration statement ends. Returns -1 if the statement isn't ending yet.
        Declaration could mean a variable or function declaration,
        and the function will adapt depending on what it assumes the declaration is.
        """
        curlybrace_pos = self._statement_end("{", text)
        semicolon_pos = self._statement_end(";", text)
        assignment_pos = self._statement_end("=", text)

        #If there's curly brace and it's placed before a semicolon: 
        if curlybrace_pos > 0 and curlybrace_pos < semicolon_pos:
            #If there's assignment before the curly brace, it's a pre-filled array
            if assignment_pos > 0 and assignment_pos < curlybrace_pos:
                return semicolon_pos
            #Else it's a function declaration
            return self._bracket_end(text)
        #If there's no curly brace or a semicolon comes before it, it's a normal variable declaration.
        else:
            return semicolon_pos

    def _exceptions(self, text):
        """
        Returns a list of tuples representing ranges of every strings 
        and comments in the text.
        Returns empty list if no strings or comments are found.
        """
        quotes_pos = self._search(tkn.string_identifiers, text)
        comment_start_pos = self._search(tkn.comments, text)

        exception_tokens_pos = list(itertools.chain.from_iterable((quotes_pos, comment_start_pos)))
        exception_tokens_pos.sort()

        ranges = []

        #This bit is skipped when there's no exceptions.
        while exception_tokens_pos:
            except_start = exception_tokens_pos[0]
            except_length = self._next(text[except_start:])

            #if there is no separator found (the except_length is -1), that means the exception
            #continues to the next line.
            if except_length == -1:
                except_end = len(text)
            else:
                except_end = except_start + except_length

            new_range = (except_start, except_end)
            ranges.append(new_range)

            #Dump every exception tokens inside the defined range.
            exception_tokens_pos = list(filter(lambda pos: pos > except_end, exception_tokens_pos))

        return ranges

    def _first(self, tokens, text):
        """
        Find the first instance of any token from the tokens dictionary on the text string.
        Returns -1 when there is no instance of any token in the string.
        """

        findall = [text.find(token) for key, token in tokens.items()]
        found = list(filter(lambda pos: pos > -1, findall))

        return min(found) if found else -1

    def _next(self, text):
        """Returns a number, which is where the current statement ends. Returns -1 if the statement isn't ending in the text."""

        line = str(text).lstrip()
        whitespace_offset = len(text) - len(line)

        end_pos = -1
        #if it's one-line comment or include statement...
        if (self._starts_with(tkn.single_comment, line)
            or self._starts_with(tkn.preprocessor, line)):
            end_pos = self._statement_end('\n', line, do_exception_checking=False)
        #if it's one line comment...
        elif self._starts_with(tkn.multi_comment, line):
            end_pos = self._statement_end('*/', line, do_exception_checking=False)
        #If it's string...
        elif self._starts_with(tkn.string_identifiers, line):
            end_pos = self._string_end(line)
        #if it's a start of new code block...
        elif self._starts_with(tkn.curly_left, line):
            end_pos = self._statement_end('{', line)
        #if it's the end of a code block...
        elif self._starts_with(tkn.curly_right, line):
            end_pos = self._statement_end('}', line)
        #if it's a declaration...
        elif self._starts_with(tkn.datatypes, line):
            end_pos = self._declaration_end(line)
        #if it's conditionals...
        elif self._starts_with(tkn.conditionals, line):
            end_pos = self._bracket_end(line)
        #if it's do loop....
        elif self._starts_with(tkn.dowhile_loop, line):
            end_pos = self._statement_end("do", line)
        #if it's while loop....
        elif self._starts_with(tkn.while_loop, line):
            end_pos = self._declaration_end(line)
        #if it's for loop....
        elif self._starts_with(tkn.for_loop, line):
            end_pos = self._bracket_end(line)
        #If it isn't everything, default to semicolon
        else:
            end_pos = self._statement_end(';', line)

        cut_pos = whitespace_offset + end_pos if end_pos > -1 else -1
        return cut_pos

    def _search(self, token, text, do_exception_checking=False):
        """
        Returns the list of index of every token occurrence in text. Returns empty list if no occurence of token is found.
        (The list are sorted from the smallest index to largest)
        
        if do_exception_checking is set to True, the function will call _exceptions(),
        and any occurrence found within the ranges returned by that function will be considered invalid and excluded from the result.
        """
        
        if isinstance(token, str):
            results = self._search_single(token, text)
        elif isinstance(token, dict):
            results = [self._search_single(token_item, text) for key, token_item in token.items()]
            results = list(itertools.chain.from_iterable(results))
        elif isinstance(token, list):
            results = [self._search_single(token_item, text) for token_item in token]
            results = list(itertools.chain.from_iterable(results))
        
        if do_exception_checking:
            to_ignore = self._exceptions(text)
            #If x is in range of any tuple inside to_ignore, ignore it.
            ignored = lambda x: True in (char_range[0] <= x <= char_range[1] for char_range in to_ignore)
            results = list(filter(lambda pos: not ignored(pos), results))

        return sorted(results)

    def _search_single(self, token, text):
        """
        Find all instances of token in text. Only supports a single token string.
        Returns a list of indexes in which the token start. If there is no token instance in the text, it returns empty list.
        (Supports overlapping cases)
        """

        result = []
        token_len = len(token)
        for i in range(len(text)):
            if token == text[i:i+token_len]:
                result.append(i)

        return result

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

    def _statement_end(self, separator, text, do_exception_checking=True):
        """
        Returns an index in which the current statement ends, or -1 if no separator are found in the text.
        The index is the first separator occurrence in the text from _search.

        The do_exception_checking is forwarded to _search, see the function's docstring for more infromation.
        """
        
        valid_sep_pos = -1

        sep_pos = self._search(separator, text, do_exception_checking)
        if sep_pos:
            #use the first instance of the separator found (the one with smallest index)
            valid_sep_pos = min(sep_pos)
        
        offset = len(separator) #Determine the offset, because we want to cut AFTER the separator.
        cut_pos = valid_sep_pos + offset if valid_sep_pos > -1 else -1
        return cut_pos

    def _string_end(self, text):
        """
        Returns an index in which the first string in the text ends. Returns -1 if no string are ending.
        (The text parameter must start with either single or double quotes)
        """
        
        #Do a sanity check; is the text really a string?
        if(not self._starts_with(tkn.string_identifiers, text)):
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

    def _substatements(self, text):
        """
        Extracts comments inserted inside a statement.
        Returns the statement (and any comments found) as a list.
        """

        no_substmts = [tkn.single_comment, tkn.multi_comment, tkn.preprocessor]
        substmts = []

        #if it's comments or include statements, no need to reanalyze statement.
        if self._starts_with(no_substmts, text):
            pass
        else:
            while self._first(tkn.comments, text) > -1:
                start_cut = self._first(tkn.comments, text)
                cut_len = self._next(text[start_cut:])
                end_cut = start_cut + cut_len
                #text on the left side are right-stripped and the text on the right are left-stripped,
                #to cut any extra whitespace/next lines between them.
                comment, text = text[start_cut:end_cut], text[:start_cut].rstrip() + " " + text[end_cut:].lstrip()
                substmts.append(comment)

        substmts.append(text)
        return map(lambda text: text.strip(), substmts)

    def lines(self):
        """Reads temporary file per-line."""

        with open(constants.INPUT_TEMPFILE_PATH) as file:
            for line in file:
                yield line

    def read(self, filepath):
        """
        Reads file and rewrites it
        into the designated temporary file path.
        """

        with open(filepath, "r") as file_input:
            
            raw_input = file_input.read()
            with open(constants.INPUT_TEMPFILE_PATH, "w") as temp_file:
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
                cut_pos = self._next(cur_line)

                if cut_pos == -1:
                    break
                else:
                    next_stmt, cur_line = cur_line[:cut_pos], cur_line[cut_pos:]
                    for stmt in self._substatements(next_stmt.strip()):
                        #Scrap empty strings.
                        if len(stmt) > 0:
                            yield stmt
            
            prev_line = cur_line

        if len(prev_line.strip()) > 0:
            yield prev_line.strip()

        return
