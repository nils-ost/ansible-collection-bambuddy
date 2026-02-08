# nils_ost.proxymanager.install_with_docker

**installs Nginx Proxy Manager within docker**

Version added: 1.0.0

- [Synopsis](#synopsis)
- [Role Variables](#role-variables)
- [Example](#example)

## Synopsis

A role for installing Nginx Proxy Manager as a docker container with the help of compose.

This role mainly just creates the compose directory, places the compose-file and executes `docker compose up`.
It requires docker to be already installed on target system, including the compose plugin.
You might want to take a look at [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker) to install docker on your system.

## Role Variables

| Variable                   | Type | Default            | Comment                                                         |
| -------------------------- | ---- | ------------------ | --------------------------------------------------------------- |
| proxymanager_compose_dir   | str  | ~/proxymanager     | location where compose-file and volume directorys are created   |
| proxymanager_auto_upgrade  | bool | false              | whether container image is updated on role run or not           |
| proxymanager_user_email    | str  | admin@some.domain  | email address configured for login (only applys on initial run) |
| proxymanager_user_password | str  | yourSecre1Pas!word | password configured for login (only applys on initial run)      |

## Example

`group_vars/proxymanager.yml`

```yaml
---
proxymanager_compose_dir: "/opt/services/proxymanager"
proxymanager_auto_upgrade: true
proxymanager_user_email: root@your.domain
proxymanager_user_password: "password;)"
```
