#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <@nils-ost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: virtual_printer

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: enable or disable virtual_printer feature

description:
    - This module enables (and configures) or disables virtual_printer feature of BamBuddy

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
    enabled:
        description:
            - state of virtual_printer
        required: false
        type: bool
        default: true
    accesscode:
        description:
            - accesscode (from slicer) for virtual printer
        required: false
        type: str
        default: '12345678'
    model:
        description:
            - virual_printer model
        required: false
        type: str
        default: 3DPrinter-X1-Carbon
        choices: ['N2S', 'N1', 'O1C', 'O1D', 'O1S', 'C11', 'C12', 'N7', '3DPrinter-X1', '3DPrinter-X1-Carbon', 'C13']
    mode:
        description:
            - mode of handling "prints" to virtual_printer
        required: false
        type: str
        default: 'immediate'
        choices: ['immediate', 'review', 'print_queue', 'proxy']
"""

EXAMPLES = r"""
# enable default X1C virtual_printer, with default accesscode
- name: enable virtual X1C printer
  nils_ost.bambuddy.virtual_printer:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
  delegate_to: localhost

# change cirtaul_printer to H2D (translation to O1D is done through role variable)
- name: enable virtual H2D printer
  nils_ost.bambuddy.virtual_printer:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    model: "{{ bambuddy_virtual_printer_models['H2D'] }}"
  delegate_to: localhost

# disable virtual_printer again
- name: disable virtual_printer
  nils_ost.bambuddy.virtual_printer:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    enable: false
  delegate_to: localhost
"""

RETURN = r"""
"""


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        token=dict(type="str", required=False, default=None, no_log=True),
        enabled=dict(type="bool", required=False, default=True),
        accesscode=dict(type="str", required=False, default="12345678"),
        model=dict(
            type="str",
            required=False,
            default="3DPrinter-X1-Carbon",
            choices=[
                "N2S",
                "N1",
                "O1C",
                "O1D",
                "O1S",
                "C11",
                "C12",
                "N7",
                "3DPrinter-X1",
                "3DPrinter-X1-Carbon",
                "C13",
            ],
        ),
        mode=dict(
            type="str",
            required=False,
            default="immediate",
            choices=["immediate", "review", "print_queue", "proxy"],
        ),
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
        url = module.params["url"]

        s = requests.Session()
        s.headers["Content-Type"] = "application/json"
        if module.params["token"] is not None and not module.params["token"] == "":
            s.headers["Authorization"] = "Bearer %s" % module.params["token"]

        response = s.get(url + "/api/v1/settings/virtual-printer")
        if not response.status_code == 200:
            module.exit_json(
                msg="error fetching current virtual_printer settings",
                response=response.text,
                **result,
            )

        update_required = False
        if not module.params["enabled"] == response.json()["enabled"]:
            update_required = True
        if module.params["enabled"]:
            if not module.params["mode"] == response.json()["mode"]:
                update_required = True
            if not module.params["model"] == response.json()["model"]:
                update_required = True

        if not update_required:
            module.exit_json(msg="configuration already as requested", **result)

        result["changed"] = True

        if module.check_mode:
            module.exit_json(msg="would have updated configuration", **result)

        if module.params["enabled"]:
            data = dict(
                access_code=module.params["accesscode"],
                enabled=module.params["enabled"],
                model=module.params["model"],
                mode=module.params["mode"],
            )
        else:
            data = dict(
                enabled=module.params["enabled"],
            )
        response = s.put(url + "/api/v1/settings/virtual-printer", params=data)
        if not response.status_code == 200:
            module.exit_json(
                msg="error setting configuration",
                response=response.text,
                **result,
            )

        module.exit_json(msg="setting configuration successful", **result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()
