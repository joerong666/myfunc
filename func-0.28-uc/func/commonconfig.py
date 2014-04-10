
"""
func

Copyright 2007, Red Hat, Inc
see AUTHORS

This software may be freely redistributed under the terms of the GNU
general public license.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""


import os
from certmaster.config import BaseConfig, BoolOption, Option, IntOption, FloatOption, ListOption

import sys
conf_dir = sys.exec_prefix
FUNCD_CONFIG_FILE = "%s/etc/func/minion.conf" % conf_dir
OVERLORD_CONFIG_FILE = "%s/etc/func/overlord.conf" % conf_dir

class FuncdConfig(BaseConfig):
    log_level = Option('INFO')
    acl_dir = Option('%s/etc/func/minion-acl.d' % conf_dir)
    certmaster_overrides_acls = BoolOption(True)

    listen_addr = Option('')
    listen_port = IntOption('51234')
    minion_name = Option('')

    method_log_dir = Option("%s/var/log/func/methods/" % conf_dir)
    use_certmaster = BoolOption(True)
    ca_file = Option('')
    cert_file = Option('')
    key_file = Option('')
    crl_location = Option('')
    module_list = ListOption([])


class OverlordConfig(BaseConfig):
    socket_timeout = FloatOption(0)
    listen_port = IntOption('51234')
    backend = Option('conf')
    group_db = Option('')
    key_file = Option('')
    cert_file = Option('')
    ca_file = Option('')
    delegate = BoolOption(False)
    puppet_minions = BoolOption(False)
    puppet_inventory = Option('%s/var/lib/puppet/ssl/ca/inventory.txt' % conf_dir)
    puppet_signed_certs_dir = Option('%s/var/lib/puppet/ssl/ca/signed' % conf_dir)
    puppet_crl = Option('%s/var/lib/puppet/ssl/ca/ca_crl.pem' % conf_dir)
    host_down_list = Option('%s/var/lib/func/hosts_down.lst' % conf_dir)
    allow_unknown_minions = BoolOption(False)
