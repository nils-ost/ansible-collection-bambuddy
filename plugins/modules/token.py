#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <home@nijos.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: token

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: fetch bambuddy API token (login)

description:
    - If authentication is enabled, BamBuddy API calls require a valid token
    - this module fetches such tokens from your instance, by logging in with username and password
    - which then can be used for other modules in this collection
    - in case autehntication is not enabled, this module can be used to build the base URL for API instance, which can be handy in some circumstances

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
            - user to authenticate on bambuddy instance
        required: false
        type: str
        default: null
    password:
        description:
            - password to authenticate on bambuddy instance
        required: false
        type: str
        default: null
"""

EXAMPLES = r"""
# fetch a token
- name: fetch bambuddy API token
  nils_ost.bambuddy.token:
    host: "{{ ansible_host }}"
    user: "{{ root_user }}"
    password: "{{ root_password_long }}"
  delegate_to: localhost
  register: bambuddy
"""

RETURN = r"""
url:
    description:
        - the URL build from protocol, host and port, to be used on other modules
    type: str
    returned: always
    sample: 'http://192.168.0.6:8000'
token:
    description:
        - newly created API token for given user
        - can be null if login failed or user is null
    type: str
    returned: always
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
        token=None,
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
        result[
            "url"
        ] = f"{module.params['protocol']}://{module.params['host']}:{module.params['port']}"

        if module.params["user"] is None or module.params["user"] == "":
            module.exit_json(**result)

        headers = dict()
        headers["Content-Type"] = "application/json"

        data = dict(
            username=module.params["user"],
            password=module.params["password"],
        )

        response = requests.post(
            result["url"] + "/api/v1/auth/login",
            json=data,
            headers=headers,
        )

        if not response.status_code == 200:
            module.fail_json(
                msg=f"error on fetching API token: {response.text}",
                **result,
            )

        if "access_token" not in response.json():
            module.fail_json(msg="API response not containing a token", **result)

        result["token"] = response.json().get("access_token")
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()
