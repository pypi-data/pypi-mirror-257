import pyjs

from cwclientlib.cwproxy import CWProxy


def cwproxy_for(section):
    return CWProxy(pyjs.js.location.origin)
