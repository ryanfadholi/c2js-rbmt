import transrules as rules

class Deformat:

    _tempfile_path = "temp/source.txt"

    def __init__(self, filepath):
        self.rules = rules.TranslationHelper()        

        #Prepare the temporary file
        self._filepath = filepath
        self._readfile()

    def _determine_decl_end(self, text):
        """
        Determines whether a sentence ends with "{" or ";".
        Should only be called when the sentence started with data type.
        (Thus it's ambiguous whether it's a variable or function declaration)
        """        
        curlybrace_pos = text.find("{")
        semicolon_pos = text.find(";")

        if curlybrace_pos > 0 and curlybrace_pos < semicolon_pos:
            return "{"
        else:
            return ";"

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
        """Determine where a statement ends and its separator."""
        separator = self.stmt_sep(text.lstrip()) #Determine separator for current statement

        sep_pos = text.find(separator)        
        offset = len(separator) #Determine the offset
        cut_pos = sep_pos + offset if sep_pos > -1 else -1
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
                    next_stmt, cur_line = cur_line[:cut_pos], cur_line[cut_pos:]
                    for stmt in self._extract_substmt(next_stmt.strip()):
                        #Scrap empty strings.
                        if len(stmt) > 0:
                            yield stmt
            
            prev_line = cur_line

        if len(prev_line) > 0:
            yield prev_line.strip()

        raise StopIteration 

    def stmt_sep(self, line):
        """
        Returns the correct ending character for the line string, according
        to the first characters of the string.
        """

        line = str(line).lstrip()

        if self.rules.is_singlecomment(line) or self.rules.is_include(line):
            return '\n'
        elif self.rules.is_multicomment(line):
            return '*/'
        elif self.rules.is_conditional(line) or self.rules.is_loop(line):
            return '{'
        elif self.rules.is_block_end(line):
            return '}'
        elif self.rules.is_declaration(line):
            return self._determine_decl_end(line)
        else: 
            return ';'

    @property
    def lines(self):
        return [line for line in self._lines_generator()]

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js