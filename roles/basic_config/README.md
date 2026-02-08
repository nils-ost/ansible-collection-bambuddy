# nils_ost.proxymanager.basic_config

**configures Nginx Proxy Manager with basic capabilities**

Version added: 1.0.0

- [Synopsis](#synopsis)
- [Role Variables](#role-variables)
  - [Structure of: proxymanager_custom_proxys](#structure-of-proxymanager_custom_proxys)
  - [Structure of: proxymanager_custom_redirections](#structure-of-proxymanager_custom_redirections)
- [Examples](#examples)
  - [Full configuration](#full-configuration)
  - [Use preconfigured certificate](#use-preconfigured-certificate)
  - [Just work with http](#just-work-with-http)

## Synopsis

configures Nginx Proxy Manager with some basic options

proxys and redirections can be created, updated and deleted. optionally a certificate can be used for proxys and redirections. requires already running proxymanager (e.g. through role `nils_ost.proxymanager.install_with_docker`)

## Role Variables

| Variable                         | Type | Default            | Comment                                                   |
| -------------------------------- | ---- | ------------------ | --------------------------------------------------------- |
| proxymanager_user_email          | str  | admin@some.domain  | email address configured for login (used for API login)   |
| proxymanager_user_password       | str  | yourSecre1Pas!word | password configured for login (used for API login)        |
| proxymanager_cert_domain         | str  | null               | domain of the checked (or created) root-certificate       |
| proxymanager_do_de_token         | str  | null               | do.de API token for creating let's encrypt certificate    |
| proxymanager_custom_proxys       | dict | null               | proxy hosts to be created (see below for structure)       |
| proxymanager_remove_proxys       | list | null               | proxy hosts to be removed (as list of domain names)       |
| proxymanager_custom_redirections | dict | null               | redirection hosts to be created (see below for structure) |
| proxymanager_remove_redirections | list | null               | redirection hosts to be removed (as list of domain names) |

### Structure of: proxymanager_custom_proxys

It's a dict of dicts, where the key of the top-level dictionary defines the domain name should be listening for this proxy.
The second-level (or value of the top-level dict) sets some variables for this proxy.

The possible variables on second-level are:

| Variable | Required | Comment                                  |
| -------- | -------- | ---------------------------------------- |
| host     | true     | the destination host the proxy points to |
| port     | true     | the destination port the proxy points to |

### Structure of: proxymanager_custom_redirections

It's a dict of dicts, where the key of the top-level dictionary defines the domain name should be listening for this redirection.
The second-level (or value of the top-level dict) sets some variables for this redirection.

The possible variables on second-level are:

| Variable | Required | Comment                                                   |
| -------- | -------- | --------------------------------------------------------- |
| dest     | true     | full destination address                                  |
| scheme   | true     | the forwarding scheme, can be one of: auto, http or https |

## Examples

### Full configuration

This example configures a certificate for `your.domain` (if not already done) a the root-dns is manages by domainoffensive.

In the next portion proxys are configured for `npm.your.domain` and `grafana.your.domain` with their corresponding targets.

Also one redirection from `pihole.your.domain` to `http://192.168.1.234:8080/admin` is configured.

To ensure `pihole.your.domain` is not already configured as a proxy and `npm.your.domain`, `grafana.your.domain` aren't used as redirections, those are expicitly ensured to be removed.

```yaml
---
proxymanager_user_email: root@your.domain
proxymanager_user_password: "password;)"

proxymanager_cert_domain: your.domain
proxymanager_do_de_token: AAAABBBBCCCC

proxymanager_custom_proxys:
  npm.your.domain:
    host: 192.168.1.234
    port: 81
  grafana.your.domain:
    host: 192.168.1.235
    port: 8000

proxymanager_remove_proxys:
  - pihole.your.domain

proxymanager_custom_redirections:
  pihole.your.domain:
    dest: 192.168.1.234:8080/admin
    scheme: http

proxymanager_remove_redirections:
  - npm.your.domain
  - grafana.your.domain
```

### Use preconfigured certificate

If you don't have your domain hosted by domainoffensive, you can still use it with this role.

First install your npm instance, than create (by hand) the certificate for `your.domain`.
By setting the variable `proxymanager_cert_domain` to `your.domain` (but leaving out `proxymanager_do_de_token`)
the role is still able, to pull the ID of your already created certificate and use it for proxy and redirection configurations.

```yaml
---
proxymanager_user_email: root@your.domain
proxymanager_user_password: "password;)"

proxymanager_cert_domain: your.domain

proxymanager_custom_proxys:
  npm.your.domain:
    host: 192.168.1.234
    port: 81
  grafana.your.domain:
    host: 192.168.1.235
    port: 8000

proxymanager_remove_proxys:
  - pihole.your.domain

proxymanager_custom_redirections:
  pihole.your.domain:
    dest: 192.168.1.234:8080/admin
    scheme: http

proxymanager_remove_redirections:
  - npm.your.domain
  - grafana.your.domain
```

### Just work with http

Also it's possible to ignore the use of https alltogether, by leaving out `proxymanager_cert_domain`.
Proxys and redirections can still be created, but are only reachable via http.

In this case just one (http aware) proxy is created.

```yaml
---
proxymanager_user_email: root@your.domain
proxymanager_user_password: "password;)"

proxymanager_custom_proxys:
  npm.your.domain:
    host: 192.168.1.234
    port: 81
```
