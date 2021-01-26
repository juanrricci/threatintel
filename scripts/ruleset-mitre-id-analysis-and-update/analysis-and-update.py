# 1ra iteración:
# - Recibir lista de IDs de rules (o no recibir nada para parsear el ruleset completo)
# - Buscar las rules dentro del ruleset
# - Parsear IDs de técnicas y tácticas
# - Generar el archivo JSON con el formato requerido

import os
# import xml.etree.etree as ET
# from xml.etree import ElementTree
from lxml import etree
import glob
import json
from bs4 import BeautifulSoup
from io import StringIO
import sys

from pyattck import Attck

attack = Attck()

temp_out = StringIO()

# class CommentedTreeBuilder(etree.TreeBuilder):
#     def comment(self, data):
#         self.start(etree.Comment, {})
#         self.data(data)
#         self.end(etree.Comment)

# Get all the paths of the XML rule files from the ruleset folder
rule_files = glob.glob('C:\\Users\\juarc\\Documents\\GitHub\\wazuh\\ruleset\\rules\\*.xml')

current_ruleset_mitre_status = {}

rule_id_list = ["504", "505", "518", "550", "553", "592", "594", "597", "750", "751", "2504", "5132", "5133", "2833", "5302", "5401", "5402", "5407", "5403", "5404", "5405", "4339", "4340", "4342", "4509", "6301", "6361", "6373", "6376", "11209", "18118", "18171", "31413", "31514", "31550", "35054", "52510", "80106", "80513", "80516", "80714", "80721", "80791", "81609", "83202", "24059", "24701", "24702", "24708", "87902", "87914", "87921", "87931", "87941", "87946", "87957", "18655", "18656", "18657", "60117", "60196", "60682", "60683", "60689", "61130", "61138", "90509", "90537", "63105", "64024", "64027", "64505", "64506"]

modified_ruleset_mitre_status_dict = {}

with open("modified_ruleset_mitre_status_linted.json") as modified_ruleset_mitre_status_json:
    modified_ruleset_mitre_status_dict = json.load(modified_ruleset_mitre_status_json)
    rule_id_list = modified_ruleset_mitre_status_dict.keys()

mitre_attrib = {   
    'tacticID':'',
    'tactic':'',
    'techniqueID':'',
    'technique':''
}



# Copy the rules of each rule file to the ruleset_wrapper.xml file under the <ruleset> tag
for rule_file in rule_files:
    with open(rule_file) as rule_file_content:
        with open('./ruleset_wrapper.xml', 'w') as ruleset_wrapper:
            ruleset_wrapper.write('<ruleset>\n')
            ruleset_wrapper.write(rule_file_content.read())
            ruleset_wrapper.write('\n</ruleset>')    

        # Parse the content of ruleset_wrapper.xml
        # if(True):
        try:
        # tree = ET.parse('./ruleset_wrapper.xml', parser)
            # parser = etree.XMLParser(target=CommentedTreeBuilder())
            # tree = etree.parse('./ruleset_wrapper.xml', parser)
            tree = etree.parse('./ruleset_wrapper.xml')
            # etree.indent(tree, space=" ", level=0)
            # print("Aca estamos:", os.path.basename(rule_file))
            ruleset = tree.getroot()
        
            for group in ruleset:
                for rule in group:
                    try:
                        # print('Chequeando rule:', rule.attrib['id'])
                        if rule.attrib['id'] in rule_id_list:
                            print('Regla', rule.attrib['id'], 'encontrada en', os.path.basename(rule_file))
                            current_ruleset_mitre_status[rule.attrib['id']] = {
                                'ruleDescription':rule.find('description').text,
                                'mitre':[]
                            }

                            # print(current_ruleset_mitre_status)
                            for mitre in rule.findall('mitre'):
                                # Populate the current_ruleset_mitre_status dict for writing to JSON
                                print('Longitud de la lista MITRE:', len(mitre))
                                for id in mitre.findall('id'):
                                    # print(id)
                                    etree.dump(id)
                                    mitre_attrib_copy = mitre_attrib.copy()
                                    if 'technique' in id.attrib: mitre_attrib_copy['technique'] = id.attrib['technique']
                                    if 'tactic' in id.attrib: mitre_attrib_copy['tactic'] = id.attrib['tactic']
                                    if 'tacticID' in id.attrib: mitre_attrib_copy['tacticID'] = id.attrib['tacticID']
                                    mitre_attrib_copy['techniqueID'] = id.text
                                    current_ruleset_mitre_status[rule.attrib['id']]['mitre'].append(mitre_attrib_copy)

                                # **** Correct attributes in the XML tree ****
                                    # 1- Remove previous IDs one by one
                                    # mitre.remove(id)
                                # 2- Add new IDs with attributes under the MITRE tag (will duplicate if multiple MITRE tags exist)
                                for mitre_id_attribs in modified_ruleset_mitre_status_dict[rule.attrib['id']]['mitre']:
                                    id = etree.SubElement(mitre, 'id')
                                    id.set('technique', mitre_id_attribs['technique'])
                                    id.set('tactic', mitre_id_attribs['tactic'])
                                    id.set('tacticID', mitre_id_attribs['tacticID'])
                                    id.text = mitre_id_attribs['techniqueID']
                                    mitre.remove(id)
                                    etree.dump(id)

                                # print(mitre.getvalue())
                                sys.stdout = temp_out
                                # etree.dump(mitre)
                                sys.stdout = sys.__stdout__
                                new_mitre_ids = temp_out.getvalue()
                                print('Nuevos MITREs:', new_mitre_ids)
                                # print (new_mitre_ids.split('</id>'))
                            # ---------------------

                            print('MITRE IDs actuales en regla', rule.attrib['id'], '-', rule.find('description').text, file=open("changes_to_apply.txt", "a"))
                            print(json.dumps(current_ruleset_mitre_status[rule.attrib['id']]['mitre'], indent = 2), file=open("changes_to_apply.txt", "a"))
                            print('--------------', file=open("changes_to_apply.txt", "a"))
                            print('MITRE IDs a aplicar en regla', rule.attrib['id'], '-', rule.find('description').text, file=open("changes_to_apply.txt", "a"))
                            print(json.dumps(modified_ruleset_mitre_status_dict[rule.attrib['id']]['mitre'], indent = 2), file=open("changes_to_apply.txt", "a"))
                            print('**************', file=open("changes_to_apply.txt", "a"))

                    except:
                        # print("Comentario")
                        continue

            # Write down the corrected tree to new ruleset files
            
            tree.write('./downloaded-ruleset/' + os.path.basename(rule_file), pretty_print=True)
            # x = etree.tostring(ruleset)
            # print(BeautifulSoup(x, 'xml').prettify(), file=open('./downloaded-ruleset/' + os.path.basename(rule_file), 'w'))
            
            file1 = open('./downloaded-ruleset/' + os.path.basename(rule_file), 'r') 
            Lines = file1.readlines() 

            del Lines[0]
            del Lines[-1]

            with open('./corrected-ruleset/' + os.path.basename(rule_file), 'w') as f:
                for line in Lines:
                    f.write(line)

            # Write down the current_ruleset_mitre_status dict to JSON
            with open('current_ruleset_mitre_status.json', 'w') as current_ruleset_mitre_status_json:
                json.dump(current_ruleset_mitre_status, current_ruleset_mitre_status_json, indent = 4)                    

        except:
            print(os.path.basename(rule_file), '- NOT OK\n')    






# 2da iteración:
# - Recibir JSON con el formato requerido (validar el formato para evitar IDs de rules duplicados)
# - Por cada rule del JSON:
# --- Buscar la rule en el ruleset
# --- Parsear IDs de técnicas y tácticas actuales de esa rule
# --- Parsear IDs de técnicas y tácticas en el JSON para esa rule
# ----- Generar un set de técnicas por cada táctica para descartar relaciones duplicadas
# ----- Validar que sea correcta la relación entre técnica y táctica con pyattck
# --- Mostrar los cambios a realizar o aplicarlos si se ingresó el parámetro -f

      
