# Data structures and functionality definig the ruleset tree
import sys, os
import tree_printer

class RuleNode:
    """Data structure representing a node

        Ascendat relationship only (parent)
    """
    def __init__(self, id):
        """Initializes node

        Args:
            id (integer): unique id
        """

        self.id = id
        self.parents = []
        self.frec_parents = {}
        self.file = ''

    # def add_parent(self, parent):
    #     """A  dd parents

    #     Args:
    #         *parents: parents id to be added
    #     """
    #     self.parents.append(parent)

    # def add_frec_parent(self, parent):
    #     """Add parents by frecuancy relation

    #     Args:
    #         *parents: parents id to be added
    #     """

    #     self.frec_parents | parent




class RuleTree:
    """Data structure representing the whole ruleset

        Stored internally with an unordered hash (Dictionary)
    """

    def __init__(self):
        """Initializes empty tree"""
        self.tree = {}
        self.groups = {}

    def __getitem__(self, key):
        """get rule by id

        Args:
            key (integer): unique id of rule

        Returns:
            ruleNode: rule identified by key
        """

        return self.tree[key]


    def add_rule(self, id, ruleNode):
        """Add rule node to tree

        Args:
            id (number): unique id
            ruleNode (RuleNode): rule node to be added
        """

        if id in self.tree.keys():
            raise DuplicatedIdError(f"Rule {id} already present on tree, nothing added")
        else:
            self.tree[id] = ruleNode


    def union(self, other):
        """Union operator

        Args:
            other (RuleTree): RuleTree to be merged

        Raises:
            DuplicatedIdError: Raised if same rule id found on both
        """

        for key in self.tree.keys():
            if key in other.tree.keys():
                raise DuplicatedIdError(
            f'Error in union: duplicated id {key} found')

        self.tree = self.tree | other.tree


    def check_integrity(self):
        """Checks integruty of ruleTree

        Raises:
            IntegrityError: if missmatch between key and ruleNode.id
            IntegrityError: if parent not present in ruleTree
            IntegrityError: if frequency parent not present in ruleTree
        """

        for key, rule in self.tree.items():
            if key == rule.id:
                for parent in rule.parents:
                    if parent not in self.tree.keys():
                        raise IntegrityError(
                            f'Error parent {parent} of rule {key} not in ruleTree',
                            parent, key)
                for parent in rule.frec_parents:
                    if parent not in self.tree:
                        raise IntegrityError(
                            f'Error frequency parent {parent} of rule {key} not in ruleTree',
                            parent, key)
            else:
                raise IntegrityError(f'key {key} not equal to rule {rule.id}',
                        child=key)



    def print_parents(self, rule):
        sys.stdout.write(f'{rule}:{self.tree[rule].parents}{self.tree[rule].frec_parents}{os.linesep}')
        for parent in self.tree[rule].parents:
            self.print_parents(parent)
        for parent in self.tree[rule].frec_parents.keys():
            self.print_parents(parent)
        # tree = self.__parent_printer_tree(rule)
        # tree = self.__parent_printer_tree(rule)
        # print(tree)


        # tree = tree(tree_printer.Node(2))
        # print(tree_printer.drawTree(tree))

    # def __parent_printer_tree(self,rule):
    #     return tree_printer.Node(rule)(self.__parent_printer_tree(p) for p in self.tree[rule].parents )





    def print_childs(self, rule):
        childs = self.__get_childs(rule)
        sys.stdout.write(f'{rule}:{childs}{os.linesep}')
        for child in childs:
            self.print_childs(child)


    def __get_childs(self, rule):
        """Return direct childs of rule

        Args:
            rule (int): rule id

        Returns:
            [int]: Array with childs ids
        """

        childs = []
        for ruleID, ruleNode in self.tree.items():
            if rule in ruleNode.parents or rule in ruleNode.frec_parents.keys():
                childs.append(ruleID)

        return childs


    # def get_subtree_parents(self, rule):

    #     subTree = RuleTree()

    #     self.__r_get_subtree_parents(rule, subTree)


    #     return subTree


    # def __r_get_subtree_parents(self, rule, subTree):
    #     subTree.add_rule(rule, self.tree[rule])
    #         for parent in self.tree[rule].parents:
    #             self.__r_get_subtree(parent, subTree)
    #         for parent in self.tree[rule].frec_parents
    #             self.__r_get_subtree(parent, subTree)











# Exceptions
class DuplicatedIdError(Exception):
    """Exception raised when duplicated ID detected

    Args:
        message (str): explanation of the error
    """

    def __init__(self, message):
        self.message = message


class IntegrityError(Exception):
    """Exception raised when integrity error detected

    Args:
        message (str): explanation of the error
    """

    def __init__(self, message, parent=None, child=None):
        self.message = message
        self.parent = parent
        self.child = child

