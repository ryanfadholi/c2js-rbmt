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

    def process(self, console_print=False, test_mode=False):
        """
        Processes the contents of the designated temporary file
        (Must be prepared first by the load() method)
        The results are then saved into another designated temporary file.
    
        If test_mode is set to True, returns stats of the translated file.
        Else it returns 0 if no errors happen.
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

        self._sltransfer.reset()
        statements = [self._sltransfer.translate(self._postagger.tag(stmt)) 
                      for stmt in self._deformatter.statements()]
        results = self._postgenerator.write(statements)

        source_stmt_count = len(list(self._deformatter.statements()))
        result_stmt_count = results

        if test_mode:
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
                elif statement.tag in [constants.CONDITIONAL_TAG, constants.SWITCH_TAG, constants.CASE_TAG]:
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

        translation_details = (
                    source_stmt_count, #Jumlah baris masukan
                    result_stmt_count, #Jumlah baris keluaran
                    count_decl, #Deklarasi Variabel/Fungsi
                    count_init, #Inisialisasi/Inisiasi
                    count_func_calls, #Pemanggilan Fungsi
                    count_io, #Masukan/Keluaran
                    count_cond, #Kondisional
                    count_loop, #Pengulangan
                    count_comment, #Komentar
                    count_etc #Lain-lain
        )

        if console_print:
            if test_mode:
                for detail in translation_details:
                    print(detail)
            else:
                for statement in statements:
                    print(statement) 

        return translation_details if test_mode else 0

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
    do_test = args.test_mode
    instance.process(do_print, do_test)
    instance.save(args.result_path)
