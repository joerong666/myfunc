#!/usr/bin/python

import os
from distutils.core import setup
#from setuptools import setup,find_packages

import sys
conf_dir = sys.exec_prefix

NAME = "certmaster"
VERSION = "0.28"
SHORT_DESC = "%s remote configuration and management api" % NAME
LONG_DESC = """
A small pluggable xml-rpc daemon used by %s to implement various web services hooks
""" % NAME


if __name__ == "__main__":
 
        manpath    = "share/man/man1/"
        etcpath    = "%s/etc/%s" % (conf_dir, NAME)
        initpath   = "%s/etc/init.d/" % conf_dir
        logpath    = "%s/var/log/%s/" % (conf_dir, NAME)
	certdir    = "%s/var/lib/%s/" % (conf_dir, NAME)
	certmaster_cert_dir = "%s/var/lib/%s/%s" % (conf_dir, NAME, NAME)
	certmaster_cert_certs_dir = "%s/var/lib/%s/%s/certs" % (conf_dir, NAME, NAME)
	certmaster_cert_csrs_dir = "%s/var/lib/%s/%s/csrs" % (conf_dir, NAME, NAME)
	trigpath   = "%s/var/lib/%s/triggers/"% (conf_dir, NAME)
        pkipath    = "%s/etc/pki/%s" % (conf_dir, NAME)
        rotpath    = "%s/etc/logrotate.d" % conf_dir
        aclpath    = "%s/minion-acl.d" % etcpath
        setup(
                name="%s" % NAME,
                version = VERSION,
                author = "Lots",
                author_email = "func-list@redhat.com",
                url = "https://fedorahosted.org/certmaster/",
                license = "GPL",
		scripts = [
                     "scripts/certmaster", "scripts/certmaster-ca",
                     "scripts/certmaster-request", "scripts/certmaster-sync",
                ],
		# package_data = { '' : ['*.*'] },
                package_dir = {"%s" % NAME: "%s" % NAME
                },
		packages = ["%s" % NAME,
                ],
                data_files = [(initpath, ["init-scripts/certmaster"]),
                              (etcpath,  ["etc/minion.conf",
					  "etc/certmaster.conf",
			                  "etc/version"]),
                              (manpath,  ["docs/certmaster.1.gz"]),
                              (manpath,  ["docs/certmaster-request.1.gz"]),
                              (manpath,  ["docs/certmaster-ca.1.gz"]),
                              (manpath,  ["docs/certmaster-sync.1.gz"]),
			      (rotpath,  ['etc/certmaster_rotate']),
                              (logpath,  []),
			      (certdir,  []),
			      (certmaster_cert_dir, []),
			      (certmaster_cert_certs_dir, []),
			      (certmaster_cert_csrs_dir, []),
			      (etcpath,  []),
			      (pkipath,  []),
			      (aclpath,  []),
                              ("%s/peers"         % certdir,  []),
			      ("%s/sign/pre/"     % trigpath, []),
                              ("%s/sign/post/"    % trigpath, []),
                              ("%s/remove/pre/"   % trigpath, []),
                              ("%s/remove/post/"  % trigpath, []),
                              ("%s/request/pre/"  % trigpath, []),
                              ("%s/request/post/" % trigpath, []),
                ],
                description = SHORT_DESC,
                long_description = LONG_DESC
        )

