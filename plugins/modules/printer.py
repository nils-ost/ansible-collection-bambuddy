#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <@nils-ost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: printer

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: manage printer

description:
    - Creates, updates or deletes a printer

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
    name:
        description:
            - descriptive name of printer
            - needs to be uniqe as it used as identifier for this module
        required: true
        type: str
    ip_address:
        description:
            - IP Address / Hostname of printer
        required: false (true if state equals present)
        type: str
        default: ""
    serial_number:
        description:
            - Serial Number of printer
        required: false (true if state equals present)
        type: str
        default: ""
    access_code:
        description:
            - From printer settings
        required: false (true if state equals present)
        type: str
        default: ""
    model:
        description:
            - Printer Model
        required: false
        type: str
        default: "X1C"
        choices: ["H2C", "H2D", "H2D Pro", "H2S", "X1E", "X1C", "X1", "P2S", "P1S", "P1P", "A1", "A1 Mini"]
    location:
        description:
            - Used to group printers and filter queue jobs
        required: false
        type: str
        default: ""
    auto_archive:
        description:
            - Auto-archive completed prints
        required: false
        type: bool
        default: true
    state:
        description:
            - whether a printer should exist or be deleted
        required: false
        type: str
        default: "present"
        choices: ["present", "absent"]
"""

EXAMPLES = r"""
# create an example printer
- name: create printer
  nils_ost.bambuddy.printer:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    name: test1
    ip_address: 192.168.0.55
    serial_number: 01P00A000000000
    access_code: 12345678
  delegate_to: localhost

# update location of previously created printer
- name: updatee printer
  nils_ost.bambuddy.printer:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    name: test1
    ip_address: 192.168.0.55
    serial_number: 01P00A000000000
    access_code: 12345678
    location: basement
  delegate_to: localhost

# delete previously created printer
- name: delete printer
  nils_ost.bambuddy.printer:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    name: test1
    state: absent
  delegate_to: localhost
"""

RETURN = r"""
data:
    description:
        - API information of created or updated print
        - is empty if state is absent
    type: dict
    returned: always
"""


def data_as_expected(d1, d2):
    for k in d1.keys():
        if k not in d2:
            return False
        if not d1.get(k) == d2.get(k):
            return False
    return True


def search(url, session, name):
    uri = f"{url}/api/v1/printers/"

    response = session.get(uri)
    if not response.status_code == 200:
        return (False, response.text)

    for item in response.json():
        if name == item.get("name", ""):
            return (True, item)
    return (True, None)


def create(url, session, data):
    uri = f"{url}/api/v1/printers/"

    response = session.post(uri, json=data)
    if not response.status_code == 200:
        return (False, response.text)
    return (True, response.json())


def update(url, session, item, data):
    uri = f"{url}/api/v1/printers/{item}"

    response = session.patch(uri, json=data)
    if not response.status_code == 200:
        return (False, response.text)
    return (True, response.json())


def delete(url, session, item):
    uri = f"{url}/api/v1/printers/{item}"

    response = session.delete(uri)
    if not response.status_code == 200:
        return (False, response.text)
    return (True, response.json())


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        token=dict(type="str", required=False, default=None, no_log=True),
        name=dict(type="str", required=True),
        ip_address=dict(type="str", required=False, default=""),
        serial_number=dict(type="str", required=False, default=""),
        access_code=dict(type="str", required=False, default=""),
        model=dict(
            type="str",
            required=False,
            default="X1C",
            choices=[
                "H2C",
                "H2D",
                "H2D Pro",
                "H2S",
                "X1E",
                "X1C",
                "X1",
                "P2S",
                "P1S",
                "P1P",
                "A1",
                "A1 Mini",
            ],
        ),
        location=dict(type="str", required=False, default=""),
        auto_archive=dict(type="bool", required=False, default=True),
        state=dict(
            type="str",
            required=False,
            default="present",
            choices=["present", "absent"],
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

        session = requests.Session()
        session.headers["Content-Type"] = "application/json"
        if module.params["token"] is not None and not module.params["token"] == "":
            session.headers["Authorization"] = "Bearer %s" % module.params["token"]

        if module.params["state"] == "present":
            for param in ["ip_address", "serial_number", "access_code"]:
                if module.params.get(param) == "":
                    module.fail_json(
                        msg=f'"{param}" is required if "state" is "present"',
                        **result,
                    )

        success, element = search(url, session, module.params["name"])
        if not success:
            module.fail_json(msg=f"error on searching for element: {element}", **result)

        if module.params["state"] == "present":
            data = dict(
                name=module.params["name"],
                ip_address=module.params["ip_address"],
                serial_number=module.params["serial_number"],
                access_code=module.params["access_code"],
                model=module.params["model"],
                location=module.params["location"],
                auto_archive=module.params["auto_archive"],
            )

            if element is None:
                if not module.check_mode:
                    success, element = create(url, session, data)
                    if not success:
                        module.fail_json(
                            msg="error on createing new element",
                            response=element,
                            **result,
                        )
                    result["changed"] = True
                    result["data"] = element
                    module.exit_json(msg="created element", **result)
                else:
                    result["changed"] = True
                    result["data"] = data
                    module.exit_json(msg="would have created a element", **result)

            else:
                if not module.check_mode:
                    if data_as_expected(data, element):
                        result["data"] = element
                        module.exit_json(
                            msg="element is already as expected",
                            **result,
                        )
                    success, element = update(url, session, element.get("id"), data)
                    if not success:
                        module.fail_json(
                            msg="error on updateing existing element",
                            response=element,
                            **result,
                        )
                    result["changed"] = True
                    result["data"] = element
                    module.exit_json(msg="updated element", **result)
                else:
                    result["changed"] = True
                    result["data"] = data
                    module.exit_json(
                        msg="would have updated element",
                        **result,
                    )

        else:
            if element is None:
                module.exit_json(msg="element is already deleted", **result)
            if not module.check_mode:
                success, element = delete(url, session, element.get("id"))
                if not success:
                    module.fail_json(
                        msg="error on deleteing element",
                        response=element,
                        **result,
                    )
                result["changed"] = True
                module.exit_json(msg="deleted element", **result)
            else:
                result["changed"] = True
                module.exit_json(msg="would have deleted a element", **result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()
