# -*- coding:utf-8 -*- 
#=====================================
#	Creater:15921315347@163.com
#	Create Time:2016-06-21 15:42:11
#	Description: tornado project initialize script
#   dir list:
#├── common
#│   ├── __init__.py
#│   └── __init__.pyc
#├── config.py
#├── config.pyc
#├── handler
#│   ├── __init__.py
#│   └── __init__.pyc
#├── manager.py
#├── README.md
#├── routes.py
#├── routes.pyc
#├── static
#│   ├── css
#│   │   └── readme.md
#│   ├── img
#│   │   └── readme.md
#│   ├── js
#│   │   ├── bundle.js
#│   │   ├── components
#│   │   ├── index.jsx
#│   │   ├── js
#│   │   ├── node_modules
#│   │   ├── package.json
#│   │   ├── readme.md
#│   │   └── webpack.config.js
#│   └── lib
#│       └── readme.md
#└── templates
#    ├── index.html
#    └── readme.md

#      -app
#       -common 公共模块目录
#       -handler handler目录
#       -manager.py 应用站点入口 
#       -templates 网页模版文件文件目录 
#       -static  静态资源文件目录
#       -routes.py 站点路由
#       -config.py 站点配置
#       -README.md
#=====================================
import datetime 
import os 
import sys
import argparse

FILE_HEADER_TPL = """# -*- coding:utf-8 -*- 
#=====================================
#	Creater:%s
#	Create Time:%s
#	Description: 
#=====================================
"""
USEAGE="""initialize tornado web app
"""
parser = argparse.ArgumentParser(description=USEAGE)
parser.add_argument('--app', help="the app name default tornado-app",default='tornado-app')
parser.add_argument('--author', help='the app author',default='15921315347@163.com')
parser.add_argument('--port', default=11108,type=int, help='the app listen port,default 11108')
args = parser.parse_args()

MANAGER_CONTENT= """import routes
from common import settings 
from tornado.web import Application
from tornado.gen import IOLoop
from tornado.log import gen_log
from tornado.options import define,options ,parse_command_line

define('port',default=%s,type=int,help='listen port')
define('debug',default=True,type=bool,help='running at debug mode?')

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
	parse_command_line()
	handlers=[]
	handlers.extend(routes.routes)
	app = Application(handlers=handlers,**settings)
	gen_log.info('server listening at '+str(options.port))
	app.listen(options.port)
	IOLoop.current().start()
"""%(args.port,)
ROUTE_CONTENT = """import handler
from tornado.web import url,StaticFileHandler


routes = [
	url(r'/',handler.IndexHandler,dict(),name='app.home'),
	url(r"/page/(.*)", StaticFileHandler, {"path": "templates","default_filename":"index.html"})
]
"""
CONFIG_CONTENT= """import os 
DEBUG = True

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),'templates')

STATIC_PATH = os.path.join(os.path.dirname(__file__),'static')


"""

COMMON_CONTENT = """import config

def load_settings():
	settings = dict()
	for attr in dir(config):
		if attr.isupper():
			settings[attr.lower()]=getattr(config,attr)

	return settings

settings = load_settings()

"""
HANDLER_CONTENT = """from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
	def get(self,*args,**kwargs):
		self.render('index.html')


"""

INDEX_CONTENT = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Home</title>

    <!-- Bootstrap -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div id="container" class="container"></div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>-->
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <!-- <script src="/static/js/bootstrap.min.js"></script>-->
    <script src="/static/js/bundle.js"></script>
  </body>
</html>
"""
PACKAGE_CONTENT="""{
  "name": "react-app",
  "version": "1.0.0",
  "description": "react-app",
  "main": "index.js",
  "author": "escapedcat",
  "license": "ISC",
  "dependencies": {
    "react": "^15.1.0",
    "react-bootstrap": "^0.29.4",
    "react-dom": "^15.1.0",
    "react-router": "^2.4.1",
    "react-router-bootstrap": "^0.23.0",
    "tcomb-form": "^0.9.7"
  },
  "devDependencies": {
    "babel-core": "^5.8.24",
    "babel-loader": "^5.3.2",     
    "webpack": "^1.12.1"
  }
}
"""
WEBPACK_CONTENT="""module.exports = {
    entry: './index.jsx',
    output: {
        filename: 'bundle.js' //this is the default name, so you can skip it
    
    },
    module: {
        loaders: [
            
            {
                test: /\.jsx$/, exclude: /node_modules/, loader: "babel-loader"
            }
        ]
    },
    externals: {
        //don't bundle the 'react' npm package with our bundle.js
        //but get it from a global 'React' variable
        //'react': 'React'
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    }
}
"""
INDEX_JSX_CONTENT="""import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';

ReactDOM.render((<App />),document.getElementById('container'));

"""

APP_CONTENT="""import React from 'react';
import ReactDOM from 'react-dom';

class App extends React.Component {
	render(){
		return (<h1>Hello,React App </h1>);
	}
}
export default App
"""

PORJECT_DIR_STRUCTURE=[{'name':'common','children':[{'name':'__init__.py','content':COMMON_CONTENT}]},
	{'name':'handler','children':[{'name':'__init__.py','content':HANDLER_CONTENT}]},
	{'name':'manager.py','content':MANAGER_CONTENT},
	{'name':'templates','children':[{'name':'readme.md'},{'name':'index.html','nohead':True,'content':INDEX_CONTENT}]},
	{'name':'static','children':[{'name':'js','children':[{'name':'package.json','content':PACKAGE_CONTENT,'nohead':True},
	{'name':'webpack.config.js','content':WEBPACK_CONTENT,'nohead':True},
	{'name':'readme.md'},{'name':'index.jsx','content':INDEX_JSX_CONTENT,'nohead':True},
	{'name':'components','children':[{'name':'App.jsx','content':APP_CONTENT,'nohead':True}]}]},
	{'name':'img','children':[{'name':'readme.md'}]},
	{'name':'css','children':[{'name':'readme.md'}]},
	{'name':'lib','children':[{'name':'readme.md'}]}]},
	{'name':'routes.py','content':ROUTE_CONTENT},
	{'name':'config.py','content':CONFIG_CONTENT},
	{'name':'README.md'}]

def loop_create_dir(dir_or_file,dirname):
	"""create file or dir"""
	if dir_or_file.get('children',None):
		new_dir = dirname+'/'+dir_or_file.get('name')
		os.mkdir(new_dir)
		for child in dir_or_file.get('children'):
			loop_create_dir(child,new_dir)
	else:
		#os.mkdirs(dirname)
		with open(dirname+'/'+dir_or_file.get('name'),'a+') as f :
			if not dir_or_file.get('nohead',None):
				f.write(FILE_HEADER_TPL%(args.author,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
			f.write(dir_or_file.get('content',''))


if __name__ == '__main__':
	
	if os.path.exists(args.app):
		print '%s is exists. change name and re-try.'%(args.app)
		sys.exit(-1)

	os.mkdir(args.app)
	for item  in PORJECT_DIR_STRUCTURE:
		loop_create_dir(item,args.app)
	#print FILE_HEADER