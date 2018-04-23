#!/usr/local/bin/python

import os
import re
import sys
import textract
from fnmatch import fnmatch


def main(argv):

    if len(argv) == 3:
        input_dir = argv[1]
        output_dir = argv[2]
        process_dir(input_dir, output_dir)
        return

    if len(argv) == 2:
        input_file = argv[1]
        f = process(input_file)
        print f
        return

    usage()

def process_dir(in_dir, out_dir):
    pattern = '*.pdf'
    try:
        os.makedirs(out_dir)
    except:
        pass
    for path, subdirs, files in os.walk(in_dir):
	for name in files:
            if fnmatch(name, pattern):
                in_file = os.path.join(in_dir, name) 
                out_file = os.path.join(out_dir, name) + ".txt"
                print "%s => %s" % (in_file, out_file)
                o =  process(in_file)
                f = open(out_file, 'w')
                f.write(o)
                f.close()

        for d in subdirs:
            process_dir(os.path.join(in_dir, d), os.path.join(out_dir, d))

def usage():
    print """
preprocess <input_dir> <output_dir>

Will parse all files under <input_dir> (rebuildng directory structure under <input_dir>) and
write to <output_dir>.
    """

def process(input_file):
    text = textract.process(input_file)
    out = re.sub(r'\W+', '', text)
    return out


if __name__ == "__main__":
    main(sys.argv)
