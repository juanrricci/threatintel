import os
import xml.etree.ElementTree as ET
import glob
import json

from pyattck import Attck

attack = Attck()

# Get all the paths of the XML rule files from the ruleset folder
rule_files = glob.glob('C:\\Users\\juarc\\Documents\\GitHub\\wazuh\\ruleset\\rules\\*.xml')

ok_file_count = 0
not_ok_file_count = 0

total_rule_count = 0
rules_with_mitre_id_count = 0

mitre_id_set = set()

# Copy the rules of each rule file to the ruleset_wrapper.xml file under the <ruleset> tag
for rule_file in rule_files:
    #print(os.path.basename(rule_file), '\n')
    with open(rule_file) as rule_file_content:
        # Create ruleset_wrapper.xml file
        with open('./ruleset_wrapper.xml', 'w') as ruleset_wrapper:
            # Open the <ruleset> tag
            ruleset_wrapper.write('<ruleset>')
            # Copy the content of the rule file under the <ruleset> tag
            ruleset_wrapper.write(rule_file_content.read())
            # Close with </ruleset> tag
            ruleset_wrapper.write('</ruleset>')    

        # Parse the content of ruleset_wrapper.xml
        try:
            tree = ET.parse('./ruleset_wrapper.xml')
            print(os.path.basename(rule_file), '- OK\n')
            ruleset = tree.getroot()
            

            for group in ruleset:
                print('----> Grupo de reglas:', group.attrib['name'])
                print('----> Cantidad total de reglas:', len(list(group)))
                print('-----\n')
                total_rule_count += len(list(group))

                for rule in group:
                    #print(rule.tag, rule.attrib['id'])
                    for mitre in rule.iter('mitre'):
                        #print('tiene mitre ids')
                        rules_with_mitre_id_count += 1
                        for mitre_id in mitre:
                            print(mitre_id.text)
                            mitre_id_set.add(mitre_id.text)

            # print('Cantidad de reglas con MITRE Ids:', rules_with_mitre_id_count)   
            ok_file_count += 1
        except:
            print(os.path.basename(rule_file), '- NOT OK\n')
            not_ok_file_count += 1

print('****************\n****************\n')
print('Cantidad de archivos de reglas analizados:', ok_file_count)
print('Cantidad de archivos de reglas ignorados:', not_ok_file_count)
print('Conteo total de reglas:', total_rule_count)
print('Conteo de reglas con al menos 1 MITRE ID:', rules_with_mitre_id_count)
rules_with_mitre_fraction = rules_with_mitre_id_count / total_rule_count
rules_with_mitre_percentage = "{:.0%}".format(rules_with_mitre_fraction)
print('Porcentaje de reglas con MITRE ID:', rules_with_mitre_percentage)
print('Conteo de reglas SIN MITRE ID:', total_rule_count - rules_with_mitre_id_count)
mitre_id_set_sorted = sorted(mitre_id_set)
print('MITRE ID set:', mitre_id_set_sorted)
print('MITRE ID set length:', len(mitre_id_set_sorted))

single_technique = '{"techniqueID": "T1098","score": 1,"color": "#e60d0d","comment": "","enabled": true,"metadata": [],"showSubtechniques": false}'

single_technique_dict = json.loads(single_technique)

with open('../technique-skeleton.json') as technique_skeleton_file:
    technique_skeleton = json.load(technique_skeleton_file)

    for technique_id in mitre_id_set_sorted:
        single_technique_dict["techniqueID"] = technique_id
        single_technique_dict_copy = single_technique_dict.copy()
        technique_skeleton["techniques"].append(single_technique_dict_copy)

json_object = json.dumps(technique_skeleton, indent = 4) 

#print(json_object)

with open('wazuh_full_mitre.json', 'w') as wazuh_full_mitre_json:
    json.dump(technique_skeleton, wazuh_full_mitre_json)

enterprise_techniques = []

for technique in attack.enterprise.techniques:
    enterprise_techniques.append(technique.id)
    for subtechnique in technique.subtechniques:
        enterprise_techniques.append(subtechnique.id)

print(enterprise_techniques)
print(len(enterprise_techniques))

invalid_technique_ids = [i for i in mitre_id_set_sorted if i not in enterprise_techniques]

print("Tecnicas invalidas:", invalid_technique_ids)
print(len(invalid_technique_ids))

uncovered_tecnique_ids = [i for i in enterprise_techniques if i not in mitre_id_set_sorted]
print("Tecnicas no cubiertas por las reglas de Wazuh:", uncovered_tecnique_ids)
print(len(uncovered_tecnique_ids))
uncovered_tecnique_ids_fraction = len(uncovered_tecnique_ids) / len(enterprise_techniques)
uncovered_tecnique_ids_percentage = "{:.0%}".format(uncovered_tecnique_ids_fraction)
print('Porcentaje de MITRE IDs no cubiertos:', uncovered_tecnique_ids_percentage)



# Copy the rules of each rule file to the ruleset_wrapper.xml file under the <ruleset> tag

rule_ids_invalid_mitre = []

for rule_file in rule_files:
    #print(os.path.basename(rule_file), '\n')
    with open(rule_file) as rule_file_content:
        # Create ruleset_wrapper.xml file
        with open('./ruleset_wrapper.xml', 'w') as ruleset_wrapper:
            # Open the <ruleset> tag
            ruleset_wrapper.write('<ruleset>')
            # Copy the content of the rule file under the <ruleset> tag
            ruleset_wrapper.write(rule_file_content.read())
            # Close with </ruleset> tag
            ruleset_wrapper.write('</ruleset>')    

        # Parse the content of ruleset_wrapper.xml
        try:
            tree = ET.parse('./ruleset_wrapper.xml')
            # print(os.path.basename(rule_file), '- OK\n')
            ruleset = tree.getroot()
            

            for group in ruleset:
                # print('----> Grupo de reglas:', group.attrib['name'])
                # print('----> Cantidad total de reglas:', len(list(group)))
                # print('-----\n')
                total_rule_count += len(list(group))

                for rule in group:
                    #print(rule.tag, rule.attrib['id'])
                    for mitre in rule.iter('mitre'):
                        #print('tiene mitre ids')
                        # rules_with_mitre_id_count += 1
                        for mitre_id in mitre:
                            # print(mitre_id.text)
                            if mitre_id.text in invalid_technique_ids:
                                print('Tecnica invalida:', mitre_id.text)
                                print(rule.find('description').text)
                                rule_ids_invalid_mitre.append({"rule-id":rule.attrib['id'],"rule-description":rule.find('description').text,"invalid-id":mitre_id.text})
                            # print(mitre_id.text)
                            # mitre_id_set.add(mitre_id.text)

            # print('Cantidad de reglas con MITRE Ids:', rules_with_mitre_id_count)   

        except:
            # print(os.path.basename(rule_file), '- NOT OK\n')
            not_ok_file_count += 1

print('IDs de rules con MITRE ID invalido:')
for data in rule_ids_invalid_mitre:
    print(data)
print(len(rule_ids_invalid_mitre))