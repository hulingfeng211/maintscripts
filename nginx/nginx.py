#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""================================================ 
#	FileName:nginx.py
#	Author: george
#	email:hulingfeng211@163.com
#	Created Time:2014年07月02日 星期三 10时35分38秒
#	Description: 
==================================================="""
import os, urllib2, sys, re, shutil, commands
from tornado.options import options, define, parse_command_line
import requests
from tornado.log import gen_log

COMMAND_USEAGE = """install:install nginx from internet
		uninstall:uninstall local nginx 
		upgrade:upgrade nginx version from low to high
		versions:print nginx version list"""

define('prefix_dir', default='/usr/local/nginx', type=str, help="nginx's default install directory")
define('other_options', type=str, help="other's nginx module config. eg:--with-http_ssl_module", multiple=True)
define('command', default='versions', type=str, help=COMMAND_USEAGE)
# 常量定义
default_install_dir = '/usr/local/nginx'
version_pattern = '<a href="en/download.html">(.*)</a>'
default_download_dir = os.getcwd()
default_compress_format = '.tar.gz'
nginx_website_url = 'http://www.nginx.org'
default_version = 'nginx-1.6.0'
default_install_dir = '/usr/local/nginx'
daemon_file_name = '/etc/init.d/nginx'
current_dir = os.getcwd()
nginx_init = '/etc/init.d/nginx'
system_service_dir = '/lib/systemd/system/'

os_version = {
    'systemd': 0,
    'upstar': 1
}


class Nginx():
    """Nginx类负责对Nginx软件的安装、卸载、升级"""

    def __init__(self):
        if not self.__check_permission():
            print "请切换至root用户进行操作"
            sys.exit()
        self.verions = []
        self.system_version = self.__get_system_version()
        self.configure_command = './configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_mp4_module --with-http_flv_module --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module'
        pass

    def install(self):
        """安装指定版本的NGINX"""
        versions = self.get_version_list()
        for item in versions:
            print item
        version = raw_input('请输入nginx的版本，默认%s:' % default_version)
        # todo check version
        if version not in versions:
            print '请输入正确的nginx版本号'
            sys.exit(1)

        file = self.__download(version)
        print "文件下载地址:", file[0]
        self.__prepare_compile_env()
        # extract $version.tar.gz
        extract_command = 'tar -zxvf ' + version + default_compress_format
        os.system(extract_command)
        # add user and group
        os.system('groupadd nginx')
        os.system('useradd nginx -g nginx -s /sbin/nologin')
        os.chdir(version)

        os.system(self.configure_command)
        os.system('make')
        os.system('make install')

        self.__rgst_sytem_service()

        # remove download file
        os.remove(file[0] + file[1])
        shutil.rmtree(file[0])

    def __get_system_version(self):
        """获取操作系统版本，主要识别为el6和el7，返回对应的版本字符串"""
        # check system version

        if len(commands.getoutput('whereis systemd')[9:]) > 0:
            return 'systemd'
        else:
            return 'upstar'

    def __rgst_sytem_service(self):
        """将nginx注册为系统服务，在系统登陆时自动运行"""
        if self.system_version == 'upstar':
            os.chdir(current_dir)
            shutil.copy('nginx', nginx_init)
            os.system('chkconfig --add nginx')
            os.system('chkconfig nginx on --level 35')
            os.chmod(nginx_init, 700)
            os.system('/etc/init.d/nginx start')
        elif self.system_version == 'systemd':
            # construct nginx.service copy to /lib/systemd/system/
            nginx_service = """[Unit]
Description=The nginx HTTP server and reverse proxy server
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=%s/logs/nginx.pid
ExecStartPre=%s/sbin/nginx -t
ExecStart=%s/sbin/nginx 
ExecReload=/usr/bin/kill -s HUP $MAINPID 
ExecStop=/usr/bin/kill -s QUIT $MAINPID 
PrivateTmp=true

[Install]
WantedBy=multi-user.target
""" % (options.prefix_dir, options.prefix_dir, options.prefix_dir)

            target = open('nginx.service', 'w')
            target.write(nginx_service)
            target.close()
            shutil.copy('nginx.service', system_service_dir + 'nginx.service')
            os.system('systemctl enable nginx')
            os.system('systemctl start nginx')

    def uninstall(self):
        """卸载已经安装的NGINX"""
        if self.system_version == 'upstar':

            if os.path.exists(nginx_init):
                os.system(nginx_init + ' stop')
                os.remove(nginx_init)
            if os.path.isdir(default_install_dir):
                shutil.rmtree(default_install_dir)

        elif self.system_version == 'systemd':

            if os.path.exists(system_service_dir + 'nginx.service'):
                os.system('systemctl stop nginx')
                os.system('systemctl disable nginx')
                os.remove(system_service_dir + 'nginx.service')
            # remove install dir
            if os.path.isdir(default_install_dir):
                shutil.rmtree(default_install_dir)

            # remove download file.

    def upgrade(self):
        """根据当前版本升级到新版本"""
        if not os.path.exists(default_install_dir + '/sbin/nginx'):
            print 'Nginx未安装，请重新选择操作'
            sys.exit()

        version_view = default_install_dir + '/sbin/nginx -v'
        result = commands.getoutput(version_view)
        current_version = 'nginx-' + result.split(':')[1].split('/')[1]
        print '当前版本:%s' % current_version
        print '可选版本:'
        version_list = self.get_version_list()
        for version in version_list:
            if version != current_version:
                print version
        while True:
            new_version = raw_input("请输入新的版本号:")
            if new_version not in version_list:
                print '输入的版本格式不正确'
                continue
            if new_version < current_version:
                print "选择的版本小于当前的版本，不能进行升级"
                continue
            break
        self.__download(new_version)
        extract_command = 'tar -zxvf ' + new_version + default_compress_format
        os.system(extract_command)
        os.chdir(new_version)
        os.system(self.configure_command)
        os.system('make')
        os.system('make install')
        os.system('make upgrade')

        print "升级成功"

    def __prepare_compile_env(self):
        """准备基础的编译环境"""
        apt_get = ['ubuntu', 'debain']
        yum = ['centos', 'redhat']
        os_issue = commands.getoutput('uname -a ')

        if len(filter(lambda x: x in os_issue.lower(), apt_get)) > 0:
            need_components = ['libpcre3-dev', 'libpcre3', 'autoconf', 'openssl', 'libssl-dev']
            install_command = 'sudo apt-get install -y ' + ' '.join(need_components)
            pass
        elif len(filter(lambda x: x in os_issue.lower(), yum)) > 0:
            need_components = ['gcc', 'gcc-c++', 'kernel', 'kernel-devel',
                               'pcre', 'pcre-devel', 'autoconf', 'unzip', 'zlib',
                               'zlib-devel', 'openssl', 'openssl-devel']
            install_command = "yum -y install " + ' '.join(need_components)

        os.system(install_command)

    def __check_permission(self):
        """当前用户是否是root用户"""
        return os.getuid() == 0

    def __download(self, version=default_version):
        """内部方法，根据指定的版本下载nginx压缩包，并返回下载后的路径"""
        download_dir = ""
        while True:
            download_dir = raw_input("请输入下载地址，默认%s:" % default_download_dir)
            if download_dir.strip() == "":
                download_dir = default_download_dir
                break
            elif os.path.isdir(download_dir):
                break
            else:
                print "请输入有效的文件路径"

        download_command = 'wget ' + nginx_website_url + '/download/' + version + default_compress_format
        os.system(download_command)
        return download_dir + "/" + version, default_compress_format  # 目录+文件

    def get_version_list(self):
        """获取NGINX当前维护的版本列表，返回版本列表"""
        if self.verions:
            return self.verions
        try:
            response = requests.get(nginx_website_url)
            versions = re.findall(version_pattern, response.text)
            self.verions = versions[1:]
            return versions[1:]
        except Exception as e:
            gen_log.error(e)
            gen_log.info('当前网络存在问题，请稍候重试')
            sys.exit()

    def versions(self):
        versions = self.get_version_list()
        for item in versions:
            print item


def useage():
    """用法"""
    print """./nginx.py --help   # view options"""


def main():
    nginx = Nginx()
    command_map = {
        'install': nginx.install,
        'uninstall': nginx.uninstall,
        'versions': nginx.versions,
        'upgrade': nginx.upgrade
    }
    command = command_map.get(options.command, useage)
    command()


if __name__ == '__main__':
    parse_command_line()
    # res=requests.get('http://www.nginx.org')
    # print res.text
    main()
