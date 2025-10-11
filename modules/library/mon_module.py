#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec={"one_name": {"type": "str", "required": True}}
    )

    one_name = module.params["one_name"]

    if one_name == "admin":
        module.fail_json(msg="Nom réservé !")

    module.exit_json(changed=True, msg=f"Bonjour {one_name}")

if __name__ == '__main__':
    main()