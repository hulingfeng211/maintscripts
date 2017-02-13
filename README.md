#maintscripts


* `nginx/nginx.py`
> HTTP Server nginx automation install script that support `**upstar**` and `**systemd**`,该脚本运行需要连接互联网

用法如下：

    python -m nginx/nginx --command install  --prfix-dir /usr/local   #安装`nginx`并指定安装路径
    
    python -m nginx/nginx --command uninstall #卸载
     
    python -m nginx/nginx --command upgrade   #升级`nginx`
     
     

* `tornado-app-init.py`

> generate SPA project structure base **tornado** and **react**
>usage:

   ```python  ./tornado-app-init.py```
   
生成的目录如下：

```
    ├── common #公共模块目录
    │   ├── __init__.py
    ├── config.py #站点配置
    ├── handler #handler目录
    │   ├── __init__.py
    ├── manager.py #应用站点入口
    ├── README.md
    ├── routes.py 站点路由
    ├── static
    │   ├── css
    │   │   └── readme.md
    │   ├── img
    │   │   └── readme.md
    │   ├── js
    │   │   ├── bundle.js
    │   │   ├── components
    │   │   ├── index.jsx
    │   │   └── readme.md
    │   ├── lib
    │   │   └── readme.md
    │   ├── node_modules
    │   │   ├── babel-core
    │   │   ├── babel-loader
    │   │   ├── react
    │   │   ├── react-bootstrap
    │   │   ├── react-dom
    │   │   ├── react-router
    │   │   ├── react-router-bootstrap
    │   │   ├── tcomb-form
    │   │   └── webpack
    │   ├── package.json
    │   └── webpack.config.js
    └── templates
        ├── index.html
        └── readme.md
        
```

* `ssl/selfsigncert.py`
> 生成自签名的ssl证书的脚本

用法：
    
    python ssl/selfsigncer.py  filename 
    
需要使用管理员帐号才能运行,机器上需要安装`openssl`,创建的证书在当前目录.配置nginx的ssl可以参考下面的配置:

```
    server {
		listen       xx:443;
		server_name  xx.xx.com ;

		ssl                  on;
        
		access_log logs/ssl-access.log;
		error_log  logs/ssl-error.log;

		ssl_certificate      ssl/chinasws.com.crt;
		ssl_certificate_key  ssl/chinasws.com.key;

		ssl_session_timeout  5m;
		ssl_protocols  SSLv2 SSLv3 TLSv1;
		ssl_ciphers  HIGH:!aNULL:!MD5;
		ssl_prefer_server_ciphers   on;
		keepalive_timeout 60;
		ssl_session_cache shared:SSL:10m;
		
		...
}
```
