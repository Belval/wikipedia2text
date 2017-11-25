# wikipedia2text
A tool to convert a Wikipedia dump file into plain text

## How to use it

Use `python3 wikipedia2text.py -h` to print usage.

A typical usage would be like this `python3 wikipedia2text out.txt -dl fr,en`

There are a few arguments you can use to change the "normal" behavior:

- `-dl (--download_languages)` Allow you to specify one or more languages to download from wikipedia (imperatively separated by a comma).
- `-i (--input_files)` Allow you to specify one or more files that were already downloaded (both options can be combined)
- `-m (--mix_sentences)` Will shuffle the data to make it more uniform (must have `sort`)
- `-u (--unique)` Will remove duplicate lines (must have `uniq`)
- `-d (--keep_digits)` Will keep digits in string
- `-s (--split_sentences)` Will split sentences on "."
- `-ml (--min_length)` Will not save any string for which `len(str) < x`

## Where can I get the dump file?

See https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-meta-current.xml.bz2 or use `-dl en`

## How long can it take?

Using `python3 wikipedia2text.py -dl fr,en -m -u -s` took about 12 hours using a Ryzen 1700X and a 120Mb/s Internet connection.
