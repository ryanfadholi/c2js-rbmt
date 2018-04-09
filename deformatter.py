import c2js_runner
import transrules as rules


class Deformat:

    _tempfile_path = "temp/source.txt"

    def stmt_validate(self, text, tokens):
        #TODO: add docstring
        if isinstance(tokens, list):
            return True in (text.startswith(token) for token in tokens)
        elif isinstance(tokens, str):
            return text.startswith(tokens)
        else:
            return False
        
    #Functions to check if a string is a conditional/looping control flow statement.
    is_conditional = lambda self, text: self.stmt_validate(text, rules.conditionals)
    is_declaration = lambda self, text: self.stmt_validate(text, rules.datatypes)
    is_include = lambda self, text: self.stmt_validate(text, rules.include)
    is_loop = lambda self, text: self.stmt_validate(text, rules.loops)
    is_multicomment = lambda self, text: self.stmt_validate(text, rules.multi_comment)
    is_singlecomment = lambda self, text: self.stmt_validate(text, rules.single_comment)

    def __init__(self, filepath):
        #Prepare the temporary file
        self._filepath = filepath
        self._readfile()

    def _determine_decl_end(self, text):
        curlybrace_pos = text.find("{")
        semicolon_pos = text.find(";")

        if curlybrace_pos > 0 and curlybrace_pos < semicolon_pos:
            return "{"
        else:
            return ";"

    def _extract_substmt(self, text):
        #TODO: extract comments from all statements
        #TODO: extract expressions from if/for/while

        substmts = [text]
        return substmts

        #if it's comments, no need to reanalyze statement.
        if self.is_singlecomment(text) or self.is_multicomment(text):
            return substmts

        if self.is_declaration(text):
            if text.find("//") != -1:
                pass



    def _readfile(self):
        with open(self._filepath, "r") as file_input:
            
            raw_input = file_input.read()
            
            with open(self._tempfile_path, "w") as temp_file:
                temp_file.write(raw_input)

    def _lines_generator(self):
        with open(self._tempfile_path) as file:
            for line in file:
                yield line

    def _statements_generator(self):

        #TODO: Refine rule to correctly separate function/for/if statements

        prev_line = ""

        counter = 0
        for line in self._lines_generator():
            counter = counter + 1
            cur_line = prev_line + line
            while len(cur_line) > 0:
                cur_sep = self.stmt_sep(cur_line.lstrip()) #Determine separator for current statement
                
                sep_offset = len(cur_sep) #Determine the offset
                cut_pos = cur_line.find(cur_sep) + sep_offset #Find the first appearance of the substring
                
                # print("Current separator:", cur_sep, end="")
                # print("Line", str(counter), "Pos", str(cut_pos))

                if cur_line.find(cur_sep) == -1:
                    break
                else:
                    next_stmt, cur_line = cur_line[:cut_pos], cur_line[cut_pos:]
                    for stmt in self._extract_substmt(next_stmt.strip()):
                        yield stmt
            
            prev_line = cur_line

        if len(prev_line) > 0:
            yield prev_line.strip()

        raise StopIteration 

    def stmt_sep(self, line):
        line = str(line).lstrip()

        if self.is_singlecomment(line) or self.is_include(line):
            return '\n'
        elif self.is_multicomment(line):
            return '*/'
        elif self.is_conditional(line) or self.is_loop(line):
            return '{'
        elif self.is_declaration(line):
            return self._determine_decl_end(line)
        else: 
            return ';'

    @property
    def lines(self):
        return [line for line in self._lines_generator()]

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js