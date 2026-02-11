# nils_ost.bambuddy.basic_config

**configures BamBuddy with basic capabilities**

Version added: 1.0.0

- [Synopsis](#synopsis)
- [Role Variables](#role-variables)
  - [Structure of: bambuddy_common_settings](#structure-of-bambuddy_common_settings)
  - [Structure of: bambuddy_virtual_printer](#structure-of-bambuddy_virtual_printer)
  - [Structure of: bambuddy_printers](#structure-of-bambuddy_printers)
- [Full usage Example](#full-usage-example)
  - [Playbook](#playbook)
  - [Variables-Definition](#variables-definition)

## Synopsis

configures BamBuddy with some basic options. requires already running bambuddy instance (e.g. through role `nils_ost.bambuddy.install_with_docker`)

if your instance is not using authentication leave `bambuddy_user` set to `null` to let this role execute anonymous API requests

## Role Variables

| Variable                 | Type | Default | Comment                                                |
| ------------------------ | ---- | ------- | ------------------------------------------------------ |
| bambuddy_user            | str  | null    | username configured for login (used for API login)     |
| bambuddy_user_password   | str  | null    | password configured for login (used for API login)     |
| bambuddy_port            | int  | 8000    | port where the bambuddy API can be reached             |
| bambuddy_common_settings | dict | {}      | holds system wide configuration options and variables  |
| bambuddy_virtual_printer | dict | {}      | information if and how virtual_printer shoud be set up |
| bambuddy_printers        | dict | {}      | holds 3D-printers to be configured                     |

### Structure of: bambuddy_common_settings

This dict contains a lot of common settings for BamBuddy, which you are able to configure to your likeing.

> [!WARNING]
> Even if this variable is empty all settings are configured with their default values as shown in the table below

Following settings can be changed using this variable, none of this settings are required to be configured, as they all have a default value:

| Setting                 | Type  | Default | Comment                                                                                                             |
| ----------------------- | ----- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| ams_humidity_good       | int   | 40      | if AMS humidity value is lower or equal the state is green (value between 1 and 100)                                |
| ams_humidity_fair       | int   | 60      | if AMS humidity value is above the state is red (value between 1 and 100)                                           |
| ams_temp_good           | float | 28.0    | if AMS temperature value is lower or equal the state is green                                                       |
| ams_temp_fair           | float | 35.0    | if AMS temperature value is above the state is red                                                                  |
| auto_archive            | bool  | true    | Automatically save 3MF files when prints complete                                                                   |
| save_thumbnails         | bool  | true    | Extract and save preview images from 3MF files                                                                      |
| capture_finish_photo    | bool  | true    | Take a photo from printer camera when print completes                                                               |
| camera_view_mode        | str   | window  | Camera opens in a separate browser window or in a resizable overlay on the main screen (for choices see link below) |
| check_updates           | bool  | true    | Automatically check for new versions on startup                                                                     |
| check_printer_firmware  | bool  | true    | Check for printer firmware updates from Bambu Lab                                                                   |
| currency                | str   | EUR     | Currency for cost estimates (for choices see link below)                                                            |
| default_filament_cost   | float | 25.0    | Default filament cost per kg                                                                                        |
| energy_cost_per_kwh     | float | 0.15    | Energy cost per kWh                                                                                                 |
| energy_tracking_mode    | str   | total   | Energy tracking by lifetime (total) or per print (for choices see link below)                                       |
| external_url            | str   | null    | The external URL where Bambuddy is accessible. Used for notification images and external integrations.              |
| ha_enabled              | bool  | false   | Access smart plugs from Home Assistant                                                                              |
| ha_url                  | str   | ""      | Home Assistant URL                                                                                                  |
| ha_token                | str   | ""      | Long-Lived Home Assistant Access Token                                                                              |
| library_archive_mode    | str   | ask     | When printing from File Manager, create an archive entry (for choices see link below)                               |
| library_disk_warning_gb | float | 5.0     | Show warning when free disk space falls below this threshold                                                        |
| prometheus_enabled      | bool  | false   | Expose printer data in Prometheus format                                                                            |
| prometheus_token        | str   | ""      | if set, Prometheus requests must include Authorization: Bearer <token>                                              |

The full list of choices for camera_view_mode, currency, energy_tracking_mode and library_archive_mode can be found in module: [nils_ost.bambuddy.settings](https://github.com/nils-ost/ansible-collection-bambuddy/blob/main/docs/nils_ost.bambuddy.settings_module.rst)

#### Example

```yaml
bambuddy_common_settings:
  ams_humidity_good: 10
  ams_humidity_fair: 30
  currency: EUR
  default_filament_cost: 25.0
  energy_cost_per_kwh: 0.25
  energy_tracking_mode: total
```

### Structure of: bambuddy_virtual_printer

This dict contains the settings for BamBuddys virtual_printer, which you are able to configure to your likeing.

> [!WARNING]
> Even if this variable is empty all settings are configured with their default values as shown in the table below

Following settings can be changed using this variable, none of this settings are required to be configured, as they all have a default value:

| Setting    | Type  | Default             | Comment                                                                   |
| ---------- | ----- | ------------------- | ------------------------------------------------------------------------- |
| enabled    | bool  | false               | state of virtual_printer                                                  |
| accesscode | str   | 12345678            | accesscode (from slicer) for virtual printer                              |
| model      | str   | 3DPrinter-X1-Carbon | virual_printer model (for choices see link below)                         |
| mode       | str   | immediate           | mode of handling "prints" to virtual_printer (for choices see link below) |

The full list of choices for model and mode can be found in module: [nils_ost.bambuddy.virtual_printer](https://github.com/nils-ost/ansible-collection-bambuddy/blob/main/docs/nils_ost.bambuddy.virtual_printer_module.rst)

#### Example

```yaml
bambuddy_virtual_printer:
  enabled: true
  accesscode: 12345678
  model: N7
  mode: immediate
```

### Structure of: bambuddy_printers

It's a dict of dicts, where the key of the top-level dictionary defines the name of a printer.
The second-level (or value of the top-level dict) sets the variables for this printer.

> [!WARNING]
> If this variable is not empty, all printers (identified by their name) that are not contained in this dict, are purged when running this role.

The possible variables on second-level are:

| Variable      | Type | Required | Default | Comment                                      |
| ------------- | ---- | -------- | ------- | -------------------------------------------- |
| ip_address    | str  | false    | ""      | IP Address / Hostname of printer             |
| serial_number | str  | false    | ""      | Serial Number of printer                     |
| access_code   | str  | false    | ""      | From printer settings                        |
| model         | str  | false    | X1C     | Printer Model (for choices see link below)   |
| location      | str  | false    | ""      | Used to group printers and filter queue jobs |
| auto_archive  | bool | false    | true    | Auto-archive completed prints                |

The full list of choices for model can be found in module: [nils_ost.bambuddy.printer](https://github.com/nils-ost/ansible-collection-bambuddy/blob/main/docs/nils_ost.bambuddy.printer_module.rst)

#### Example

```yaml
bambuddy_printers:
  printer1:
    ip_address: 192.168.56.204
    serial_number: 01P00A000000001
    access_code: "12345678"
    location: basement
  printer2:
    ip_address: 192.168.56.206
    serial_number: 01P00A000000004
    access_code: "12345678"
    model: P1P
```

## Full usage Example

Here you have a practical example of a playbook using this role, with a corresponding variables definition.  
The playbook also installs docker and bambuddy within docker using the corresponding roles.

### Playbook

```yaml
- name: install and configure BamBuddy server

  hosts: buddy

  vars_files:
    - secrets.yml

  roles:
    - geerlingguy.docker
    - nils_ost.bambuddy.install_with_docker
    - nils_ost.bambuddy.basic_config
```

### Variables-Definition

```yaml
bambuddy_port: 8080
bambuddy_user: admin
bambuddy_user_password: "{{ root_password }}"
bambuddy_auto_upgrade: false

bambuddy_common_settings:
  ams_humidity_good: 10
  ams_humidity_fair: 30
  currency: EUR
  default_filament_cost: 25.0
  energy_cost_per_kwh: 0.25
  energy_tracking_mode: total

bambuddy_virtual_printer:
  enabled: true
  accesscode: 12345678
  model: "{{ bambuddy_virtual_printer_models['X1C'] }}"
  mode: immediate

bambuddy_printers:
  printer1:
    ip_address: 192.168.56.204
    serial_number: 01P00A000000001
    access_code: "{{ printer1_access_code }}"
    location: basement
  printer2:
    ip_address: 192.168.56.206
    serial_number: 01P00A000000004
    access_code: "{{ printer2_access_code }}"
    model: P1P
```

The variables `root_password`, `printer1_access_code` and `printer2_access_code` come from the vault file `secrets.yml` as defined in the playbook.

The variable `bambuddy_virtual_printer_models` is a helper to map common printer names, to what the API expects. It is provided by this roles default-variables, ready to be used in your variables-definition.

Personally I like to place a definition like this in a group_vars file, but as a host_vars file it would work the same (but just for one host, in case you have multiple BamBuddys ;) )
