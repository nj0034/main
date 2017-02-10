from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__)
app.secret_key = '23@RASF@#IRJ@#@R@#G@#G@#GSGDGSDGSDGSDGGEWGEWGWG@#G@G@#G@#'

def sample():
    return 1000

@app.route('/')
def main():
    if session.get('is_logined'):
        return render_template('main.html', name=session.get('name'))
    else:
        return render_template('login.html')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    password = request.form['password']
    session['is_logined'] = True
    session['name'] = id
    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session['is_logined'] = False
    return redirect(url_for('main'))

@app.route('/hello/<name>')
def get_hello(name):
    return render_template('main.html', name=name)

if __name__ == '__main__':
    app.debug = True
    app.run()
