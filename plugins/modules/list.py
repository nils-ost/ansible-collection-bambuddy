#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <@nils-ost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: list

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: lists all elements

description:
    - Fetches a list of all elements from type target

options:
    url:
        description:
            - the full URL of API-Endpoint
        required: true
        type: str
    token:
        description:
            - the token used for authentication on API-Endpoint
            - if token is ommited or set to null, an anonymous API call is executed
        required: false
        type: str
        default: null
    target:
        description:
            - element type to get list of
        required: false
        type: str
        default: "printer"
        choices: ["printer"]
"""

EXAMPLES = r"""
# fetches all existing printers
- name: Pulling existing printers
  nils_ost.bambuddy.list:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    target: printer
  delegate_to: localhost
  register: existing_printers
"""

RETURN = r"""
data:
    description:
        - list of existing elements of type target
    type: list
    returned: always
"""


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        token=dict(type="str", required=False, default=None, no_log=True),
        target=dict(
            type="str",
            required=False,
            default="printer",
            choices=["printer"],
        ),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        data=dict(),
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
        url = module.params["url"]

        s = requests.Session()
        s.headers["Content-Type"] = "application/json"
        if module.params["token"] is not None and not module.params["token"] == "":
            s.headers["Authorization"] = "Bearer %s" % module.params["token"]

        if module.params["target"] == "printer":
            uri = url + "/api/v1/printers/"
        else:
            module.fail_json(msg="invalid target", **result)

        response = s.get(uri)
        if not response.status_code == 200:
            module.fail_json(
                msg="error fetching list",
                response=response.text,
                **result,
            )

        result["data"] = response.json()

        module.exit_json(msg="fetching list successful", **result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()
