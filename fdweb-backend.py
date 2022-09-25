from Fdweb import maindet
from flask import Flask

app = Flask(__name__)

@app.route("/doclandpage")
def idpatient():
    maindet()
