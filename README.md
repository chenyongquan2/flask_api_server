# Introduce
flask_api_server
a web server with python flask

## requirement
pip install flask

## run
flask --app main run

## changeLog
v1:
实现api，演示api的get post，以及他的request里的param,query,body

v2:
1) 利用工厂模式去创建flask实例
https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/
2) 数据库实例的创建
https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
用sqllite是因为它是python built-in内嵌的数据库，不需要我们去搭建另外的数据库服务器

创建数据库实例:
flask --app flaskr-v2 init-db
会在instance目录里面多出来一个.sqllite的文件

v3:
CURD实现:
通过post，get，put，delete进行create，read，delete，update的操作。
其实一般不会直接写裸sql，不同框架都有成熟的orm（比如sqlalchemy），后面了解一下。