import os
import sys
import xmlrpclib
import urllib

from certmaster import SSLCommon
from certmaster.config import read_config
from func.commonconfig import FuncdConfig


class SSL_Transport(xmlrpclib.Transport):

    user_agent = "pyOpenSSL_XMLRPC/%s - %s" % ('0.1', xmlrpclib.Transport.user_agent)

    def __init__(self, ssl_context, timeout=None, use_datetime=0):
        if sys.version_info[:3] >= (2, 5, 0):
            xmlrpclib.Transport.__init__(self, use_datetime)
        self.ssl_ctx=ssl_context
        self._timeout = timeout

    def make_connection(self, host):
        # Handle username and password.
        try:
            host, extra_headers, x509 = self.get_host_info(host)
        except AttributeError:
            # Yay for Python 2.2
            pass
        _host, _port = urllib.splitport(host)
        if hasattr(xmlrpclib.Transport, 'single_request'):
            cnx_class = SSLCommon.HTTPSConnection
        else:
            cnx_class = SSLCommon.HTTPS
        return cnx_class(_host, int(_port), ssl_context=self.ssl_ctx, timeout=self._timeout)


class SSLXMLRPCServerProxy(xmlrpclib.ServerProxy):
    def __init__(self, uri, pkey_file, cert_file, ca_cert_file, timeout=None):
        self.ctx = SSLCommon.CreateSSLContext(pkey_file, cert_file, ca_cert_file)
        xmlrpclib.ServerProxy.__init__(self, uri, SSL_Transport(ssl_context=self.ctx, timeout=timeout), allow_none=True)


class FuncServer(SSLXMLRPCServerProxy):
    def __init__(self, uri, pem=None, crt=None, ca=None, timeout=None):
        self.pem = pem
        self.crt = crt
        self.ca = ca
        self.timeout = timeout

        SSLXMLRPCServerProxy.__init__(self, uri,
                                      self.pem,
                                      self.crt,
                                      self.ca,
                                      self.timeout)


if __name__ == "__main__":
    conf_dir = sys.exec_prefix
    minion_cfg = read_config("%s/etc/func/minion.conf" % conf_dir, FuncdConfig)
    port = minion_cfg.listen_port
    if port == '':
        port = 51234
    s = SSLXMLRPCServerProxy('https://localhost:%s/' % port, '%s/etc/pki/certmaster/slave.pem' % conf_dir, '%s/etc/pki/certmaster/slave.cert' % conf_dir, '%s/etc/pki/certmaster/ca/certmaster.crt' % conf_dir)
    f = s.ping(1, 2)
    print f
