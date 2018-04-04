class Deformat:

    _tempfile_path = "temp/source.txt"

    def __init__(self, filepath):
        #Prepare the temporary file
        self._filepath = filepath
        self._readfile()

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

        #TODO: Strip leading whitespace in statements
        #TODO: Refine rule to correctly separate function/for/if statements

        lines = self._lines_generator()
        prev_line = ""

        itera = 0
        for line in self._lines_generator():
            itera = itera + 1
            cur_line = prev_line + line
            while len(cur_line) > 0:
                cur_sep = self.stmt_sep(cur_line.lstrip()) #Determine separator for current statement
                print("Current separator:", cur_sep, end="")
                sep_offset = len(cur_sep) #Determine the offset
                cut_pos = cur_line.find(cur_sep) + sep_offset #Find the first appearance of the substring
                print("Line", str(itera), "Pos", str(cut_pos))
                if cur_line.find(cur_sep) == -1:
                    break
                else:
                    next_stmt, cur_line = cur_line[:cut_pos], cur_line[cut_pos:]
                    print(len(cur_line))
                    yield next_stmt
            
            prev_line = cur_line

        if len(prev_line) > 0:
            yield prev_line

        raise StopIteration 


    def stmt_sep(self, line):
        line = str(line).lstrip()

        if line.startswith("//") or line.startswith("#"):
            return '\n'
        elif line.startswith("/*"):
            return '*/'
        else:
            return ';'

    @property
    def lines(self):
        return [line for line in self._lines_generator()]