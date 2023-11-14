#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
# Author: Bernd Finger
#
# Purpose: Create the a role's defaults/main.yml file from the role's meta/argument_specs.yml file
#
# ./create-defaults-main-from-argument_specs.py role_directory
#
# argv[1]: Root directory of the role
#
# Example:
# ./create-defaults-main-from-argument_specs.py ~/.ansible/collections/ansible_collections/community/sap_install/roles/sap_netweaver_preconfigure
#
# Order of fields in defaults/main.yml (only for parameters for which a default is defined):
# 1 - parameter: default_value
# 2 - # description
# 3 - # possible values (as part of the description, if defined)

import sys
import re
from tkinter import W
import yaml
import json

if(len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
   print("create-defaults-main-from-argument_specs.py: Display a role's defaults/main.yml file to stdout from the role's meta/argument_specs.yml file")
   print('Usage: create-defaults-main-from-argument_specs.py role_directory')
   print('  role_directory: Root directory of the role')
   print('Note: The file defaults/main.yml is fully created by this program.')
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
defaults_main_path = role_directory + '/' + 'defaults/main.yml'

_begin_pattern='# BEGIN: Default Variables for ' + role_name
_end_pattern='# END: Default Variables for ' + role_name

with open(argument_specs_path) as file_argument_specs:
    argument_specs_dict[role_name].update(yaml.safe_load(file_argument_specs))
    _vars_dict = (json.dumps(argument_specs_dict, indent=4, sort_keys=False, separators=(',', ': ')))

print('---')
print(_begin_pattern)
print('')

for key, value in list(argument_specs_dict.values())[0]['argument_specs']['main']['options'].items():

   if('default' in value):
      print(key + ':', end='')
      if(('type' in value) and (value['type']) == 'bool'):
         print(' ' + str(value['default']).lower())
      else:
         if('{{' in str(value['default'])):
            print(' "' + str(value['default']) + '"')
         else:
            if('list' in str(type(value['default']))):
               print('')
               for elem in value['default']:
                  print('  - ' + elem)
            else:
               print(" '" + str(value['default']) + "'")
   else:
      print('# ' + key + ': (not defined by default)')

   for elem in value['description']:
      print('# ' + elem)
   if('choices' in value):
      print("# Possible Values:")
      for elem in value['choices']:
         print ("# - " + str(elem))

   if('example' in value):
      print("# Example: See README.md")

   print("")

print(_end_pattern)
