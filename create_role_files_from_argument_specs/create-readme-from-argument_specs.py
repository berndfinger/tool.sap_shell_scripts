#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
# Author: Bernd Finger
#
# Purpose: Create the a role's README.md file from the role's meta/argument_specs.yml file
#
# create-readme-from-argument_specs.py role_directory
#
# argv[1]: Root directory of the role
#
# Example:
# create-readme-from-argument_specs.py ~/.ansible/collections/ansible_collections/community/sap_install/roles/sap_netweaver_preconfigure
#
# Order of fields in README.md:
# 1 - ### parameter
# 2 - type
# 3 - default_value (if defined)
# 4 - possible values (if defined)
# 5 - description
# 6 - example (if defined)

import sys
import re
from tkinter import W
import yaml
import json

if(len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
   print("create-readme-from-argument_specs.py: Display a role's README.md file to stdout from the role's meta/argument_specs.yml file")
   print('Usage: create-readme-from-argument_specs.py role_directory')
   print('  role_directory: Root directory of the role')
   print('Note: A README.md file must already exist, and it must contain at least the following two lines:')
   print('<!-- BEGIN: Role Input Parameters -->')
   print('<!-- END: Role Input Parameters -->')
   print('These two lines indicate the start and end of the variables section, which is created dynamically.')
   print('The rest of the README.md file is displayed without modification.')
   exit(0)

role_directory = sys.argv[1]
role_name = re.split('/', role_directory)[-1]
argument_specs_file = 'meta/argument_specs.yml'

_indent = '  '
_debug = False

# Build a dictionary with the same structure as the output of ansible-doc:
argument_specs_dict = {
    role_name: {
        'collection': "",
        'path': role_directory + '/' + role_name
    }
}

argument_specs_path = role_directory + '/' + argument_specs_file
readme_path = role_directory + '/' + 'README.md'

_begin_pattern='<!-- BEGIN: Role Input Parameters -->'
_end_pattern='<!-- END: Role Input Parameters -->'

with open(readme_path) as file_readme:
   for _line in file_readme:
      if(_begin_pattern in _line):
         break
      print(_line, end='')

with open(argument_specs_path) as file_argument_specs:
    argument_specs_dict[role_name].update(yaml.safe_load(file_argument_specs))
    _vars_dict = (json.dumps(argument_specs_dict, indent=4, sort_keys=False, separators=(',', ': ')))

print(_begin_pattern)
print('## Role Input Parameters')

for key, value in list(argument_specs_dict.values())[0]['argument_specs']['main']['options'].items():
   print("### " + key)
   print("- _Type:_ `" + str(value['type'] + "`"), end='')
   if(value['type'] == 'list' and value['elements'] == 'dict'):
      print(' of dicts; elements:')
      for key_2, value_2 in list(argument_specs_dict.values())[0]['argument_specs']['main']['options'][key]['options'].items():
         print('  #### ' + key_2)
         print(_indent + '- _Type:_ ' + str(value_2['type']))
         print("")
         for elem in value_2['description']:
            print(_indent + elem)
#         print("")
#      if('example' in value):
#         _example=str(value['example'])
#         print(_indent + 'example: ')
#         _example_lines = re.split('\n', _example)
#         for elem in _example_lines:
#            print(_indent + _indent + elem)
#   else:
   print("")
   if('default' in value):
      if(value['type']) == 'bool':
         print("- _Default:_ `" + str(value['default']).lower() + "`")
      else:
         print("- _Default:_ `" + str(value['default']) + "`")
   if('choices' in value):
      print("- _Possible Values:_<br>")
      for elem in value['choices']:
         print ("  - `" + elem + "`")
   print("")
   for elem in value['description']:
      print(elem + "<br>")

#   if('required' in value):
#      print(_indent + 'required: ' + str(value['required']))
#   else:
#      print(_indent + 'required: false')

   print("")
   if('example' in value):
      _example=str(value['example'])
      print("Example:")
      print("")
      print("```yaml")
      _example_lines = re.split('\n', _example)
      for elem in _example_lines:
         print(elem)
      print("```")
      print("")

#   if(value['type'] == 'list' and value['elements'] == 'dict'):
#      print(' of dicts; elements:')

_continue_switch = False

# The rest of the README.md file, which also includes _end_pattern, is displayed here:
with open(readme_path) as file_readme:
   for _line in file_readme:
      if(_end_pattern in _line):
         _continue_switch = True
      if(_continue_switch):
         print(_line, end='')
