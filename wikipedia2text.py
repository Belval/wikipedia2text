import sys
import os
import re

from bz2 import BZ2Decompressor

def main(args):
    input_file = args[1]
    output_file = args[2]

    regex_remove_tag = re.compile(r"<.*?>")
    char_to_remove = ['{', '}', '[', ']', '<', '>', '=', '&', '"', '(', ')', '|', '/', '\\', '*', '\'', '#', ':']
    translation_table = str.maketrans(''.join(char_to_remove), ''.join([' '] * len(char_to_remove)))

    with open(output_file + '_decompressed', 'wb') as fout, open(input_file, 'rb') as fin:
        decompressor = BZ2Decompressor()
        for data in iter(lambda : fin.read(100 * 1024), b''):
            fout.write(decompressor.decompress(data))


    with open(output_file, 'w') as fout, open(output_file + '_decompressed', 'r') as fin:
        for line in fin.readlines():
            fout.write(' '.join(regex_remove_tag.sub(' ', line).translate(translation_table).split()) if len(line) > 100 else '')

if __name__=='__main__':
    main(sys.argv)
