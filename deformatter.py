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
        lines = self._lines_generator()
        prevline_leftover = ""

        for line in self._lines_generator():
            pass

    def determine_statement_end(self, line):
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