import argparse
import os
import sys

import constants
import deformatter
import postagger
import sltransfer
import postgenerator
import reformatter
import tokens

DEFAULT_SOURCE_FILE = "source.c"
DEFAULT_RESULT_FILE = "result.js"

class C2js:
    def __init__(self):
        self._deformatter = deformatter.Deformatter()
        self._postagger = postagger.POSTagger()
        self._sltransfer = sltransfer.StructuralLexicalTransfer()
        self._postgenerator = postgenerator.PostGenerator()
        self._reformatter = reformatter.Reformatter()

        source_temp_path, _f = os.path.split(constants.INPUT_TEMPFILE_PATH)
        result_temp_path, _f = os.path.split(constants.OUTPUT_TEMPFILE_PATH)
        
        #Create temporary path if not exists
        if not os.path.exists(source_temp_path):
            os.makedirs(source_temp_path)
        if not os.path.exists(result_temp_path):
            os.makedirs(result_temp_path)

    def load(self, source_path):
        """Loads the given source_path contents to a temporary file."""
        self._deformatter.read(source_path)

    def process(self, console_print=False):
        """
        Processes the contents of the designated temporary file
        (Must be prepared first by the load() method)
        The results are then saved into another designated temporary file.
        """

        self._sltransfer.reset()
        statements = [self._sltransfer.translate(self._postagger.tag(stmt)) 
                      for stmt in self._deformatter.statements()]
        self._postgenerator.write(statements)

        if console_print:
            for statement in statements:
                print(statement)

    def save(self, output_path):
        """
        Copies the contents of a result temporary file
        (genreated by the process() method)
        into the given output_path.
        """
        self._reformatter.write(output_path)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", help="C file to process", nargs='?', default=DEFAULT_SOURCE_FILE, type=str)
    parser.add_argument("result_path", help="Result file destination", nargs='?', default=DEFAULT_RESULT_FILE, type=str)
    parser.add_argument("-np", "--no_print", help="Disable statement print", action="store_true")
    args = parser.parse_args()

    instance = C2js()
    instance.load(args.source_path)

    do_print = not args.no_print
    instance.process(do_print)
    instance.save(args.result_path)
