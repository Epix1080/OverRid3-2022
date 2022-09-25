from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
POSTS = []

@app.route('/')
def home():
    return render_template('home.html') #change the name to appropiate name given 

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')#change the name to appropiate name given 

@app.route('/sobre_nosotros')
def contacto():
    return render_template('sn.html')#change the name to appropiate name given 

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'doc' or request.form['password'] != 'doc' or request.form['username'] != 'paciente' or request.form['password'] != 'paciente':
            error = 'Invalid Credentials. Please try again.'
        elif request.form['username'] != 'doc' or request.form['password'] != 'doc':
            return redirect(url_for('doclandpage'))
        else:
            return redirect(url_for('eficha'))

    return render_template('login.html', error=error)#change the name to appropiate name given https://www.youtube.com/watch?v=7nrVtrIBRh8

@app.route ('/register')
def register():
    return render_template('register.html')

