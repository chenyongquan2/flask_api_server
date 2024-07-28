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
    # 从当前目录(用 . 表示)导入一个名为 db 的模块或对象
    from . import db

    # 这条语句是调用 db 模块或对象的 init_app 方法。
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
    # R:Read 读取userProfile /GET
    # C:Create 创建一个userProfile/POST
    # U:Update 更新创建的userProfile /PUT
    # D:Delete 删除创建的userProfile /DELETE
    @app.route("/userProfile", methods=["GET", "POST", "PUT", "DELETE"])
    def userProfile():
        # def get_userProfile(): 错误起名方式，按照RSEST的规范，前面不用带上动词，动词交由method的get/post
        if request.method == "GET":
            # 一般是返回结构化数据，例如josn,这样可以根据key比较方便的去拿到value
            # return "<p>name:cc, fans:10000</p>"
            name = request.args.get("name", "")
            id = request.args.get("id", 1)
            print(id)
            # 从数据库里面去读取

            # 1获取数据库连接
            connection = db.get_db()

            # 2写sql
            # happy path(理想情况)
            # 下面这里sql注入的风险
            # 如果用户输入的 id 参数包含恶意的 SQL 代码,比如 1 OR 1=1，
            # 那么最终生成的 SQL 查询语句将变成:
            # SELECT * from userProfile where id=1 OR 1=1
            # 被注入的写法: query = "SELECT * from userProfile where id={}".format(id)
            # 查询语句中的参数值是通过占位符 ? 传递的,而不是直接嵌入到 SQL 语句中
            query = "SELECT * from userProfile where id = ?"
            # print(query)
            
            # 3执行sql 获取数据库的游标cursor
            # cursor 是数据库连接的一个句柄,它允许你执行 SQL 查询并获取结果
            # 它提供了对数据库查询结果的访问和操作能力
            # cursor = connection.execute(query)
            cursor = connection.execute(
                query, (id,)
            )  # 查询语句中的参数值是通过占位符 ? 传递的,而不是直接嵌入到 SQL 语句中
            print(cursor)

            # 4处理从数据库里读取的数据
            result = cursor.fetchall()
            print(result)  # 返回了一个list [<sqlite3.Row object at 0x000001E842480850>]
            # python中list和数组的区别:
            # - Python 中的 list 是一种动态数据结构,可以存储不同类型的元素。
            # - 而数组是一种固定大小的数据结构,通常用于存储相同类型的元素。
            if not result:
                return dict(result="failed", msg="id not existed")
            else:
                print(result[0])
                # 6返回结果给调用者
                return dict(
                    id=result[0]["id"],
                    username=result[0]["username"],
                    fans=result[0]["fans"],
                )
        elif request.method == "POST":
            # print(request.form)  # ImmutableMultiDict([])
            # print(request.data)  # b'{\n\t"name": "cc"\n}'
            print(request.json)  # {'name': 'cc'}
            # 获取post body中的name fans等
            name = request.json.get("name")
            fans = request.json.get("fans")
            queryNewRow = request.json.get("queryNewRow", False)

            # 插入新的数据到数据库
            connection = db.get_db()
            # query = "INSERT INTO userProfile (username,fans) values('{}',{})".format(name,fans)
            # print(query)
            # 执行sql
            # connection.execute(query)

            # 为了避免 SQL 注入的风险,更安全的做法是使用参数化查询,即使用占位符 (%s 或 ?) 来代替直接插入变量值
            # query = "INSERT INTO userProfile (username, fans) VALUES (%s, %d)" #会报错，因为在 SQLite 中,通常使用 ? 作为占位符,而不是 %d 或 %s
            query = "INSERT INTO userProfile (username, fans) VALUES (?, ?)"
            values = (name, fans)

            try:
                cursor = connection.execute(
                    query, values
                )  # execute的时候出错了，会在这里直接报错(抛异常)

                # commit 当你对数据库有改动的时候，需要commit，否则改动不会生效
                connection.commit()

                if not queryNewRow:
                    return dict(result="ok")
                else:
                    print(cursor.lastrowid)
                    query = "SELECT * from userProfile where id = ?"
                    cursor = connection.execute(query, (cursor.lastrowid,))
                    result = cursor.fetchall()
                    return dict(
                        result="ok",
                        id=result[0]["id"],
                        username=result[0]["username"],
                        fans=result[0]["fans"],
                    )

            # except:#catch(error):
            except Exception as e:
                return dict(result="fail", error=str(e))

        elif request.method == "PUT":
            print(request.json)
            # 获取post body中的name fans等
            id = request.json.get("id")
            name = request.json.get("name")
            fans = request.json.get("fans")
            queryNewRow = request.json.get("queryNewRow", False)

            # 更改已有的数据到数据库
            connection = db.get_db()
            # 为了避免 SQL 注入的风险,更安全的做法是使用参数化查询,即使用占位符 (?) 来代替直接插入变量值
            query = "UPDATE userProfile SET username = ?, fans = ? WHERE id = ?"
            values = (name, fans, id)
            print(name, fans, id)

            try:
                cursor = connection.execute(
                    query, values
                )  # execute的时候出错了，会在这里直接报错(抛异常)

                # commit 当你对数据库有改动的时候，需要commit，否则改动不会生效
                connection.commit()

                if not queryNewRow:
                    return dict(result="ok")
                else:
                    print(id)
                    query = "SELECT * from userProfile where id = ?"
                    values = (id,)  # 注意要使用逗号将单个值包裹成元组
                    cursor = connection.execute(
                        query, values
                    )  # execute的时候出错了，会在这里直接报错(抛异常)

                    result = cursor.fetchall()
                    return dict(
                        result="ok",
                        id=result[0]["id"],
                        username=result[0]["username"],
                        fans=result[0]["fans"],
                    )

            # except:#catch(error):
            except Exception as e:
                return dict(result="fail", error=str(e))

        elif request.method == "DELETE":
            print(request.json)
            # 获取post body中的id等
            id = request.json.get("id")
            print(id)

            # 插入新的数据到数据库
            connection = db.get_db()
            # 为了避免 SQL 注入的风险,更安全的做法是使用参数化查询,即使用占位符 (?) 来代替直接插入变量值

            query = "DELETE FROM userProfile WHERE id = ?"
            # values = (id) #错误写法
            # (id,) 是一个包含单个元素的元组。元组是一种不可变的序列数据类型。
            # (id) 只是一个单独的整数值。
            values = (id,)  # 注意要使用逗号将单个值包裹成元组
            try:
                cursor = connection.execute(
                    query, values
                )  # execute的时候出错了，会在这里直接报错(抛异常)

                # commit 当你对数据库有改动的时候，需要commit，否则改动不会生效
                connection.commit()

                return dict(
                    result="ok",
                    id=id,
                )
            except Exception as e:
                return dict(result="fail", error=str(e))

    return app
