from fileinput import close
from flask import Flask, flash, redirect, render_template, url_for, request, session, Response
from flask_session import Session
from tempfile import mkdtemp
from Fdweb import maindet
import sqlite3
import mysql.connector
import sys

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_THRESHOLD"] = 400
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = mkdtemp()
Session(app)


#https://flask.palletsprojects.com/en/2.0.x/api/
@app.after_request
def after_request(response):
    response.headers["Expires"] = 0
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Pragma"] = "no-cache"
    return response

# Handling the "/" route which is the main page
@app.route("/", methods=["GET", "POST"])
def login():
    # Handlig if the request method is POST or GET
    # POST allows to insert a new patient into the database
    if request.method == "POST":
        # Connection to sql

        username = request.form.get("username1")
        inserted_password = request.form.get("password")

        conn_general = mysql.connector.connect(user="user_test", password="OverRid3", host="34.173.224.249", database="datos-generales")

        cursor_general = conn_general.cursor()

        query_general1 = "select * from usuarios where userNameHash = '" + username + "'"
        query_general2 = "select * from usuarios where passwordHash = '" + inserted_password + "'"

        cursor_general.execute(query_general1)
        resultFrame1 = cursor_general.fetchall()

        cursor_general.execute(query_general2)
        resultFrame2 = cursor_general.fetchall()

        if (len(resultFrame1) > 0 and len(resultFrame2) > 0):
            return redirect("/home-page-user")
        else:
            conn_general.close()
            conn_hospital = mysql.connector.connect(user="user_test", password="OverRid3", host="34.173.224.249", database="datos-hospital")
            cursor_hospital = conn_hospital.cursor()

            query_general1 = "select * from usuarios where userHash = '" + username + "'"

            cursor_hospital.execute(query_general1)
            resultFrame1 = cursor_hospital.fetchall()

            cursor_hospital.execute(query_general2)
            resultFrame2 = cursor_hospital.fetchall()

            if (len(resultFrame1) > 0 and len(resultFrame2) > 0):
                return redirect("/home-page-dr")
            else:
                return redirect("/")
    else:
        return render_template("home-page.html")


@app.route("/home-page-dr", methods=["GET", "POST"])
def doclandpage():
    if request.method == "POST":
        # return redirect("/video_feed")
        return render_template("video-stream.html")
    else:
        return render_template("home-page-dr.html")

@app.route("/home-page-user")
def home_page_user():
    return render_template("home-page-user.html")


@app.route("/video_feed")
def video_feed():
     return Response(maindet(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/registro-paciente")
def registro_paciente():
     return render_template("registro-paciente.html")


@app.route("/historial-paciente")
def historial_paciente():
     return render_template("historial-paciente.html")


@app.route("/usuario-historial")
def usuario_historial():
     return render_template("historial-usuario.html")


@app.route("/usuario-info")
def usuario_info():
     return render_template("informacion-paciente.html")


if __name__=='__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, ssl_context='adhoc')