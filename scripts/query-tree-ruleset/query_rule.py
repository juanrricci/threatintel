# Custom classes imports
import tree_ruleset as TR
import rule_file_io as RIO

# Imports
import argparse
import sys, os


# Console arguments definition
parser = argparse.ArgumentParser(
    prog="query_rule.py",
    description='Script to query about ruleset')

# General arguments
parser.add_argument(
    '-V', '--verbose',
    action='store_true',
    help="Print detailed information")
parser.add_argument(
    '-d', '--debug',
    type=int,
    choices=range(0,5),
    default=0,
    help='Print debug information: 0 none, 4 max (default: %(default)s)')

# COMMANDS selection subparser
subparsers = parser.add_subparsers(
    dest='COMMAND',
    title='COMMANDS',
    help='check %(prog)s {COMMAND} --help for more info')

# generate
parser_generate = subparsers.add_parser(
    'generate',
    help="Generate json ruleset file used to perform querys")
parser_generate.add_argument(
    'input_dir',
    help='Input directory containing ruleset files')
parser_generate.add_argument(
    '-e', '--extension',
    required=True,
    choices=['xml'],
    help='Specify file extension')
parser_generate.add_argument(
    '-o', '--output',
    metavar='file_path',
    default='./tree_ruleset.json',
    help='Specify file output path, (default: %(default)s) ')

# query
parser_query = subparsers.add_parser(
    'query',
    help='Interactive prompt for quering rules')


### GENERATE FUNCTION ###
def generate(input_dir, extension, output_dir, d_level, verbose):
    rulesetReader = RIO.RulesetReader(input_dir, extension)
    ruleTree = rulesetReader.generate_tree()
    print(ruleTree.size())
    #ruleTree.to_str()


### QUERY FUNCTION ###
def query():
    pass

if __name__ == "__main__":
    args = parser.parse_args()
    if args.COMMAND == 'generate':
        generate(
            args.input_dir,
            args.extension,
            args.output,
            args.debug,
            args.verbose)
    elif args.COMMAND == 'query':
        query()

