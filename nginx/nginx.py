#!/usr/bin/env python
# -*- coding:utf8 -*- 
''' 
+FileName:nginx.py
+Author: george
+mail:hulingfeng211@163.com
+Created Time:2014年07月02日 星期三 10时35分38秒
Description: '''
import os,urllib2,sys,re,shutil,commands

#常量定义
default_install_dir='/usr/local/ngxin'
version_pattern='<a href="en/download.html">(.*)</a>'
default_download_dir=os.getcwd()
default_compress_format='.tar.gz'
nginx_website_url='http://www.nginx.org'
default_version='nginx-1.6.0'
default_install_dir='/usr/local/nginx'
daemon_file_name='/etc/init.d/nginx'
current_dir=os.getcwd()
nginx_init='/etc/init.d/nginx'

class Nginx():
	"""Nginx类负责对Nginx软件的安装、卸载、升级"""
	def __init__(self):
		if not self.__check_permission():
			print "请切换至root用户进行操作"
			sys.exit()
		self.verions=[]
		self.configure_command='./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_mp4_module --with-http_flv_module --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module'
		pass
	def install(self,version=default_version):
		"""安装指定版本的NGINX"""
		file=__download(version)
		print "文件下载地址:",file	
		if __check_permission():
			print "请切换到root用户重新安装"
			sys.exit()

		__prepare_comple_env(self)
		#add user and group 
		os.system('groupadd nginx')
		os.system('useradd nginx -g nginx -s /sbin/nologin')
		os.chdir(version)
		os.system(self.configure_command)
		os.system('make')
		os.system('make install')

		os.chdir(current_dir)
		shutil.copy('nginx',nginx_init)
		os.system('chkconfig --add nginx')
		os.system('chkconfig nginx on --level 35')
		os.chmod(nginx_init,700)
		print "安装完成，请运行/etc/init.d/nginx start 启动nginx服务"

	def uninstal(self):
		"""卸载已经安装的NGINX"""
		if os.path.exists(nginx_init):
			os.system(nginx_init+' stop')
			os.remove(nginx_init)
		if os.path.isdir(default_install_dir):
			shutil.rmtree(default_install_dir)
	def upgrade(self,new_version):
		"""根据当前版本升级到新版本"""
		if not os.path.exists(default_install_dir+'/sbin/nginx'):
			print 'Nginx未安装，请重新选择操作'
			sys.exit()

		version_view=default_install_dir+'/sbin/nginx -v'
		result=commands.getoutput(version_view)
		current_version='nginx-'+result.split(':')[1].split('/')[1]
		print '当前版本:%s'%current_version
		print '可选版本:'
		version_list=get_version_list()
		for version in version_list:
			if version !=current_version:
				print version
		while True:
			new_version=raw_input("请输入新的版本号:")
			if new_version not in version_list:
				print '输入的版本格式不正确'
				continue
			if new_version<current_version:
				print "选择的版本小于当前的版本，不能进行升级"
				contains
			break
		self.__download(new_version)
		extract_command='tar -zxvf '+new_version+default_compress_format
		os.system(extract_command)
		os.chdir(new_version)
		os.system(self.configure_command)
		os.system('make')
		os.system('make install')
		os.system('make upgrade')
		print "升级成功"
		
	def __prepare_comple_env(self):
		"""准备基础的编译环境"""
		compnents="gcc gcc-c++ kernel kernel-devel pcre pcre-devel autoconf unzip zlib zlib-devel openssl openssl-devel"
		install_command="yum -y install "+compnents
		os.system(install_command)

	def self.__check_permission(self):
		"""当前用户是否是root用户"""
		return os.getuid()==0

	def self.__download(version=default_version):
		"""内部方法，根据指定的版本下载nginx压缩包，并返回下载后的路径"""
		download_dir=""
		while True:
			download_dir=raw_input("请输入下载地址，默认:"+default_download_dir)
			if download_dir.strip()=="":
				download_dir=default_download_dir
			elif os.path.isdir(download_dir):
				break
			else:
				print "请输入有效的文件路径"

		download_command='wget '+nginx_website_url+'/download'+version+default_compress_format
		os.system(download_command)
		return download_dir+"/"+version #目录+文件

	def get_version_list(self):
		"""获取NGINX当前维护的版本列表，返回版本列表"""
		if self.verions:
			return self.verions
		try:
			response=urllib2.urlopen(nginx_website_url).read()
			versions=re.findall(version_pattern,response)
			self.verions=verions[1:]
			return versions[1:]
		except:
			print '当前网络存在问题，请稍候重试'
			sys.exit()

if __name__== '__main__':
	nginx=Nginx()
	version_list=nginx.get_version_list()
	for version in version_list:
		print version


