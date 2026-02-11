#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <@nils-ost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
from copy import deepcopy

import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: settings

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: configure common settings

description:
    - This module is able to configure instance wide common settings

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
    ams_humidity_good:
        description:
            - AMS humidity value lower or equal is in state green (value between 1 and 100)
        required: false
        type: int
        default: 40
    ams_humidity_fair:
        description:
            - AMS humidity value above which is in state red (value between 1 and 100)
        required: false
        type: int
        default: 60
    ams_temp_good:
        description:
            - AMS temperature value lower or equal is in state green
        required: false
        type: float
        default: 28.0
    ams_temp_fair:
        description:
            - AMS temperature value above which is in state red
        required: false
        type: float
        default: 35.0
    auto_archive:
        description:
            - Automatically save 3MF files when prints complete
        required: false
        type: bool
        default: true
    save_thumbnails:
        description:
            - Extract and save preview images from 3MF files
        required: false
        type: bool
        default: true
    capture_finish_photo:
        description:
            - Take a photo from printer camera when print completes
        required: false
        type: bool
        default: true
    camera_view_mode:
        description:
            - Camera opens in a separate browser window or in a resizable overlay on the main screen
        required: false
        type: str
        default: "window"
        choices: ["window", "embedded"]
    check_updates:
        description:
            - Automatically check for new versions on startup
        required: false
        type: bool
        default: true
    check_printer_firmware:
        description:
            - Check for printer firmware updates from Bambu Lab
        required: false
        type: bool
        default: true
    currency:
        description:
            - Currency for cost estimates
        required: false
        type: str
        default: "EUR"
        choices: ["USD", "EUR", "GBP", "CHF", "JPY", "CNY", "CAD", "AUD"]
    default_filament_cost:
        description:
            - Default filament cost per kg
        required: false
        type: float
        default: 25.0
    energy_cost_per_kwh:
        description:
            - Energy cost per kWh
        required: false
        type: float
        default: 0.15
    energy_tracking_mode:
        description:
            - Energy tracking by lifetime (total) or per print
        required: false
        type: str
        default: "total"
        choices: ["print", "total"]
    external_url:
        description:
            - The external URL where Bambuddy is accessible. Used for notification images and external integrations.
        required: false
        type: str
        default: same as url parameter
    ha_enabled:
        description:
            - Access smart plugs from Home Assistant
        required: false
        type: bool
        default: false
    ha_url:
        description:
            - Home Assistant URL
        required: false
        type: str
        default: ""
    ha_token:
        description:
            - Long-Lived Home Assistant Access Token
        required: false
        type: str
        default: ""
    library_archive_mode:
        description:
            - When printing from File Manager, create an archive entry
        required: false
        type: str
        default: "ask"
        choices: ["always", "never", "ask"]
    library_disk_warning_gb:
        description:
            - Show warning when free disk space falls below this threshold
        required: false
        type: float
        default: 5.0
    prometheus_enabled:
        description:
            - Expose printer data in Prometheus format
        required: false
        type: bool
        default: false
    prometheus_token:
        description:
            - if set, Prometheus requests must include Authorization: Bearer <token>
        required: false
        type: str
        default: ""
"""

EXAMPLES = r"""
# configure currency to USD and set energy costs
- name: configure energy costs
  nils_ost.bambuddy.settings:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    currency: USD
    energy_cost_per_kwh: 0.17
  delegate_to: localhost

# configure AMS values
- name: configure AMS
  nils_ost.bambuddy.settings:
    url: "{{ bambuddy.url }}"
    token: "{{ bambuddy.token }}"
    ams_humidity_good: 10
    ams_humidity_fair: 30
  delegate_to: localhost
"""

RETURN = r"""
"""


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        token=dict(type="str", required=False, default=None, no_log=True),
        ams_humidity_good=dict(type="int", required=False, default=40),
        ams_humidity_fair=dict(type="int", required=False, default=60),
        ams_temp_good=dict(type="float", required=False, default=28.0),
        ams_temp_fair=dict(type="float", required=False, default=35.0),
        auto_archive=dict(type="bool", required=False, default=True),
        save_thumbnails=dict(type="bool", required=False, default=True),
        capture_finish_photo=dict(type="bool", required=False, default=True),
        camera_view_mode=dict(
            type="str",
            required=False,
            default="window",
            choices=["window", "embedded"],
        ),
        check_updates=dict(type="bool", required=False, default=True),
        check_printer_firmware=dict(type="bool", required=False, default=True),
        currency=dict(
            type="str",
            required=False,
            default="EUR",
            choices=["USD", "EUR", "GBP", "CHF", "JPY", "CNY", "CAD", "AUD"],
        ),
        default_filament_cost=dict(type="float", required=False, default=25.0),
        energy_cost_per_kwh=dict(type="float", required=False, default=0.15),
        energy_tracking_mode=dict(
            type="str",
            required=False,
            default="total",
            choices=["print", "total"],
        ),
        external_url=dict(type="str", required=False, default=None),  # use url if none
        ha_enabled=dict(type="bool", required=False, default=False),
        ha_url=dict(type="str", required=False, default=""),
        ha_token=dict(type="str", required=False, default="", no_log=True),
        library_archive_mode=dict(
            type="str",
            required=False,
            default="ask",
            choices=["always", "never", "ask"],
        ),
        library_disk_warning_gb=dict(type="float", required=False, default=5.0),
        prometheus_enabled=dict(type="bool", required=False, default=False),
        prometheus_token=dict(type="str", required=False, default="", no_log=True),
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

        response = s.get(url + "/api/v1/settings/")
        if not response.status_code == 200:
            module.exit_json(
                msg="error fetching current settings",
                response=response.text,
                **result,
            )

        data = deepcopy(module.params)
        data.pop("url", None)
        data.pop("token", None)
        if data["external_url"] is None:
            data["external_url"] = url

        update_required = False
        for k, v in data.items():
            if not response.json().get(k, None) == v:
                update_required = True
                break

        if not update_required:
            module.exit_json(msg="all settings configured as required", **result)

        result["changed"] = True

        if module.check_mode:
            module.exit_json(msg="would now configure settings", **result)

        response = s.put(url + "/api/v1/settings/", json=data)
        if not response.status_code == 200:
            module.exit_json(
                msg="error configuring settings",
                response=response.text,
                **result,
            )

        module.exit_json(msg="configuring settings successful", **result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()
