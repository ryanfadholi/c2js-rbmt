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

    def load(self, source_path):
        """Loads the given source_path contents to a temporary file."""
        self._deformatter.read(source_path)

    def process(self, console_print=False, test_mode=False):
        """
        Processes the contents of the designated temporary file
        (Must be prepared first by the load() method)
        The results are then saved into another designated temporary file.
        """

        #Test values
        count_decl = 0
        count_init = 0
        count_func_calls = 0
        count_io = 0
        count_cond = 0
        count_loop = 0
        count_comment = 0
        count_etc = 0

        if test_mode:
            #suppress notices & warnings from modules
            sys.stdout = open(os.devnull, 'w')
            console_print = False

        statements = [self._sltransfer.translate(self._postagger.tag(stmt)) 
                      for stmt in self._deformatter.statements()]
        self._postgenerator.write(statements)

        if console_print:
            for statement in statements:
                print(statement)

        if test_mode:
            #re-enable console output
            sys.stdout = sys.__stdout__

            for statement in statements:
                if statement.tag == constants.DECLARATION_TAG:
                    count_decl += 1
                    for token in statement:
                        if token.tag == tokens.tag_assign:
                            count_init += 1
                            break
                elif statement.tag == constants.FUNCTION_TAG:
                    count_decl += 1
                elif statement.tag in [constants.INITIATION_TAG, constants.DECREMENT_INCREMENT_TAG]:
                    count_init += 1
                elif statement.tag == constants.FUNCTION_CALL_TAG:
                    count_func_calls += 1
                elif statement.tag in [constants.INPUT_TAG, constants.OUTPUT_TAG]:
                    count_io += 1
                elif statement.tag == constants.CONDITIONAL_TAG:
                    count_cond += 1
                elif statement.tag == constants.LOOP_TAG:
                    count_loop += 1
                elif statement.tag in [constants.MULTI_COMMENT_TAG, constants.SINGLE_COMMENT_TAG]:
                    count_comment += 1
                #Ignore blocks
                elif statement.tag in [constants.BLOCK_START_TAG, constants.BLOCK_END_TAG]:
                    continue
                else:
                    count_etc += 1

            #Deklarasi Variabel/Fungsi
            print(count_decl)
            #Inisialisasi/Inisiasi
            print(count_init)
            #Pemanggilan Fungsi
            print(count_func_calls)
            #Masukan/Keluaran
            print(count_io)
            #Kondisional
            print(count_cond)
            #Pengulangan
            print(count_loop)
            #Komentar
            print(count_comment)
            #Lain-lain
            print(count_etc)

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
    parser.add_argument('-t', "--test_mode", help="Turn on test mode", action="store_true")
    args = parser.parse_args()

    instance = C2js()
    instance.load(args.source_path)

    do_print = not args.no_print
    test_mode = args.test_mode
    instance.process(do_print, test_mode)
    instance.save(args.result_path)
