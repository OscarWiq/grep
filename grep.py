from argparse import ArgumentParser, FileType, RawDescriptionHelpFormatter
import os
import re
from textwrap import dedent


parser = ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,
    description=dedent("""
        Search for PATTERN in each FILE.

        Example: python3 grep.py -i 'SOME PATTERN' file.py
    """),
)
parser.add_argument('pattern', metavar='PATTERN')
parser.add_argument('files', metavar='FILE', nargs='*', type=FileType('rt'))
parser.add_argument(
    '-i',
    '--ignore-case',
    dest='flags',
    action='store_const',
    const=re.I,
    default=0,
    help="ignore case distinctions",
)
parser.add_argument(
    '-n',
    '--line-number',
    action='store_true',
    help="print line number with output lines",
)
parser.add_argument(
    '-v',
    '--invert-match',
    action='store_true',
    help="select non-matching lines",
)
parser.add_argument(
    '-T',
    '--initial-tab',
    action='store_true',
    help="make tabs line up",
)

args = parser.parse_args()

pattern = re.compile(args.pattern, flags=args.flags)
with_filename = len(args.files) > 1

for f in args.files:
    size = os.fstat(f.fileno()).st_size
    digits = len(str(size))
    for n, line in enumerate(f, start=1):
        match = pattern.search(line)
        if match and not args.invert_match or not match and args.invert_match:
            if with_filename:
                print(f"{f.name}:", end='')
            if args.line_number:
                if args.initial_tab:
                    print(f"{n}:".rjust(digits+1), end='')
                else:
                    print(f"{n}:", end='')
            if args.initial_tab:
                print("\t", end='')
            print(line.rstrip('\n'))