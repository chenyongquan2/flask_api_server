import os

from flask import Flask, request


# 用工厂模式去创建flask app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    from . import db

    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!123"

    @app.route("/name", methods=["GET", "POST"])
    def get_name():
        if request.method == "POST":
            return "<p>POST Cc</p>"
        else:
            return "<p>Get Cc</p>"

    @app.route("/fans")
    def get_fans():
        return "<p>10000</p>"

    # 一次性返回用户资料endpoint
    @app.route("/userProfile", methods=["GET", "POST"])
    def get_userProfile():
        if request.method == "GET":
            # 一般是返回结构化数据，例如josn,这样可以根据key比较方便的去拿到value
            # return "<p>name:cc, fans:10000</p>"
            name = request.args.get("name", "")
            # print(name)
            return dict(name=name, fans=10000)
        elif request.method == "POST":
            print(request.form)  # ImmutableMultiDict([])
            print(request.data)  # b'{\n\t"name": "cc"\n}'
            print(request.json)  # {'name': 'cc'}
            # name = request.form[]
            name = request.json.get("name", "")
            return dict(name=name, fans=10000)

    return app
