'''
Takes a large file and splits into smaller files
'''
from itertools import chain
import os

def split_file(filename, pattern, size):
    """Split a file into multiple output files.

    The first line read from 'filename' is a header line that is copied to
    every output file.
    The remaining lines are split into blocks of at
    least 'size' lines and written to output files whose names
    are pattern.format(1), pattern.format(2), and so on.
    The last output file may be short.

    """
    with open(filename, 'rb') as f:
        header = next(f)
        for index, line in enumerate(f, start=1):
            with open(pattern.format(index), 'wb') as out:
                out.write(header)
                n = 0
                for line in chain([line], f):
                    out.write(line)
                    n += 1
                    if n >= size:
                        break
            print(pattern.format(index))

if __name__ == '__main__':
    source_filename = 'data\\' +'suppression_bounces_email_only_full.csv'  # this is full list of subscribers from OpenEMM
    destination_filename = 'data\\' + 'suppression_bounces_email_only_full'
    source_file = os.path.join('', source_filename)
    print(source_file)
    pattern = destination_filename + 'part_{0:03d}.csv'
    split_file(source_file, pattern, 10000)