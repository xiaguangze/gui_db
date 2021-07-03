from flask import Flask, request, render_template, g, session, url_for, redirect
from connection_database import connect_db, return_data
from table_cols import get_table_name, get_table_pages, show_pages

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
page_size = 4


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

        session["host"] = request.form["host"]
        session["port"] = int(request.form["port"]) if request.form["port"] else 3306
        session["user"] = request.form["user"]
        session["pswd"] = request.form["pswd"]
        sql = "show databases;"
        try:
            databases = return_data(session["host"],
                                    session["port"],
                                    session["user"],
                                    session["pswd"],
                                    sql)
            session["dbs"] = databases
            g.nick = session["nick"] = request.form["nick"] if request.form["nick"] else ""

            return render_template("index.html",
                                   dbs=session["dbs"],
                                   tables=session["tables"])
        except Exception as e:
            error = "数据库连接失败" + str(e)
            g.nick = ""
            return render_template("index.html", error=error)

    return render_template("index.html", error=error)


@app.route("/query/<name>", methods=["GET"])
def query(name):
    sql = "show tables;"
    session["tables"] = tables = return_data(session["host"],
                                             session["port"],
                                             session["user"],
                                             session["pswd"],
                                             sql,
                                             databases=name)
    session["db_name"] = name

    return render_template("index.html",
                           dbs=session["dbs"],
                           tables=tables,
                           query_db=name)


@app.route("/table_data", methods=["GET"])
def table_data():
    session["current_table"] = name = request.args["name"]
    page_num = request.args["page_num"]
    sql = "select count(*) from %s" % name
    session["row"] = return_data(session["host"],
                                 session["port"],
                                 session["user"],
                                 session["pswd"],
                                 sql,
                                 databases=session["db_name"])[0]
    all_page = get_table_pages(session["row"], page_size)
    show_page = show_pages(all_page, int(page_num))
    sql = "desc %s;" % name
    session["col"] = return_data(session["host"],
                                 session["port"],
                                 session["user"],
                                 session["pswd"],
                                 sql,
                                 databases=session["db_name"])
    start_num = 0 + (int(page_num) - 1) * page_size
    stop_num = page_size if page_size <= session["row"] - page_size * (int(page_num)-1) \
                         else session["row"] - page_size * (int(page_num)-1)
    sql = "select * from %s limit %d,%d;" % (name, start_num, stop_num)
    datas = return_data(session["host"],
                        session["port"],
                        session["user"],
                        session["pswd"],
                        sql,
                        databases=session["db_name"],
                        status=1)

    return render_template("index.html",
                           dbs=session["dbs"],
                           tables=session["tables"],
                           cols=session["col"],
                           datas=datas,
                           query_db=session["db_name"],
                           all_page=show_page,
                           table=session["current_table"],
                           select_page=int(page_num))


@app.route("/query_one", methods=["POST"])
def query_one():
    if request.method == "POST":
        sql = request.form["query_one"]
        table_name = get_table_name(sql)
        col_sql = "desc %s" % table_name

        session["col"] = return_data(session["host"],
                                     session["port"],
                                     session["user"],
                                     session["pswd"],
                                     col_sql,
                                     databases=session["db_name"])

        datas = return_data(session["host"],
                            session["port"],
                            session["user"],
                            session["pswd"],
                            sql,
                            databases=session["db_name"],
                            status=1)

        return render_template("index.html",
                               dbs=session["dbs"],
                               tables=session["tables"],
                               cols=session["col"],
                               datas=datas,
                               query_db=session["db_name"])


if __name__ == '__main__':
    app.run()
