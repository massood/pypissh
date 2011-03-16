import subprocess, socket
from httplib import HTTPConnection
import urllib2
from urllib2 import *

class PipeSocket:
    def __init__(self, proc):
        self.proc = proc
        self.filecount = 0

    def write(self, data):
        return self.proc.stdin.write(data)

    def read(self, amt=None):
        return self.proc.stdout.read(amt)

    def readline(self):
        return self.proc.stdout.readline()

    def sendall(self, data):
        return self.write(data)

    def makefile(self, mode, buffering=0):
        self.filecount += 1
        return self

    def close(self):
        if self.filecount:
            self.filecount -= 1
            return
        self.proc.stdout.close()
        self.proc.stdin.close()
        self.proc.wait()

class HTTPSSHConnection(HTTPConnection):
    def __init__(self, host, timeout=None):
        self.user, self.host = host.split('@')
        HTTPConnection.__init__(self, self.host, timeout=timeout)
        self.debuglevel = 1

    def connect(self):
        p = subprocess.Popen(['ssh', '-T', '-l', self.user, self.host],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.sock = PipeSocket(p)

class HTTPSSHHandler(AbstractHTTPHandler):
    def httpssh_open(self, req):
        return self.do_open(HTTPSSHConnection, req)

def build_opener(*handlers):
    return urllib2.build_opener(HTTPSSHHandler, *handlers)

_opener = None
def urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    global _opener
    if _opener is None:
        _opener = build_opener()
    return _opener.open(url, data, timeout)

def monkeypatch():
    import pypissh # ourselves
    from distutils.command import register, upload
    from distutils.config import PyPIRCCommand
    register.urllib2 = pypissh
    upload.urlopen = urlopen
    PyPIRCCommand.DEFAULT_REPOSITORY = 'httpssh://submit@pypi.python.org/pypi'

if __name__=='__main__':
    #import pdb; pdb.set_trace()
    f = urlopen('httpssh://submit@pypi.python.org/pypi')
    print f.read()

