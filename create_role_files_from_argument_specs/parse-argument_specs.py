#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
# Author: Bernd Finger
#
# Purpose: Display the variables of a role's meta/argument_specs.yml file, keeping the sort order unchanged
#
# Called from create-readme-from-argument_specs.yml as follows:
# ./parse-argument_specs.py role_directory
#
# argv[1]: Root directory of the role
#
# Example:
# ./parse-argument_specs.py ~/.ansible/collections/ansible_collections/community/sap_install/roles/sap_netweaver_preconfigure

import sys
import re
import yaml
import json

if(len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
   print('parse-argument_specs.py: Parse the meta/argument_specs.yml file and display it in a compact way')
   print('Usage: parse-argument_specs.py role_directory')
   print('  role_directory: Root directory of the role')
   exit(0)

role_directory = sys.argv[1]
argument_specs_file = 'meta/argument_specs.yml'

_indent = '  '
_print_none = False
_debug = False

role_name = re.split('/', role_directory)[-1]

# Build a dictionary with the same structure as the output of ansible-doc:
argument_specs_dict = {
    role_name: {
        'collection': "",
        'path': role_directory + '/' + role_name
    }
}

argument_specs_path = role_directory + '/' + argument_specs_file

with open(argument_specs_path) as f:
    argument_specs_dict[role_name].update(yaml.safe_load(f))
    _vars_dict = (json.dumps(argument_specs_dict, indent=4, sort_keys=False, separators=(',', ': ')))

# print (_vars_dict)

for key, value in list(argument_specs_dict.values())[0]['argument_specs']['main']['options'].items():
   print('- ' + key)
   print(_indent + 'description: ')
   for elem in value['description']:
      print(_indent + '  ' + elem)
   if('required' in value):
      print(_indent + 'required: ' + str(value['required']))
   else:
      print(_indent + 'required: false')
   print(_indent + 'type: ' + str(value['type']), end='')
   if(value['type'] == 'list' and value['elements'] == 'dict'):
      print(' of dicts; elements:')
      for key_2, value_2 in list(argument_specs_dict.values())[0]['argument_specs']['main']['options'][key]['options'].items():
         print(_indent + '- ' + key + '.' + key_2)
         print(_indent + '  description: ')
         for elem in value_2['description']:
            print(_indent + '    ' + elem)
         print(_indent + '  type: ' + str(value_2['type']))
      if('example' in value):
         _example=str(value['example'])
         print(_indent + 'example: ')
         _example_lines = re.split('\n', _example)
         for elem in _example_lines:
            print(_indent + _indent + elem)
      else:
         if(_print_none): print(_indent + 'example: None')
   else:
      print('')
      if('choices' in value):
         print(_indent + 'choices: ')
         for elem in value['choices']:
            print (_indent + '  - ' + elem)
      else:
         if(_print_none): print(_indent + 'choices: None')
      if('default' in value):
         print(_indent + 'default: ' + str(value['default']))
      else:
         if(_print_none): print(_indent + 'default: None')
      if('example' in value):
         _example=str(value['example'])
         print(_indent + 'example: ')
         _example_lines = re.split('\n', _example)
         for elem in _example_lines:
            print(_indent + _indent + elem)
      else:
         if(_print_none): print(_indent + 'example: None')
