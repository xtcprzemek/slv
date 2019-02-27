from flask import Flask, render_template, request, redirect, json, jsonify
from OracleSession import OracleSession
from flask.helpers import locked_cached_property
import jinja2_highlight
import os

class MyFlask(Flask):
    jinja_options = dict(Flask.jinja_options)
    jinja_options.setdefault('extensions',
        []).append('jinja2_highlight.HighlightExtension')

    # If you'd like to set the class name of the div code blocks are rendered in
    # Uncomment the below lines otherwise the option below can be used
    @locked_cached_property
    def jinja_env(self):
        jinja_env = self.create_jinja_environment()
        jinja_env.extend(jinja2_highlight_cssclass = 'codehilite')
        return jinja_env

app = MyFlask(__name__)

if os.environ.get('ENV') == 'PROD':
    app.config.from_pyfile('production.cfg')
else:
    app.config.from_pyfile('config.cfg')


dbuser=app.config.get('USERNAME')
dbpass=app.config.get('PASSWORD')
dsn=app.config.get('DSN')



items_per_site=app.config.get('ITEMS_PER_SITE')

##Routing##
@app.route("/", methods=["GET", "POST"])
def home():
    print("przed połączeniem")
    sess = OracleSession(dbuser, dbpass, dsn)
    print("połączony")
    sessions = sess.get_sessions()

    cnt = sess.get_sessions_count()
    nofpg= sess.get_nof_sites(items_per_site)
    sess.disconnect()
    return render_template("home.html", sessions=sessions, cnt=cnt, nofpg=nofpg)


@app.route("/sites/<int:id>")
def sessions(id):
    sess = OracleSession(dbuser, dbpass, dsn)
    sessions = sess.get_session_page(id, items_per_site)

    if sessions :
        #print("session exists")
        cnt = sess.get_sessions_count()
        nofpg = sess.get_nof_sites(items_per_site)
        sess.disconnect()
        return render_template("sessions.html", sessions=sessions , cnt=cnt, nofpg=nofpg, pgno=id)
    else :
        sess.disconnect()
        return render_template("404.html")

@app.route("/session/<int:session_id>")
def session(session_id):
    sess = OracleSession(dbuser, dbpass, dsn)
    session = sess.get_session(session_id)
    steps=sess.get_session_steps(session_id)
    step_tasks=sess.get_session_step_tasks(session_id)
    for task in step_tasks:
        txt = sess.get_log_txt(task.session_id, task.scen_task_no)
        #highlited = highlight(txt, PythonLexer(), HtmlFormatter())
        task.txt=txt
    sess.disconnect()
    return render_template("session.html",  session=session, steps=steps, step_tasks=step_tasks)

@app.route("/sites/failed/<int:id>")
def failed(id):
    sess = OracleSession(dbuser, dbpass, dsn)
    failed = sess.get_failed_sessions(id, items_per_site)

    if failed :
        #print("session exists")
        cnt = sess.get_sessions_count('E')
        nofpg = sess.get_nof_sites(items_per_site, 'E')
        sess.disconnect()
        return render_template("sessions.html", sessions=failed , cnt=cnt, nofpg=nofpg, pgno=id)
    else :
        sess.disconnect()
        return render_template("404.html")

@app.route("/api/logtext", methods=["GET", "POST"])
def logtext():
    print("i am in log")
    session_id = request.args.get('session_id')
    print(f"session_id{session_id}")
    step_task_no = request.args.get('step_task_no')
    #print(session_id, scen_task_no)
    sess = OracleSession(dbuser, dbpass, dsn)
    txt=sess.get_log_txt(session_id, step_task_no)
    sess.disconnect()
    #highlited = highlight(txt, PythonLexer(), HtmlFormatter())
    #print(highlited)
    return jsonify(txt)


##example below to remove
@app.route("/env")
def env():
    return os.environ.get('ENV')
@app.route("/test")
def test():
    code="select * from dual"
    highlited =highlight(code, PythonLexer(), HtmlFormatter())
    return highlited


@app.route("/getEmployeeList")
def getEmployeeList():
    # Initialize a employee list
    employeeList = []

    #create a instances for filling up employee list
    for i in range(0, 2):
        empDict = {
                'firstName': 'Roy',
                'lastName': 'Augustine'}
        employeeList.append(empDict)

            # convert to json data
    jsonStr = json.dumps(employeeList)

    return jsonify(Employees=jsonStr)
################################

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
####End of Routing###############



if __name__ == "__main__":
    #sess = OracleSession(dbuser, dbpass, dsn)
    app.run()