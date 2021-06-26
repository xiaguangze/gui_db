from flask import Flask, request, render_template, g, session, url_for, redirect
from connection_database import connect_db, return_data

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


@app.before_request
def load_connect_database():
    nickname = session.get('nick')
    if nickname:
        g.nick = nickname
    else:
        g.nick = ""


@app.before_first_request
def clear_env():
    session.clear()
    session["dbs"] = ""
    session["tables"] = ""


@app.route("/", methods=["GET"])
def return_index():
    return redirect(url_for("index"))


@app.route('/index', methods=["GET", "POST"])
def index():
    error = ""
    if request.method == "POST":
        if not request.form.get("host"):
            error = "host不能为空"
            return render_template("index.html", error=error)
        if not request.form["user"]:
            error = "用户名不能为空"
            return render_template("index.html", error=error)
        if not request.form["pswd"]:
            error = "密码不能为空"
            return render_template("index.html", error=error)

        g.nick = session["nick"] = request.form["nick"] if request.form["nick"] else request.form["nick"]
        session["host"] = request.form["host"]
        session["port"] = int(request.form["port"]) if request.form["port"] else 3306
        session["user"] = request.form["user"]
        session["pswd"] = request.form["pswd"]
        sql = "show databases;"
        try:
            databases = return_data(session["host"], session["port"], session["user"], session["pswd"], sql)
            session["dbs"] = databases
            return render_template("index.html", dbs=session["dbs"], tables=session["tables"])
        except Exception as e:
            error = "数据库连接失败" + str(e)
            return render_template("index.html", error=error)

    return render_template("index.html", error=error)


@app.route("/query/<name>", methods=["GET"])
def query(name):
    sql = "show tables;"
    session["tables"] = tables = return_data(session["host"], session["port"], session["user"], session["pswd"], sql, databases=name)
    session["db_name"] = name

    return render_template("index.html", dbs=session["dbs"], tables=tables)


@app.route("/table_data/<name>", methods=["GET"])
def table_data(name):
    sql = "desc %s;" % name
    session["col"] = colmuns = return_data(session["host"], session["port"], session["user"], session["pswd"], sql, databases=session["db_name"])
    sql = "select * from %s;" % name
    datas = return_data(session["host"], session["port"], session["user"], session["pswd"], sql, databases=session["db_name"], status=1)

    return render_template("index.html", dbs=session["dbs"], tables=session["tables"], cols=session["col"], datas=datas)


@app.route("/query_one", methods=["POST"])
def query_one():
    if request.method == "POST":
        sql = request.form["query_one"]
        datas = return_data(session["host"], session["port"], session["user"], session["pswd"], sql, databases=session["db_name"], status=1)

        return render_template("index.html", dbs=session["dbs"], tables=session["tables"], cols=session["col"], datas=datas)


if __name__ == '__main__':
    app.run()
