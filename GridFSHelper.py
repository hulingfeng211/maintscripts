#!/usr/bin/env python
# -*- coding:utf8 -*- 
""" 
+FileName:GridFSHelper.py
+Author: george
+mail:hulingfeng211@163.com
+Created Time:Mon 18 Aug 2014 03:37:39 PM CST
Description: """
import os
from bson import ObjectId
import gridfs
from pymongo import MongoClient
import argparse
import os
import sys


class GridFSHelper(object):
    """
        yum -y install python-pip
        pip install pymongo
        MongoDB文件系统的帮助类
    """

    def __init__(self, host='10.0.0.68', port=27017, dbName='fs', user=None, password=None):
        self._host = host
        self._port = port
        client = MongoClient(host=host, port=port)
        db = client[dbName]
        self._fs = gridfs.GridFS(db)

    def __del__(self):
        pass

    def put(self, file_path, **kwargs):
        return self._fs.put(open(file_path), **kwargs)

    def get(self, object_id):
        objectId = ObjectId(object_id)
        return self._fs.get(objectId)

    def delete(self, object_id):
        objectId = ObjectId(object_id)
        self._fs.delete(objectId)


    def list(self):
        return self._fs.list()

    def find(self, args, **kwargs):
        return self._fs.find(**kwargs)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="add file to mangodb gridfs ")
    parser.add_argument('filepath', help="file full path")
    parser.add_argument('--filename', help='file alias name')
    parser.add_argument('--keys', help='key word description this file')
    args = parser.parse_args()
    if args.filepath:
        # check file exist
        if not os.path.exists(args.filepath):
            print "file not find. type full path and confirm has permission access that"
            sys.exit(-1)
        helper = GridFSHelper()
        kwargs = {}
        if args.filename:
            kwargs["filename"] = args.filename
        else:
            kwargs["filename"] = args.filepath
        if args.keys:
            kwargs["keys"] = args.keys

        helper.put(args.filepath, **kwargs)

        # kwargs={"filename":"python1","filetype":"py","keys":"python mongo"}
        # file_id = helper.put('gridfs1.py', **kwargs)
        # print file_id
        #file_list = helper.list()
        #print file_list
        #outfile = helper.get("53f3f63c5aa0101236ccc8bb")
        #print  outfile.name
        #print  outfile.filename
        #print outfile
        #test(name='hu', sex = 'nan')
        #kwargs={"firstname":"hulingfeng",'lastName':"hulingfeng"}
        #test(**kwargs)
        #53f3f63c5aa0101236ccc8bb

