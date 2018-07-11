import transrules as rules

from collections import namedtuple

#TODO: delete all unnecessary commented print-debugs! 

class Deformat:

    _tempfile_path = "temp/source.txt"

    def __init__(self, filepath):
        self.rules = rules.TranslationHelper()        
        self.CharRange = namedtuple("CharRange", ['start', 'end'])
        #Prepare the temporary file
        self._filepath = filepath
        self._readfile()

    def scan_parsing_exceptions(self, text):
        
        unchecked_text = text
        text_length = len(text)
        offset = 0
        ranges = []

        comment_start = self.rules.findstring(unchecked_text) 
        while comment_start > -1:
            offset = text_length - len(unchecked_text)

            comment_length = self._skip_text(unchecked_text[comment_start:])
            if comment_length == -1:
                comment_end = len(unchecked_text)
            else:
                comment_end = comment_start + comment_length

            new_range = self.CharRange(offset + comment_start, offset + comment_end)
            ranges.append(new_range)

            unchecked_text = unchecked_text[comment_end+1:]
            # print(f"Text: {unchecked_text}")
            comment_start = self.rules.findstring(unchecked_text)

        return ranges

    def _determine_decl_end(self, text):
        """
        Determines whether a declaration sentence ends with "{" or ";", 
        or in other words, whether it's a variable or function declaration
        """        
        curlybrace_pos = text.find("{")
        semicolon_pos = text.find(";")

        if curlybrace_pos > 0 and curlybrace_pos < semicolon_pos:
            return self._determine_statement_end(text, "{")
        else:
            return self._determine_statement_end(text, ";")

    def _determine_bracket_end(self, text):
        # print(f"determine_bracket_end called, the text: {text}")
        first_open_bracket = text.find("(")
    
        if first_open_bracket == -1:
            return -1
        else:
            char_idx = first_open_bracket+1

            bracket_end_idx = -1
            open_bracket_count = 1

            while(char_idx < len(text)):
                cur_char = text[char_idx]
                if cur_char == "(":
                    open_bracket_count += 1
                elif cur_char == ")":
                    open_bracket_count -= 1
                
                if open_bracket_count == 0:
                    bracket_end_idx = char_idx
                    break

                char_idx += 1
                
        bracket_closed = open_bracket_count == 0
        # print(f"is bracket closed? {bracket_closed}")

        if bracket_closed:
            # print(f"bracket closed at {bracket_end_idx + 1} from {len(text)} chars")
            return bracket_end_idx + 1
        else:
            return -1

    def _determine_statement_end(self, text, separator=None, bypass_exception_checking=False):

        # print(f"determine_statement_end called. Text is {text}")

        if separator is None:
            return -1

        sep_pos = self.rules.findall(text, separator)
        #If there's no separator found, that means the statement isn't over yet.
        if len(sep_pos) == 0:
            return -1
        
        #If it's a comment, bypass parsing exception checking 
        to_ignore = [] if bypass_exception_checking else self.scan_parsing_exceptions(text)

        if len(to_ignore) > 0:
            print("Sanity check")
            print(f"Statement length is {len(text)}, content: {text}")
        
            print(f"to ignore: {to_ignore}")
            print(f"separator positions: {sep_pos}")
            valid_sep_pos = -1
            for pos in sep_pos:
                for char_range in to_ignore:
                    if not char_range.start <= pos <= char_range.end:
                        valid_sep_pos = pos
                        break
                if valid_sep_pos != -1:
                    break
        else:
            valid_sep_pos = sep_pos[0]
        
        offset = len(separator) #Determine the offset, because we want to cut AFTER the separator.
        cut_pos = valid_sep_pos + offset if valid_sep_pos > -1 else -1
        return cut_pos

    def _extract_substmt(self, text):
        """
        Extracts comments inserted inside a statement.
        Returns the statement (and any comments found) as a list.
        """
        original_text = text

        substmts = []

        #if it's comments or include statements, no need to reanalyze statement.
        if self.rules.is_singlecomment(text) or self.rules.is_multicomment(text) or self.rules.is_include(text):
            pass 
        else:
            while self.rules.findcomment(text) > -1:
                # print(f"original text is: {original_text} ~")
                # print(f"text is: {text} ~")
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
        """Determine where a statement ends and its separator.
        Returns the correct ending character for the line string, according
        to the first characters of the string.
        """

        #TODO: How do you handle separator occurrence in strings comments?
        line = str(text).lstrip()
        whitespace_offset = len(text) - len(line)

        end_pos = -1
        if self.rules.is_singlecomment(line) or self.rules.is_include(line):
            end_pos = self._determine_statement_end(line, '\n', bypass_exception_checking=True)
        elif self.rules.is_multicomment(line):
            end_pos = self._determine_statement_end(line,  '*/', bypass_exception_checking=True)
        elif self.rules.is_block_start(line):
            end_pos = self._determine_statement_end(line, '{')
        elif self.rules.is_block_end(line):
            end_pos = self._determine_statement_end(line,  '}')
        elif self.rules.is_declaration(line):
            end_pos = self._determine_decl_end(line)
        elif self.rules.is_conditional(line) or self.rules.is_loop(line):
            end_pos = self._determine_bracket_end(line)
        else: 
            end_pos = self._determine_statement_end(line,  ';')

        cut_pos = whitespace_offset + end_pos if end_pos > -1 else -1
        return cut_pos

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
                    # print(f"{cur_line[:cut_pos]}, {cur_line[cut_pos:]}")
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


    def _skip_text(self, text):
        """
        Merges every tokens between single or double quotes (including the quotes) into one. 
        Leave the rest as it is, except that whitespaces outside quotes is removed.
        
        Will handle escaped quotes correctly, but fails silently if there is non-even number of quotes 
        (the last quote and all quote afterwards will be dumped)
        """
        
        #Do a sanity check; is the text really a string?
        if(not self.rules.is_string(text)):
            print(f"ERROR! The text ({text}) is not a string, but skip_text() is called on it.")
            return -1

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

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js