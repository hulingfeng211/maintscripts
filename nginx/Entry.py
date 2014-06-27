#!/usr/bin/env python
# -*- coding:utf8 -*-
__author__ = 'george'
import os
import urllib2
import re

NGINX_SITE_URL = "http://www.nginx.org"
VERSION_PATTERN = '<a href="en/download.html">(.*)</a>'
DEFAULT_DOWNLOAD_DIR = os.getcwd()
DEFAULT_VERSION = "nginx-1.6.0"
DEFAULT_COMPRESS_FORMAT = ".tar.gz"


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


if __name__ == "__main__":

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

    print download_dir
    print select_version