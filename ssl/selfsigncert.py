#!/usr/bin/env python
# -*- coding:utf8 -*- 
"""#=====================================================
#	FileName:selfsigncert.py
#	Author: george
#	mail:hulingfeng211@163.com
#	Created Time:2014年11月03日 星期一 14时23分10秒
#	Description: 
#====================================================="""
import os
import sys
import argparse
root_cert_key='root'
root_C='CN'  #国家的缩写 CN、US等
root_ST='SH' #州或省
root_L='shanghai' #城市或地区
root_O='CSSC-SWS'#根证书颁发的证书的 O必须与根证书的O相同
root_OU='上海外高桥造船有限公司'#描述&说明，可以随意填写
root_crt_period_of_valid=5 #默认根证书5年的有效期
def create_private_key(keyname):
	print '创建证书私钥%s.key'%keyname
	private_key_command='openssl genrsa -out %s.key 2048'%keyname
	print private_key_command
	os.system(private_key_command)

def create_root_crt():
	create_private_key(root_cert_key)
	print '利用根证书私钥生成根证书'
	root_cert_command_temp="""openssl req -new -x509 -days %(period_of_valid)s -key %(domain)s.key -out %(domain)s.crt"""+ ' -subj "/C=%(C)s/ST=%(ST)s/L=%(L)s/O=%(O)s/OU=%(OU)s"'
	cert_data={
			'period_of_valid':root_crt_period_of_valid,
			'domain':root_cert_key,
			'C':root_C,
			'ST':root_ST,
			'L':root_L,
			'O':root_O,
			'OU':root_OU,

			}
	root_cert_command=root_cert_command_temp%cert_data
	print root_cert_command
	os.system(root_cert_command)

def create_ssl_csr(filename):
	domain=raw_input('请输入域名，注意不要输入wwww:')
	create_private_key(filename)
	csr_command_temp="""openssl req -new -key %(domain)s.key -out %(domain)s.csr"""+' -subj "/C=%(C)s/ST=%(ST)s/L=%(L)s/O=%(O)s/OU=%(OU)s/CN=%(CN)s"'
	C=raw_input('请输入国家，如(CN、US):')
	ST=raw_input('请输入州或省:')
	L=raw_input('请输入地区:')
	OU=raw_input('请输入单位:')
	cert_data={
			'domain':filename,
			'C':C,
			'ST':ST,
			'L':L,
			'O':root_O,
			'OU':OU,
			'CN':domain

			}
	csr_command=csr_command_temp%cert_data
	print csr_command
	os.system(csr_command)
	print '签名证书'
	sign_command_temp='openssl ca -in %(domain)s.csr -out %(domain)s.crt -cert %(root)s.crt -keyfile %(root)s.key'
	sign_command_data={
			'domain':filename,
			'root':root_cert_key
			}
	sign_command=sign_command_temp%sign_command_data
	print sign_command
	os.system(sign_command)


#funcation define to here 
if __name__== "__main__":
	if os.getuid()!=0:
		print '请切换root用户进行操作'
		sys.exit(1)
	parse=argparse.ArgumentParser()
	parse.add_argument('filename',help="域名信息")
	args=parse.parse_args()
	if not os.path.exists('/etc/pki/CA/index.txt'):
		os.system('touch /etc/pki/CA/index.txt')
	if not os.path.exists('/etc/pki/CA/serial'):
		os.system('echo "1000">/etc/pki/CA/serial')
	if not os.path.exists(root_cert_key+'.key'):
		create_root_crt()
	create_ssl_csr(args.filename)	

