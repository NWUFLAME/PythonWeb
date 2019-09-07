# Python WSGI服务器
环境准备:  
安装gevent协程库:pip install gevent(必需)  
安装对mysql的支持:pip install pymysql(可选)  
  
启动命令
python web_server.py 端口号
  
static文件夹用于放置静态文件，访问服务器IP:端口号将会默认访问static文件夹下的index.html。  

web_server.py文件无需修改，要添加自己的业务逻辑，只需要修改wsgi.py。  

其中用@route注解定义url路径，@route注解修饰的方法即为该路径的处理器。访问该处理器的完整路径为/api/具体的URL路径。

处理器都有params参数，类型为字典，代表url携带的参数，可以用params[参数名]取到值。  



