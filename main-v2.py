# 首先，我们导入了 Flask 类。 这个类的实例就是我们的 WSGI 应用程序。
# 接下来，我们创建这个类的实例。 第一个参数是应用程序模块或软件包的名称。
# __name__ 是一个方便的快捷方式，适用于大多数情况。
# 这样，Flask 就能知道在哪里查找模板和静态文件等资源。 然后，我们使用 route() 装饰器告诉 Flask 什么 URL 应触发我们的函数。 该函数返回我们希望在用户浏览器中显示的信息。
# 默认内容类型是 HTML，因此字符串中的 HTML 将被浏览器渲染。

# 要运行应用程序，请使用 flask 命令或 python -m flask。
# 您需要使用 --app 选项告诉 Flask 应用程序的位置。
# flask --app main run


from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# 路由 现代网络应用程序使用有意义的 URL 来帮助用户。
# 如果页面使用了一个有意义的 URL，用户可以记住并直接访问该页面，那么他们就更有可能喜欢该页面并再次访问。
# 使用 route() 装饰器将函数绑定到 URL。


@app.route("/name", methods=["GET", "POST"])
def get_name():
    if request.method == "POST":
        return "<p>POST Cc</p>"
    else:
        return "<p>Get Cc</p>"


@app.route("/fans")
def get_fans():
    return "<p>10000</p>"

#一次性返回用户资料endpoint
@app.route("/userProfile", methods = ['GET','POST'])
def get_userProfile():
    if request.method == 'GET':
        #一般是返回结构化数据，例如josn,这样可以根据key比较方便的去拿到value
        #return "<p>name:cc, fans:10000</p>"
        name = request.args.get('name','')
        # print(name)
        return dict(name=name,fans=10000)
    elif request.method == 'POST':
        print(request.form) #ImmutableMultiDict([])
        print(request.data) #b'{\n\t"name": "cc"\n}'
        print(request.json) #{'name': 'cc'}
        # name = request.form[]
        name = request.json.get('name','')
        return dict(name=name,fans=10000)