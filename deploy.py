#!/bin/env python
#coding=utf-8

import sys
import json
import time
import logging

from func.overlord.client import Client

logging.basicConfig(level = logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = 'deploy.log',
    )

class BaseDeploy(object):
    def __init__(self, host):
        self.host = host

        logging.info("Contruct Func client on %s" % host)
        self.client = Client(host)

    def send(self, local, remote, file):
        logging.info("Send %s/%s to %s:%s/%s" % (local, file, self.host, remote, file))
        return self.client.local.copyfile.send("%s/%s" % (local, file), "%s/%s" % (remote, file))

    def run(self, cmd):
        logging.info("Run command[%s] on %s" % (cmd, self.host))
        res = self.client.command.run(cmd)
        return res

class FooYunDeploy(BaseDeploy):
    def __init__(self, host):
        super(FooYunDeploy, self).__init__(host)

        self.ret_ok = 0
        self.ret_err = -1
        self.res = {'host': self.host, 'ret': self.ret_err, 'ok': '', 'err': ''}

    def encode(self, res):
        return json.dumps(res, encoding='utf-8', ensure_ascii=False)

    def _stop(self, grep):
        res = self.run("ps x|fgrep '%s' |fgrep -v 'fgrep' |awk '{print $1}' |xargs kill -9" % grep)
        if res[self.host][0] != 0:
            logging.error("Stop fail: %s" % res)
            self.res['err'] = "Stop fail: %s" % res[self.host][2]
        else:
            self.res['ret'] = self.ret_ok
            self.res['ok'] = "Success"

        return self.res

    def stop(self, grep):
        res = self._stop(grep)
        return self.encode(res)

    def _restart(self, local, remote, file, start_cmd, grep):
        res = self.run("ls %s/%s" % (remote, file))
        if res[self.host][0] == 0 and res[self.host][1]:
            logging.warn("%s/%s existed, no need distribute" % (remote, file))
        else:
            res = self.send(local, remote, file)
            if res[self.host][0] != 0:
                logging.error("Send fail: %s" % res)
                self.res['err'] = "Send fail: %s" % res[self.host][2]
                return self.res

        res = self.run("ps x|fgrep '%s' |fgrep -v 'fgrep' |awk '{print $1}' |xargs kill -9" % grep)
        if res[self.host][0] != 0:
            logging.warn("Stop fail: %s" % res)

#        import pdb;pdb.set_trace()
        res = self.run("cd %s && tar xf %s" % (remote, file))
        if res[self.host][0] != 0:
            logging.error("Untar fail: %s" % res)
            self.res['err'] = "Untar fail: %s" % res[self.host][2]
            return self.res

        res = self.run(start_cmd)
        if res[self.host][0] != 0:
            logging.error("Start fail: %s" % res)
            self.res['err'] = "Start fail: %s" % res[self.host][2]
            return self.res

        t = 0.2
        logging.info("Sleep %0.1f seconds then check process" % t)
        time.sleep(t)
        res = self.run("ps x |fgrep '%s' |fgrep -v 'fgrep'" % grep)
        if res[self.host][0] != 0 or not res[self.host][1]:
            logging.error("Start fail, process exited: %s" % res)
            self.res['err'] = "Start fail, process exited"
            return self.res

        self.res['ret'] = self.ret_ok
        self.res['ok'] = "Success"

        return self.res


    def restart(self, local, remote, file, start_cmd, grep):
        res = self._restart(local, remote, file, start_cmd, grep)
        return self.encode(res)

def main(argv):
    deploy = FooYunDeploy(argv[1])
    method = {'restart': deploy.restart, 'stop': deploy.stop}

    return method[argv[0]](*tuple(argv[2:]))

def test():
    return main(('restart', 'platform1', '/home/func_local/tmp', 
            '/home/func_remote/local', 
            'app.tar.gz',
            "cd /home/func_remote/local/app && `pwd`/cmd arg1 arg2", 
        'cmd arg1 arg2'))

if __name__ == '__main__':
    try:
        res = main(sys.argv[1:])
        #res = test()
    except Exception, e:
        logging.error("Call error: %s" % e)
        res = {"host": sys.argv[2] if len(sys.argv) >= 3 else 'ERROR', "ok": "", "err": "argv%s: %s" % (sys.argv, e), "ret": -1}

    logging.info("Call Result: %s" % res)
    print res
