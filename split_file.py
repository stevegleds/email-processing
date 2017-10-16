'''
Takes a large file and splits into smaller files
It was created to split email csv files that Openemm rejected because of some bad email.
Some of the parts would work leaving a sub part that contained the bad data.
Enter the source and destination files and adjust the size parameter to the required size of each file
For the email import the first line needs to be 'email' so this is added before the next batch of emails are added
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
    source_filename = 'weed20171016checked.csv'  # this is full list of subscribers from OpenEMM
    destination_filename = 'weed20171016part1000.csv'
    source_file = os.path.join('', source_filename)
    print('Source file is:', source_file)
    pattern = destination_filename + 'part_{0:03d}.csv'
    split_file(source_file, pattern, 1000)