#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers,
using the function do_deploy."""
from fabric.api import put, run, env
from os import path


env.hosts = ['54.160.124.170', '100.26.50.248']
env.user = 'ubuntu'
env.key_filename = "secret_key"

def do_deploy(archive_path):
    """Function to distribute an archive to your web servers."""
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        name = archive_path.split("/")[-1]
        name2 = name.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}".format(name2))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(name, name2))
        run("rm /tmp/{}".format(name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name2, name2))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name2))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name2))
        return True
    except:
        return False
