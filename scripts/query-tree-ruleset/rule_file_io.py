# Custom Imports
# import xml_parser
import tree_ruleset as TR

# Imports
from pathlib import Path
import os
import importlib


class RulesetReader:
    def __init__(self, dirPath, parser):
        """Initialize Reader

        Args:
            dirPath (str): path to directory

        Raises:
            FileNotFoundError: if directory does not exits
        """

        self.dirPath = Path(dirPath)

        if not self.__check_directory_path(dirPath):
            raise FileNotFoundError(message =
        f'Error: directory {dirPath} does not exists')

        elif parser == 'xml':
            self.__parser = importlib.import_module('xml_parser')
        else:
            raise ParserNotSupportedError(
                f'Error, parser for {parser} not supported')




    def __check_directory_path(self, path):
        """Checks if directory identified by path exists

        Args:
            path (str): path of the directory

        Returns:
            boolean: true if exists, false otherwise
        """

        f_path = Path(path)
        if not f_path.is_dir():
            return False
        else:
            return True

    def generate_tree(self):
        """obtain rule tree from directory

        Returns:
            RuleTree: rule tree
        """

        ruleTree = TR.RuleTree()
        for filename in os.listdir(self.dirPath):
            f = os.path.join(self.dirPath, filename)
            if os.path.isfile(f):
                parser = self.__parser.Parser(f)
                ruleTree.union(parser.get_rule_tree())

        return ruleTree





    # def __iter__(self):
    #     """Iterator definition

    #     Returns:
    #         RulesetReaderIterator: iterator for RulesetReader
    #     """

    #     return RulesetReaderIterator(self)


# class RulesetReaderIterator:

#     def __init__(self, reader):
#         self._reader = reader
#         self._index = 0

#     def __next__(self):
#         if self._index < len(self._reader.Files):
#             result = self._reader.Files[self._index]
#             self._index += 1
#             return result
#         else:
#             raise StopIteration

def ParserNotSupportedError(Exception):
    """Exception raised if specified parser is not supported by RulesetReader.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)