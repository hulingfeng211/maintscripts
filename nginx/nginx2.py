#!/usr/bin/env python
# -*- coding:utf8 -*- 
""" 
+FileName:nginx2.py
+Author: george
+mail:hulingfeng211@163.com
+Created Time:2014年08月13日 星期三 13时11分56秒
Description: """
import os
import argparse
from nginx import Nginx

if __name__== "__main__":
	parse=argparse.ArgumentParser()
	command_help="""
	install: To install nginx server \n
	uninstall: To remove nginx server from local \n
	upgrad: To upgrad nginx server from low version to new version \n
	"""
	command=["install","uninstall","upgrad"]
	parse.add_argument('option',help=command_help)
	args=parse.parse_args()
	nginx=Nginx()	
	if args.option == command[0]:
		versions=nginx.get_version_list()
		for version in versions:
			print version
		ngxin.install()		
	elif args.option==command[1]:
		nginx.uninstall()
		pass
	elif args.option==command[2]:
		nginx.upgrad()
		pass
	else:
		parse.error("option not in (install,uninstall,upgrad),try again later")
		pass



