#!/usr/bin/env python
# -*- coding:utf8 -*-
__author__ = 'george'
import os
import sys
import urllib2
import re
import shutil
import commands

NGINX_SITE_URL = "http://www.nginx.org"
VERSION_PATTERN = '<a href="en/download.html">(.*)</a>'
DEFAULT_DOWNLOAD_DIR = os.getcwd()
DEFAULT_VERSION = "nginx-1.6.0"
DEFAULT_COMPRESS_FORMAT = ".tar.gz"
DEFAULT_INSTALL_DIR = '/usr/local/nginx'
CURRENT_DIR = os.getcwd()
nginx_init = '/etc/init.d/nginx'


def find_nginx_versions():
	"""列表Nginx所有的版本，返回Nginx版本数组"""
	response = urllib2.urlopen(NGINX_SITE_URL).read()

	versions = re.findall(VERSION_PATTERN, response)
	return versions[1:]


def download_nginx(nginx_version_name):
	"""下载Nginx压缩文件，tar.gz格式"""
	download_command = "wget " + NGINX_SITE_URL + "/download/" + nginx_version_name + DEFAULT_COMPRESS_FORMAT
	os.system(download_command)


def prepare_compile_env():
	"""准备编译环境"""
	base_softwares = "gcc gcc-c++ kernel kernel-devel pcre pcre-devel autoconf unzip zlib zlib-devel"
	yum_command = "yum -y install " + base_softwares
	os.system(yum_command)


def check_permission():
	"""判断当前用户是否是root"""
	return os.getuid() == 0


def check_version(nginx_version_name, versions):
	"""检查用户输入的版本是否正确，正确则返回版本名称"""
	while True:
		if nginx_version_name in versions:
			return nginx_version_name
		else:
			nginx_version_name = raw_input("输入的版本错误，请重新输入:")


def install_nginx(nginx_version_name):
	"""安装nginx软件"""
	prepare_compile_env()
	if check_permission() == False:
		print "请切换至root用户进行安装"
		return
	extract_command = "tar -zxvf " + nginx_version_name + DEFAULT_COMPRESS_FORMAT
	os.system(extract_command)
	os.system('groupadd nginx ')
	os.system('useradd nginx -g nginx -s /sbin/nologin ')
	os.chdir(nginx_version_name)
	configure_command = "./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_mp4_module --with-http_flv_module --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module"
	os.system(configure_command)
	os.system('make')
	os.system('make install')


def regst_ningx_service():
	"""将Nginx注册为服务的模式，开机自启动"""
	if check_permission():
		os.chdir(CURRENT_DIR)
		shutil.copyfile('nginx', '/etc/init.d/nginx')
		os.system('chkconfig --add nginx')
		os.system('chkconfig  nginx on --level 35')
		os.chmod(nginx_init, 700)
		# os.system(nginx_init + ' start')


def uninstall_nginx():
	"""卸载已经安装的NGINX服务"""

	if os.path.isfile(nginx_init):
		# check nginx is runging? stop it
		os.system(nginx_init + ' stop')

		# delete /etc/init.d/nginx
		os.remove(nginx_init)

	if os.path.isdir(DEFAULT_DOWNLOAD_DIR):
		# delete /usr/local/nginx dirctory
		shutil.rmtree(DEFAULT_INSTALL_DIR)

	print 'clean completed!'
def nginx_upgrade():
	"""升级nginx到新版本"""
	#check local version 
	if not os.path.exists(DEFAULT_INSTALL_DIR+'/sbin/nginx') :
		print 'Nginx未安装，请重新运行'
		sys.exit()

	cmd=DEFAULT_INSTALL_DIR+'/sbin/nginx -v'
	result=commands.getoutput(cmd)
	current_version='nginx-'+result.split(':')[1].split('/')[1]
	print '当前版本:%s'%current_version

	#print version list
	version_list=find_nginx_versions()
	print "可选版本:"
	for version in version_list:
		if version !=current_version:
			print version
	new_version=raw_input("请输入新的版本号:")
	download_nginx(new_version)
	extract_command='tar -zxvf '+new_version+DEFAULT_COMPRESS_FORMAT
	os.system(extract_command)
	os.chdir(new_version)



if __name__ == "__main__":

	command = raw_input("请输入操作指令,I:安装  UI:卸载 默认为[I]")
	if command == "UI":
		uninstall_nginx()
	elif command == "I":

		versions = find_nginx_versions()
		print "【版本列表】"
		for version in versions:
			print version

		select_version = raw_input('默认为【nginx-1.6.0】:')
		if select_version.strip() == "":
			select_version = DEFAULT_VERSION
		select_version = check_version(select_version, versions)

		download_dir = raw_input("请输入下载目录【默认为当前目录】")
		if download_dir.strip() == "":
			download_dir = DEFAULT_DOWNLOAD_DIR
		if download_dir != DEFAULT_DOWNLOAD_DIR:
			os.chdir(download_dir)
		download_nginx(select_version)
		install_nginx(select_version)
		regst_ningx_service()
		print "Nginx安装目录:", DEFAULT_INSTALL_DIR
		print "Nginx启动路径:", nginx_init
	elif command =="U":
		pass
	else:
		print 'exit'

