.. _nils_ost.bambuddy.virtual_printer_module:


*********************************
nils_ost.bambuddy.virtual_printer
*********************************

**enable or disable virtual_printer feature**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module enables (and configures) or disables virtual_printer feature of BamBuddy




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
                    <b>accesscode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"12345678"</div>
                </td>
                <td>
                        <div>accesscode (from slicer) for virtual printer</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enabled</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>state of virtual_printer</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>immediate</b>&nbsp;&larr;</div></li>
                                    <li>review</li>
                                    <li>print_queue</li>
                                    <li>proxy</li>
                        </ul>
                </td>
                <td>
                        <div>mode of handling &quot;prints&quot; to virtual_printer</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>model</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>N2S</li>
                                    <li>N1</li>
                                    <li>O1C</li>
                                    <li>O1D</li>
                                    <li>O1S</li>
                                    <li>C11</li>
                                    <li>C12</li>
                                    <li>N7</li>
                                    <li>3DPrinter-X1</li>
                                    <li><div style="color: blue"><b>3DPrinter-X1-Carbon</b>&nbsp;&larr;</div></li>
                                    <li>C13</li>
                        </ul>
                </td>
                <td>
                        <div>virual_printer model</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remote_interface_ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                <td>
                        <div>override the listening IP of BamBuddy for virtual_printer</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target_printer_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                <td>
                        <div>in proxy mode the destination printer name</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">null</div>
                </td>
                <td>
                        <div>the token used for authentication on API-Endpoint</div>
                        <div>if token is ommited or set to null, an anonymous API call is executed</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>the full URL of API-Endpoint</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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

    # use proxy mode
    - name: enable virtual_printer in proxy mode
      nils_ost.bambuddy.virtual_printer:
        url: "{{ bambuddy.url }}"
        token: "{{ bambuddy.token }}"
        mode: proxy
        target_printer_name: test2
      delegate_to: localhost




Status
------


Authors
~~~~~~~

- Nils Ost (@nils-ost)
