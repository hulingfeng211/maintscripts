# -*- coding:utf-8 -*-
__author__ = 'george'

import os
import sys

import argparse

hosts = [
    {
        'ip': '127.0.0.1',
        'port': 27017,
        'db_path': '/data/db0'
    },
    {
        'ip': '127.0.0.1',
        'port': 27018,
        'db_path': '/data/db1'
    },
    {
        'ip': '127.0.0.1',
        'port': 27019,
        'db_path': '/data/db2'
    }
]

mongodb_bin = '/usr/local/src/mongodb/bin/mongod'

if __name__ == "__main__":
    # check user
    if os.getuid() != 0:
        print '必须切换为root用户才能执行'
        exit()
    parse = argparse.ArgumentParser()
    parse.add_argument('--cmd', default='start', help='start: start mongodb replica set stop:stop mongodb replica set '
                       )
    parse.add_argument('--name', default='foo', help='replica set name')
    args = parse.parse_args()
    if args.cmd == 'start':
        for index, host in enumerate(hosts):
            if not os.path.exists(host['db_path']):
                os.mkdir(host['db_path'])
            command = mongodb_bin + ' --fork --rest --httpinterface --syslog --dbpath %s --replSet %s --port %s --bind_ip %s' % (
            host['db_path'], args.name, host['port'], host['ip'])
            os.system(command)
    pass
