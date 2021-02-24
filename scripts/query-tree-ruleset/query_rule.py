# Custom classes imports
import tree_ruleset as TR
import rule_file_io as RIO

# Imports
import argparse
import sys, os

def main():
    rulesetReader = RIO.RulesetReader("/home/osbee/Projects/WazuhProjects/wazuh/ruleset/rules")
    ruleTree = rulesetReader.generate_tree()
    print(ruleTree.rule_count())
    #ruleTree.to_str()

if __name__ == "__main__":
    main()

