from pyattck import Attck
import json
import argparse

attack = Attck()

parser = argparse.ArgumentParser(description='Gets MITRE info based on id')
parser.add_argument('rule_id', help='Id to match')
parser.add_argument('t_id', help='technique or subtechnique ID')
parser.add_argument('rule_desc', help="rule description")
parser.add_argument('-o', '--output', metavar="FILE_PATH", help="Save output to FILE_PATH")
parser.add_argument('-V', '--verbose', action='store_true', help="Print detailed information")
parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')

args = parser.parse_args()

id = args.t_id
rule_number = args.rule_id

found = False
rule_description = args.rule_desc
for technique in attack.enterprise.techniques:
    for subtechnique in technique.subtechniques:    
        if subtechnique.id == id:
            found = True
            print('Subtechnique ID: ' + subtechnique.id)
            print('Subtechnique name: ' + subtechnique.name)
            subtech_id = subtechnique.id
            subtech_name = subtechnique.name
            print('Technique ID: ' + technique.id)
            print('Technique name: ' + technique.name)
            tech_id = technique.id
            tech_name = technique.name
            for tactic in technique.tactics:
                print('Tactic ID: ' + tactic.id)
                print('Tactic name: ' + tactic.name)
                tac_id = tactic.id
                tac_name = tactic.name
            
if found:
    jsondata = {}
    rule_dict = {}

    mitre = {}
    mitre['tacticID']  = tac_id
    mitre['tactic']  = tac_name
    mitre['techniqueID']  = subtech_id
    mitre['technique']  = tech_name + ': ' + subtech_name

    rule_dict['ruleDescription'] = rule_description
    rule_dict['mitre'] = mitre

    jsondata[rule_number] = rule_dict
    print(json.dumps(jsondata))

    modified_ruleset_json = json.dumps(jsondata)


else:
    print('Subtechnique not found. Searching in techniques... \n')
    for technique in attack.enterprise.techniques:    
        if technique.id == id:
            found = True
            print('Technique ID: ' + technique.id)
            print('Technique name: ' + technique.name)
            tech_id = technique.id
            tech_name = technique.name
            for tactic in technique.tactics:
                print('Tactic ID: ' + tactic.id)
                print('Tactic name: ' + tactic.name)
                tac_id = tactic.id
                tac_name = tactic.name

if found:
    jsondata = {}
    rule_dict = {}

    mitre = {}
    mitre['tacticID']  = tac_id
    mitre['tactic']  = tac_name
    mitre['techniqueID']  = tech_id
    mitre['technique']  = tech_name

    rule_dict['ruleDescription'] = rule_description
    rule_dict['mitre'] = mitre

    jsondata[rule_number] = rule_dict
    print(json.dumps(jsondata))

    modified_ruleset_json = json.dumps(jsondata)
    with open(args.output, "w") as of:
        of.write(modified_ruleset_json) 

else:
    print("Not found :(")



