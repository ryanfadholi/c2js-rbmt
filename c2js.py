import deformatter
import postagger
import sltransfer
import postgenerator
import reformatter

#TODO: Enable command-line arguments

SOURCE_TEMPFILE_PATH = deformatter.TEMPFILE_PATH
OUTPUT_TEMPFILE_PATH = postgenerator.TEMPFILE_PATH

class C2js:
    def __init__(self):
        self._deformatter = deformatter.Deformatter()
        self._postagger = postagger.POSTagger()
        self._sltransfer = sltransfer.StructuralLexicalTransfer()
        self._postgenerator = postgenerator.PostGenerator()
        self._reformatter = reformatter.Reformatter()

    def load(self, source_path):
        """Loads the given source_path contents to a temporary file."""
        self._deformatter.read(source_path)

    def process(self, console_print=False):
        """
        Processes the contents of the designated temporary file
        (Must be prepared first by the load() method)
        The results are then saved into another designated temporary file.
        """
        stmts = [stmt for stmt in self._deformatter.statements()]
        tagged_stmts = map(self._postagger.tag, stmts)
        identified_stmts = list(map(self._sltransfer.translate, tagged_stmts))

        if console_print:
            for stmt in identified_stmts:
                print(stmt)

        self._postgenerator.write(identified_stmts)

    def save(self, output_path):
        """
        Copies the contents of a result temporary file
        (genreated by the process() method)
        into the given output_path.
        """
        self._reformatter.write(output_path)


if __name__ == "__main__":
    instance = C2js()
    instance.load("example.c")
    instance.process(True)
    instance.save("new_result.js")
