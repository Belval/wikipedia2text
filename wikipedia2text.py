import sys
import os
import re

from bz2 import BZ2Decompressor

def main(args):
    """
        wikipedia2text.py  [input_file] [output_file]
    """

    input_file = args[1]
    output_file = args[2]

    regex_remove_tag = re.compile(r"<.*?>")
    char_to_remove = ['{', '}', '[', ']', '<', '>', '=', '&', '"', '(', ')', '|', '/', '\\', '*', '\'', '#', ':']
    translation_table = str.maketrans(''.join(char_to_remove), ''.join([' '] * len(char_to_remove)))

    # We start by decompressing the file
    print('Starting decompression')
    with open(output_file + '_decompressed', 'wb') as fout, open(input_file, 'rb') as fin:
        decompressor = BZ2Decompressor()
        for i, data in enumerate(iter(lambda : fin.read(1000 * 1024), b'')):
            if i % 100 == 0:
                print(str(i) + ' MB processed')
            fout.write(decompressor.decompress(data))

    # We then remove whatever wouldn't go well in word2vec
    print('Starting line conversion')
    with open(output_file, 'w') as fout, open(output_file + '_decompressed', 'r') as fin:
        count = 0
        for line in fin:
            if count % 10000 == 0:
                print(str(count) + ' lines processed')
            fout.write(' '.join(regex_remove_tag.sub(' ', line).translate(translation_table).split()) if len(line) > 100 else '')
            count += 1

    # Finally we delete the file!
    print('Cleaning up')
    os.remove(output_file + '_decompressed')

if __name__=='__main__':
    main(sys.argv)
