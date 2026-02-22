===============================================
nils\_ost proxymanager Collection Release Notes
===============================================

.. contents:: Topics

v1.1.0
======

Release Summary
---------------

Improvements regarding the virtual_printer -- it now works out-of-the box

Minor Changes
-------------

- by adding parameters 'remote_interface_ip' and 'target_printer_name' all features of virtual_printer are now usable
- virtual_printer certificate is shown to be injected to slicer configuration
- virtual_printer ports are properly forwared for docker installations done by this collection

Bugfixes
--------

- some modules used exit_json in places where fail_json should be called

v1.0.0
======

Release Summary
---------------

This is the first proper release of ``nils_ost.bambuddy`` collection on 2026-02-11.
This release contains everything I need to setup my BamBuddy instance for what I like to use it.

New Modules
-----------

- nils_ost.bambuddy.list - lists all elements.
- nils_ost.bambuddy.printer - manage printer.
- nils_ost.bambuddy.settings - configure common settings.
- nils_ost.bambuddy.setup - executes initial setup.
- nils_ost.bambuddy.token - fetch bambuddy API token (login).
- nils_ost.bambuddy.virtual_printer - enable or disable virtual\_printer feature.

New Roles
---------

- nils_ost.bambuddy.basic_config - configures basic BamBuddy capabilities.
- nils_ost.bambuddy.install_with_docker - installs BamBuddy within docker.
