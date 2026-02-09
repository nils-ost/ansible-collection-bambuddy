#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <home@nijos.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: setup

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: executes initial setup

description:
    - this modules executes the initial setup (first steps)
    - if a username and password is given, authentication is enabled and the corresponding admin user created
    - if username is left empty, authentication is disabled and the setup is marked as completed

options:
    protocol:
        description:
            - wether http or https is used on bambuddy
        required: false
        type: str
        default: 'http'
        choices: ['http', 'https']
    host:
        description:
            - host (-address) of bambuddy API endpoint
        required: true
        type: str
    port:
        description:
            - host-port of bambuddy API endpoint
        required: false
        type: int
        default: 8000
    user:
        description:
            - username to be configured
        required: false
        type: str
        default: null
    password:
        description:
            - password to be configured for user
        required: false
        type: str
        default: null
"""

EXAMPLES = r"""
# setup with authentication disabled
- name: setup with authentication disabled
  nils_ost.bambuddy.setup:
    host: "{{ ansible_host }}"
  delegate_to: localhost

# setup with authentication enabled and create admin user
- name: setup with authentication
  nils_ost.bambuddy.setup:
    host: "{{ ansible_host }}"
    user: admin
    password "{{ bambuddy_password }}"
  delegate_to: localhost
"""

RETURN = r"""
"""


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        protocol=dict(type="str", default="http", choices=["http", "https"]),
        host=dict(type="str", required=True),
        port=dict(type="int", required=False, default=8000),
        user=dict(type="str", required=False, default=None),
        password=dict(type="str", required=False, default=None, no_log=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        url = f"{module.params['protocol']}://{module.params['host']}:{module.params['port']}"

        s = requests.Session()
        s.headers["Content-Type"] = "application/json"

        response = s.get(url + "/api/v1/auth/status")
        if not response.status_code == 200:
            module.fail_json(
                msg="error on fetching API status",
                response=response.text,
                **result,
            )

        if not response.json()["requires_setup"]:
            module.exit_json(msg="setup already completed", **result)

        if module.check_mode:
            result["changed"] = True
            module.exit_json(msg="would execute setup now", **result)

        result["changed"] = True
        if module.params["user"] is None or module.params["user"] == "":
            # just send a complete
            data = dict(
                auth_enabled=False,
            )
            response = s.post(url + "/api/v1/auth/setup", json=data)
            if not response.status_code == 200:
                module.fail_json(
                    msg="error on finishing setup",
                    response=response.text,
                    **result,
                )
        else:
            # setup admin user
            if module.params["password"] is None or module.params["password"] == "":
                module.fail_json(msg="password required to create admin user", **result)

            data = dict(
                admin_username=module.params["user"],
                admin_password=module.params["password"],
                auth_enabled=True,
            )
            response = s.post(url + "/api/v1/auth/setup", json=data)
            if not response.status_code == 200:
                module.fail_json(
                    msg="error on creating admin user",
                    response=response.text,
                    **result,
                )

        module.exit_json(msg="finished setup", **result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()
