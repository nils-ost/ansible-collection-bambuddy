# nils_ost proxymanager Collection Release Notes

**Topics**

- <a href="#v1-1-0">v1\.1\.0</a>
  - <a href="#release-summary">Release Summary</a>
  - <a href="#minor-changes">Minor Changes</a>
  - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
  - <a href="#release-summary-1">Release Summary</a>
  - <a href="#new-modules">New Modules</a>
  - <a href="#new-roles">New Roles</a>

<a id="v1-1-0"></a>

## v1\.1\.0

<a id="release-summary"></a>

### Release Summary

Improvements regarding the virtual_printer \-\- it now works out\-of\-the box

<a id="minor-changes"></a>

### Minor Changes

- by adding parameters \'remote_interface_ip\' and \'target_printer_name\' all features of virtual_printer are now usable
- virtual_printer certificate is shown to be injected to slicer configuration
- virtual_printer ports are properly forwared for docker installations done by this collection

<a id="bugfixes"></a>

### Bugfixes

- some modules used exit_json in places where fail_json should be called

<a id="v1-0-0"></a>

## v1\.0\.0

<a id="release-summary-1"></a>

### Release Summary

This is the first proper release of <code>nils_ost\.bambuddy</code> collection on 2026\-02\-11\.
This release contains everything I need to setup my BamBuddy instance for what I like to use it\.

<a id="new-modules"></a>

### New Modules

- nils_ost\.bambuddy\.list \- lists all elements\.
- nils_ost\.bambuddy\.printer \- manage printer\.
- nils_ost\.bambuddy\.settings \- configure common settings\.
- nils_ost\.bambuddy\.setup \- executes initial setup\.
- nils_ost\.bambuddy\.token \- fetch bambuddy API token \(login\)\.
- nils_ost\.bambuddy\.virtual_printer \- enable or disable virtual_printer feature\.

<a id="new-roles"></a>

### New Roles

- nils_ost\.bambuddy\.basic_config \- configures basic BamBuddy capabilities\.
- nils_ost\.bambuddy\.install_with_docker \- installs BamBuddy within docker\.
