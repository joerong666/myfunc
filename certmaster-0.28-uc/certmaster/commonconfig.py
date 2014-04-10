"""
Default configuration values for certmaster items when
not specified in config file.

Copyright 2008, Red Hat, Inc
see AUTHORS

This software may be freely redistributed under the terms of the GNU
general public license.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""


import os
import sys
from config import BaseConfig, BoolOption, IntOption, Option

class CMConfig(BaseConfig):
    conf_dir = sys.exec_prefix

    log_level = Option('INFO')
    listen_addr = Option('')
    listen_port = IntOption(51235)
    cadir = Option('%s/etc/pki/certmaster/ca' % conf_dir)
    cert_dir = Option('%s/etc/pki/certmaster' % conf_dir)
    certroot =  Option('%s/var/lib/certmaster/certmaster/certs' % conf_dir)
    csrroot = Option('%s/var/lib/certmaster/certmaster/csrs' % conf_dir)
    cert_extension = Option('cert')
    autosign = BoolOption(False)
    sync_certs = BoolOption(False)
    peering = BoolOption(True)
    peerroot =  Option('%s/var/lib/certmaster/peers' % conf_dir)

class MinionConfig(BaseConfig):
    conf_dir = sys.exec_prefix

    log_level = Option('INFO')
    certmaster = Option('certmaster')
    certmaster_port = IntOption(51235)
    cert_dir = Option('%s/etc/pki/certmaster' % conf_dir)
