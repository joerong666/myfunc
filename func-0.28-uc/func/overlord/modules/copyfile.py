
import os
import stat
import sys
import xmlrpclib

from func.overlord import overlord_module

class copyfile(overlord_module.BaseModule):
    def send(self, localpath, remotepath, bufsize=10000000):
        host = self.parent.server_spec
        res = {host: [0, 'Send %s success', '']}
        try:
            f = open(localpath, "r")

            st = os.stat(localpath)
            mode = stat.S_IMODE(st.st_mode)

            ret = self.parent.run("copyfile", "open", [remotepath, mode])
            if ret[host] != 0: 
                return {host: [-1, '', ret[host]]}

            while True:
                data=f.read(bufsize)
                if data:
                    ret = self.parent.run("copyfile", "append", [remotepath, xmlrpclib.Binary(data)])

                    if ret[host] != 0: 
                        return {host: [-1, '', ret[host]]}

                else:
                    break

        except Exception, e:
            res = {host: [-1, '', str(e)]}

        return res
