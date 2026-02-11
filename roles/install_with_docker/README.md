# nils_ost.bambuddy.install_with_docker

**installs BamBuddy within docker**

Version added: 1.0.0

- [Synopsis](#synopsis)
- [Role Variables](#role-variables)
- [Example](#example)

## Synopsis

A role for installing BamBuddy as a docker container with the help of compose.

This role mainly just creates the compose directory, places the compose-file and executes `docker compose up`.
It requires docker to be already installed on target system, including the compose plugin.
You might want to take a look at [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker) to install docker on your system.

## Role Variables

| Variable               | Type | Default       | Comment                                                         |
| ---------------------- | ---- | ------------- | --------------------------------------------------------------- |
| bambuddy_compose_dir   | str  | /opt/bambuddy | location where compose-file and volume directorys are created   |
| bambuddy_auto_upgrade  | bool | false         | whether container image is updated on role run or not           |
| bambuddy_port          | int  | 8000          | port to be used for web and API communication                   |
| bambuddy_timezone      | str  | Europe/Berlin | timezone to be set for container                                |
| bambuddy_user          | str  | null          | username configured for login (only applys on initial run)      |
| bambuddy_user_password | str  | null          | password configured for login (only applys on initial run)      |

> [!IMPORTANT]  
> if `bambuddy_user` is left (or set) to be `null` no authentication is set up for BamBuddy
> therefor web and API calls can be done anonymous without the need to login

## Example

`group_vars/bambuddy.yml`

```yaml
---
bambuddy_compose_dir: "/opt/services/bambuddy"
bambuddy_port: 8080
bambuddy_user: admin
bambuddy_user_password: test123
```
