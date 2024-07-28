import sqlite3

import click
from flask import current_app, g

# 在flask这个app里面，每个请求都会有一个global，在请求的生命周期
# 任何时候都可以通过g来存储/访问一些信息（例如数据库连接，认证信息等）


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# open_resource()会打开一个相对于 flaskr 软件包的文件，这非常有用，因为在以后部署应用程序时，你不一定知道该文件的位置。 get_db 会返回一个数据库连接，用于执行从文件中读取的命令。
def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# click.command() 定义了一条名为 init-db 的命令行命令，它调用 init_db 函数并向用户显示成功消息。 你可以阅读 "命令行界面 "了解更多有关编写命令的信息。
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

#close_db 和 init_db_command 函数需要在应用程序实例中注册，否则应用程序不会使用它们。 但是，由于您使用的是工厂函数，因此在编写函数时，应用程序实例不可用。 取而代之的是，编写一个接收应用程序并进行注册的函数。
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
