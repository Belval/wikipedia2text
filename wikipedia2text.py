import sys
import os
import uuid
import re
import argparse
import requests
import subprocess

from bz2 import BZ2Decompressor

def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(description='Generate a corpus from Wikipedia.')

    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        help="The output file",
        default="data.txt",
    )

    parser.add_argument(
        "-dl",
        "--download_languages",
        type=str,
        nargs="?",
        help="The languages to download and use, with 2 char code (en,fr,de,es) separated by commas",
        default="en"
    )

    parser.add_argument(
        "-i",
        "--input_files",
        nargs="+",
        help="The input files to use to build the corpus.",
    )

    parser.add_argument(
        "-m",
        "--mix_sentences",
        action="store_true",
        help="Define if the lines should be shuffled to allow for a more uniform distribution",
        default=True
    )

    return parser.parse_args()

def main(args):
    """
        wikipedia2text.py  [input_file] [output_file]
    """

    args = parse_arguments()

    input_files = args.input_files if args.input_files is not None else []
    output_file = args.output_file
    mix_sentences = args.mix_sentences
    download_languages = args.download_languages.split(',') if args.download_languages is not None else []

    print(download_languages)

    regex_remove_tag = re.compile(r"<.*?>")
    char_to_remove = ['{', '}', '[', ']', '<', '>', '=', '&', '"', '(', ')', '|', '/', '\\', '*', '\'', '#', ':']
    translation_table = str.maketrans(''.join(char_to_remove), ''.join([' '] * len(char_to_remove)))

    if download_languages is not None and len(download_languages) > 0:
        print('Starting download')
        for lang in download_languages:
            print('Downloading ' + lang + ' package')
            r = requests.get('https://dumps.wikimedia.org/{}wiki/latest/{}wiki-latest-pages-meta-current.xml.bz2'.format(lang, lang), stream=True)
            lang_filename = str(uuid.uuid4())
            with open(lang_filename, 'wb') as f:
                for i, chunk in enumerate(r.iter_content(chunk_size=1000 * 1024)):
                    if i % 10 == 0:
                        print(str(i) + ' MB downloaded')
                    if chunk:
                        f.write(chunk)
                input_files.append(lang_filename)

    # We start by decompressing the file
    print('Starting decompression')
    for input_file in input_files:
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

    if mix_sentences:
        if os.name == 'posix':
            print('Shuffling file!')
            # For this, I kneeled before the power of shuf, obviously this won't work on Windows
            # shuf [output_file] -o [random_output_file]
            subprocess.call(['shuf', output_file, '-o', 'random_' + output_file])
        else:
            print('Mix sentences is only available on Posix systems!')

    # Finally we delete the file!
    print('Cleaning up')
    os.remove(output_file + '_decompressed')

if __name__=='__main__':
    main(sys.argv)
