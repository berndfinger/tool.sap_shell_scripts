#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Author: Bernd Finger
#
# Purpose: Update a role's defaults/main.yml file with all vars entries from the role's meta/argument_specs.yml file
#
# update-role-defaults_main.sh role_directory
#
# $1: Root directory of the role
#
# Example:
# update-role-defaults_main.sh ~/.ansible/collections/ansible_collections/community/sap_install/roles/sap_netweaver_preconfigure

set -o nounset
set -o pipefail

usage () {
   echo "update-role-defaults_main.sh: Update a role's defaults/main.yml file with all vars entries from the role's meta/argument_specs.yml file"
   echo "Usage: update-role-defaults_main.sh [role_directory] [-h|--help]"
   echo "  role_directory             directory where the role resides"
   echo "  -h|--help                  display this help and exit"
   echo ""
   echo "Requires:"
   echo "- create-defaults_main-from-argument_specs.py: Python program for displaying the new defaults/main.yml file"
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
_DEFAULTS_MAIN_PATH="${_ROLE_DIRECTORY}/defaults/main.yml"
echo File argument_specs.yml: ${_ARGUMENT_SPECS_PATH}
echo File defaults/main.yml: ${_DEFAULTS_MAIN_PATH}

if [[ ! -f ${_ARGUMENT_SPECS_PATH} ]]; then
   echo "File ${_ARGUMENT_SPECS_PATH} does not exist. Exit."
   exit 1
fi

if [[ ! -f ${_DEFAULTS_MAIN_PATH} ]]; then
   echo "INFO: File ${_DEFAULTS_MAIN_PATH} does not yet exist."
fi

echo "Identifying create-readme-from-argument_specs.py..."
if [[ -f ${PWD}/create-defaults_main-from-argument_specs.py && -x ${PWD}/create-defaults_main-from-argument_specs.py ]]; then
   _CREATE_DEFAULTS_MAIN_FROM_ARGUMENT_SPECS_PATH="${PWD}/create-defaults_main-from-argument_specs.py"
elif [[ -f ./create-defaults_main-from-argument_specs.py && -x ./create-defaults_main-from-argument_specs.py ]]; then
   _CREATE_DEFAULTS_MAIN_FROM_ARGUMENT_SPECS_PATH="./create-defaults_main-from-argument_specs.py"
else
   _CREATE_DEFAULTS_MAIN_FROM_ARGUMENT_SPECS_PATH=$(which create-readme-from-argument_specs.py)
   _RC1=$?
   if [[ ${_RC1} != 0 ]]; then
      echo "No file create-readme-from-argument_specs.py found in PWD, ., or PATH. Exit."
      exit 1
   fi
fi

_TMP_README_DIR=$(mktemp -d)
mkdir ${_TMP_README_DIR}/defaults

echo "${_CREATE_DEFAULTS_MAIN_FROM_ARGUMENT_SPECS_PATH} ${_ROLE_DIRECTORY} > ${_TMP_README_DIR}/defaults/main.yml"
${_CREATE_DEFAULTS_MAIN_FROM_ARGUMENT_SPECS_PATH} ${_ROLE_DIRECTORY} > ${_TMP_README_DIR}/defaults/main.yml

echo "Differences between existing and new version of defaults/main.yml:"
diff ${_DEFAULTS_MAIN_PATH} ${_TMP_README_DIR}/defaults/main.yml
_RC2=$?

if [[ ${_RC2} -eq 0 ]]; then
   echo "File defaults/main.yml is already up to date and will not be modified."
   rm ${_TMP_README_DIR}/defaults/main.yml
   rmdir ${_TMP_README_DIR}/defaults
   rmdir ${_TMP_README_DIR}
fi

echo "Press RETURN to copy ${_TMP_README_DIR}/defaults/main.yml to ${_DEFAULTS_MAIN_PATH}:"
read a
cp ${_TMP_README_DIR}/defaults/main.yml ${_DEFAULTS_MAIN_PATH}
echo "File ${_TMP_README_DIR}/defaults/main.yml has been modified."
echo "Press RETURN to remove ${_TMP_README_DIR}/defaults/main.yml and ${_TMP_README_DIR}:"
read b
rm ${_TMP_README_DIR}/defaults/main.yml
rmdir ${_TMP_README_DIR}/defaults
rmdir ${_TMP_README_DIR}
