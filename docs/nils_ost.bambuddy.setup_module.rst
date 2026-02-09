.. _nils_ost.bambuddy.setup_module:


***********************
nils_ost.bambuddy.setup
***********************

**executes initial setup**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- this modules executes the initial setup (first steps)
- if a username and password is given, authentication is enabled and the corresponding admin user created
- if username is left empty, authentication is disabled and the setup is marked as completed




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>host (-address) of bambuddy API endpoint</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">null</div>
                </td>
                <td>
                        <div>password to be configured for user</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">8000</div>
                </td>
                <td>
                        <div>host-port of bambuddy API endpoint</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>http</b>&nbsp;&larr;</div></li>
                                    <li>https</li>
                        </ul>
                </td>
                <td>
                        <div>wether http or https is used on bambuddy</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">null</div>
                </td>
                <td>
                        <div>username to be configured</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # setup with authentication disabled
    - name: setup with authentication disabled
      nils_ost.bambuddy.setup:
        host: "{{ ansible_host }}"
      delegate_to: localhost

    # setup with authentication enabled and create admin user
    - name: setup with authentication
      nils_ost.bambuddy.setup:
        host: "{{ ansible_host }}"
        user: admin
        password "{{ bambuddy_password }}"
      delegate_to: localhost




Status
------


Authors
~~~~~~~

- Nils Ost (@nils-ost)
