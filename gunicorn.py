import os
 
def getCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")
 
bind = "127.0.0.1:4321"
workers = getCPUs()
backlog = 2048
worker_class = "gevent"
debug = False
daemon = True
pidfile = "/tmp/gunicorn-flaskpress.pid"
