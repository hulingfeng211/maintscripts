#maintscripts
---

1.`nginx.py`
---

> HTTP Server nginx automation install script that support **upstar** and **systemd**

2.`tornado-app-init.py`
---
> generate SPA project structure base **tornado** and **react**
>usage:
* running script

   ``` ./tornado-app-init.py```
* The generated directory is as follows
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
