# create_role_files_from_argument_specs

Purpose: Update a role's `README.md` and `defaults/main.yml` files with all vars entries from a role's `meta/argument_specs.yml` file

The shell scripts `update-role-readme.sh` and `update-role-defaults_main.sh` are used for this purpose. Each of them is calling a
corresponding Python programs `create-readme-from-argument_specs.py` or `create-defaults_main-from-argument_specs.py` for creating
the content of the files.

The Python program `parse-argument_specs.py` reads a role's `meta/argument_specs.yml` and displays the content in a compact form. It
is not used by any of the other four programs but maybe it is useful for extending the functionality of this set of tools.

## The file README.md of the role

Make sure your role's `README.md` has two lines for denoting the start and end of the variables section, as follows:
- Start marker:
```
<!-- BEGIN: Role Input Parameters -->
```

- End marker:
```
<!-- END: Role Input Parameters -->
```

Run the following command to create the vars entries or replace existing ones by new ones after updating the role's `meta/argument_specs.yml` file:

```
# update-role-readme.sh role_directory
```

Example:
```
$ update-role-readme.sh ~/.ansible/collections/ansible_collections/community/sap_install/roles/sap_netweaver_preconfigure'
```

## The file defaults/main.yml of the role

The role's `defaults/main.yml` will be created freshly. The file will get start marker at the top and and end marker
at the bottom, as follows:
- Start marker:
```
# BEGIN: Default Variables for <role name>
```

  Example:
```
# BEGIN: Default Variables for sap_general_preconfigure
```

- End marker:
```
# END: Default Variables for <role name>
```

  Example:
```
# END: Default Variables for sap_general_preconfigure
```

Run the following command to create a new file defaults/main.yml after updating the role's `meta/argument_specs.yml` file:

```
$ update-role-defaults_main.sh role_directory
```

Example:
```
# update-role-defaults_main.sh ~/.ansible/collections/ansible_collections/community/sap_install/roles/sap_netweaver_preconfigure'
```

## Further information
[Role argument validation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation)

## List of roles which are using this mechanism
- [sll/sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
- [sll/sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure)
- [sll/sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
- [sll/sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster)

## Authors and acknowledgment
Bernd Finger

## License
Apache 2.0
