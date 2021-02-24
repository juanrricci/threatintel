# Data structures and functionality definig the ruleset tree


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

    def add_parents(self, *parents):
        """Add parents

        Args:
            *parents: parents id to be added
        """

        self.parents.append(parents)

class RuleTree:
    """Data structure representing the whole ruleset

        Stored internally with an unordered hash (Dictionary)
    """

    def __init__(self):
        """Initializes empty tree"""
        self.__tree = {}

    def __getitem__(self, key):
        """get rule by id

        Args:
            key (integer): unique id of rule

        Returns:
            ruleNode: rule identified by key
        """

        return self.__tree[id]


    def add_rule(self, id, ruleNode):
        """Add rule node to tree

        Args:
            id (number): unique id
            ruleNode (RuleNode): rule node to be added
        """

        if id in self.__tree.keys():
            raise DuplicatedIdError(f"Rule {id} already present on tree, nothing added")
        else:
            self.__tree[id] = ruleNode


    def union(self, other):
        """Union operator

        Args:
            other (RuleTree): RuleTree to be merged

        Raises:
            DuplicatedIdError: Raised if same rule id found on both
        """

        for key in self.__tree.keys():
            if key in other.__tree.keys():
                raise DuplicatedIdError(
            f'Error in union: duplicated id {key} found')

        self.__tree = self.__tree | other.__tree

    def rule_count(self):

        return len(self.__tree)

    def to_str(self):
        for id in self.__tree.keys():
            print(id)


class DuplicatedIdError(Exception):
    """Exception raised when duplicated ID detected

    Args:
        message (str): explanation of the error
    """

    def __init__(self, message):
        self.message = message
