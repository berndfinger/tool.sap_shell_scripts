#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Author: Bernd Finger
#
# Purpose: Update a role's README.md file with all vars entries from the role's meta/argument_specs.yml file
#
# Make sure your role's README.md has two lines for denoting the start and end of the variables section, as follows:
# <!-- BEGIN: Role Input Parameters -->
#
# <!-- END: Role Input Parameters -->
#
# update-role-readme.sh role_directory
#
# $1: Root directory of the role
#
# Example:
# update-role-readme.sh ~/.ansible/collections/ansible_collections/community/sap_install/roles/sap_netweaver_preconfigure

set -o nounset
set -o pipefail

usage () {
   echo "update-role-readme.sh: Update a role's README.md file with all vars entries from the role's meta/argument_specs.yml file"
   echo "Usage: update-role-readme.sh [role_directory] [-h|--help]"
   echo "  role_directory             directory where the role resides"
   echo "  -h|--help                  display this help and exit"
   echo ""
   echo "Requires:"
   echo "- create-readme-from-argument_specs.py: Python program for displaying the new README.md file"
   echo ""
   echo "Note: A README.md file must already exist, and it must contain at least the following two lines:"
   echo "<!-- BEGIN: Role Input Parameters -->"
   echo "<!-- END: Role Input Parameters -->"
   echo "These two lines indicate the start and end of the variables section, which is created dynamically."
   echo "The rest of the README.md file is displayed without modification."
}

if [[ ${#} == 0 ]]; then
   usage
   exit 1
fi

options=":h-:"
while getopts "$options" opt; do
   case ${opt} in
      -)
         case "${OPTARG}" in
            help)
               usage
               exit 0
               ;;
            *)
               if [[ "$OPTERR" = 1 ]] && [[ "${options:0:1}" != ":" ]]; then
                  echo "Invalid option -${OPTARG}"
                  usage
               fi
               exit 0
               ;;
         esac;;
      h)
         usage
         exit 0
         ;;
      \?)
         echo "Invalid option -$OPTARG"
         usage
         exit 0
         ;;
   esac
done
shift "$((OPTIND-1))"

echo $0

_ROLE_DIRECTORY=${1}

_ROLE=$(echo ${_ROLE_DIRECTORY} | awk 'BEGIN{FS="/"}{print $NF}')

echo Role: ${_ROLE}

_ARGUMENT_SPECS_FILE="meta/argument_specs.yml"
_ARGUMENT_SPECS_PATH="${_ROLE_DIRECTORY}/${_ARGUMENT_SPECS_FILE}"
_README_PATH="${_ROLE_DIRECTORY}/README.md"
echo File argument_specs.yml: ${_ARGUMENT_SPECS_PATH}
echo File README.md: ${_README_PATH}

if [[ ! -f ${_ARGUMENT_SPECS_PATH} ]]; then
   echo "File ${_ARGUMENT_SPECS_PATH} does not exist. Exit."
   exit 1
fi

if [[ ! -f ${_README_PATH} ]]; then
   echo "File ${_README_PATH} does not exist. Exit."
   exit 1
fi

echo "Identifying create-readme-from-argument_specs.py..."
if [[ -f ${PWD}/create-readme-from-argument_specs.py && -x ${PWD}/create-readme-from-argument_specs.py ]]; then
   _CREATE_README_FROM_ARGUMENT_SPECS_PATH="${PWD}/create-readme-from-argument_specs.py"
elif [[ -f ./create-readme-from-argument_specs.py && -x ./create-readme-from-argument_specs.py ]]; then
   _CREATE_README_FROM_ARGUMENT_SPECS_PATH="./create-readme-from-argument_specs.py"
else
   _CREATE_README_FROM_ARGUMENT_SPECS_PATH=$(which create-readme-from-argument_specs.py)
   _RC1=$?
   if [[ ${_RC1} != 0 ]]; then
      echo "No file create-readme-from-argument_specs.py found in PWD, ., or PATH. Exit."
      exit 1
   fi
fi

_TMP_README_DIR=$(mktemp -d)

echo "${_CREATE_README_FROM_ARGUMENT_SPECS_PATH} ${_ROLE_DIRECTORY} > ${_TMP_README_DIR}/README.md"
${_CREATE_README_FROM_ARGUMENT_SPECS_PATH} ${_ROLE_DIRECTORY} > ${_TMP_README_DIR}/README.md

echo "Differences between existing and new version of README.md:"
diff ${_README_PATH} ${_TMP_README_DIR}/README.md
_RC2=$?

if [[ ${_RC2} -eq 0 ]]; then
   echo "File README.md is already up to date and will not be modified."
   rm ${_TMP_README_DIR}/README.md
   rmdir ${_TMP_README_DIR}
fi

echo "Press RETURN to copy ${_TMP_README_DIR}/README.md to ${_README_PATH}:"
read a
cp ${_TMP_README_DIR}/README.md ${_README_PATH}
echo "File ${_TMP_README_DIR}/README.md has been modified."
echo "Press RETURN to remove ${_TMP_README_DIR}/README.md and ${_TMP_README_DIR}:"
read b
rm ${_TMP_README_DIR}/README.md
rmdir ${_TMP_README_DIR}
