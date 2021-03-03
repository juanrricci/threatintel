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

# # query
# parser_query = subparsers.add_parser(
#     'query',
#     help='Interactive prompt for quering rules')


### GENERATE FUNCTION ###
def generate(input_dir, extension, output_dir, d_level, verbose):
    rulesetReader = RIO.RulesetReader(input_dir, extension)
    ruleTree = rulesetReader.generate_tree()

    return ruleTree


### QUERY FUNCTIONS ###
def query(ruleTree):
    sys.stdout.write(f'Correctly loaded {len(ruleTree.tree)} rules, type rule id and press enter:{os.linesep}')
    # for key in ruleTree.tree.keys():
    #     print(key)

    prompt = True
    option = ''

    while prompt:
        sys.stdout.write(f'Hello, choose option:{os.linesep} \
        1) Query rule {os.linesep} \
        2) Size of ruleset {os.linesep} \
        3) Query groups {os.linesep} \
        quit) quit program {os.linesep}')

        option = sys.stdin.readline().replace(os.linesep, '')
        if option == '1':
            query_rule(ruleTree)
        elif option == '2':
            sys.stdout.write(f'{len(ruleTree.tree)}{os.linesep}')
        elif option == '3':
            query_group(ruleTree)
        elif option == 'quit':
            prompt = False
        else:
            sys.stdout.write(f'Not understood{os.linesep}')



def query_rule(ruleTree):

    prompt = True


    while prompt:
        sys.stdout.write(f'Enter rule number or go [back]:{os.linesep}')
        option = ''
        option = sys.stdin.readline().replace(os.linesep, '')

        if option == 'back':
            prompt = False
        elif option in ruleTree.tree.keys():
            sys.stdout.write(
                f'----- Rule {option} PARENTS -----{os.linesep}')
            ruleTree.print_parents(option)
            sys.stdout.write(
                f'----- Rule {option} CHILDS -----{os.linesep}')
            ruleTree.print_childs(option)

        else:
            sys.stdout.write(f'Rule {option} not found{os.linesep}')


def query_group(ruleTree):
    sys.stdout.write(f'Not implemented yet {os.linesep}')

if __name__ == "__main__":
    args = parser.parse_args()
    ruleTree = generate(
            args.input_dir,
            args.extension,
            args.output,
            args.debug,
            args.verbose)
    query(ruleTree)
    # args = parser.parse_args()
    # if args.COMMAND == 'generate':

    # elif args.COMMAND == 'query':


