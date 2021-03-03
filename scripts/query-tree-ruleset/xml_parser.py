# Custom imports
import tree_ruleset as TR

# Imports
import xml.etree.ElementTree as ET
from pathlib import Path
import os, sys

class Parser:
    """XmlParser, parse xml file to RuleTree"""

    def __init__(self, filePath):
        """Initialize XmlParser

        Args:
            filePath (str): path to xml file

        Returns:
            XmlParser: Object if file exitst, None otherwise
        """

        if self.__check_file_path(filePath):
            self.__filePath = filePath
            self.__tree = self.__read_file(self.__filePath)
        else:
            raise FileNotFoundError(f'Error: file {filePath} does not exists or is not xml')


    def __check_file_path(self, path):
        """Checks if file identified by path exists and is xml

        Args:
            path (Path): path of the file

        Returns:
            boolean: true if exists, false otherwise
        """

        f_path = Path(path)
        return f_path.exists() and not f_path.is_dir() and f_path.suffix == '.xml'


    def __read_file(self, path):
        """read and parse xml file

        Fixes bad formatting of ruleset xml files, only to work with its data

        Args:
            path (str): path to xml file

        Returns:
            ElementTree: ET object if file found, None otherwise
        """

        with open (path, "r") as input_file:
            input_string = f'<document>{os.linesep}{input_file.read()}{os.linesep}</document>'
            return ET.fromstring(input_string)


    def get_rule_tree(self):
        ruleTree = TR.RuleTree()

        for element in self.__tree:
            # ignore anything but groups
            if element.tag != 'group':
                pass
                # # if args.debug:
                # sys.stdout.write(f'Ignoring {element.tag}: {element.attrib}{os.linesep}')
                # for child in element:
                #     sys.stdout.write(f'    {child.tag}: {child.attrib}{child.linesep}')

            else:
                # if args.debug:
                #     sys.stdout.write(f'{os.linesep}Found {element.tag}: {element.attrib}{os.linesep}Searching inside:{os.linesep}')

                # Iterate over rules

                for rule in element:
                    # Parse rule id
                    ruleNode = TR.RuleNode(rule.attrib['id'])
                    ruleNode.file = self.__filePath

                    for attr in rule:
                        if attr.tag == 'if_sid':
                            for parent in attr.text.split(','):
                                ruleNode.parents.append(parent.replace(' ', ''))
                        # Parse frequency parent
                        elif attr.tag == 'if_matched_sid':

                            freq = 0
                            if 'frequency' in rule.attrib:
                                freq = rule.attrib['frequency']
                            for parent in attr.text.split(','):
                                ruleNode.frec_parents[parent.replace(' ', '')]\
                                    = freq


                    # Add ruleNode to ruleTree
                    ruleTree.add_rule(ruleNode.id, ruleNode)

        return ruleTree
