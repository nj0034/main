from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

import json
import hashlib

app = Flask(__name__)
app.secret_key = '23@RASF@#IRJ@#@R@#G@#G@#GSGDGSDGSDGSDGGEWGEWGWG@#G@G@#G@#'
users = dict()
memo = dict()

def sample():
    return 1000

@app.route('/')
def main():
    if session.get('is_logined') and session.get('is_written'):
        return render_template('memo_write.html', subject=session.get('subject'), content=session.get('content')) and render_template('main.html', name=session.get('name'), subject=session.get('subject'), content=session.get('content'))
    else:
        return render_template('signin.html')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    id = request.form['id']
    password = request.form['password']

    if users.get(id):
        password = hashlib.sha1((password+'salting value').encode('utf-8')).hexdigest()
        if users[id] == password:
            session['is_logined'] = True
            session['name'] = id
            return redirect(url_for('main'))
        else:
            return render_template('signin.html', error_msg='비밀번호가 일치하지 않습니다.')
    else:
        return render_template('signin.html', error_msg='아이디가 없습니다.')


@app.route('/logout')
def logout():
    session['is_logined'] = False
    return redirect(url_for('main'))

@app.route('/join', methods=['GET','POST'])
def join():
    if request.method=='POST':
        id = request.form['id']
        password = request.form['password']
        re_password = request.form['re-password']

        if users.get(id):
            return render_template('join.html', error_msg='이미 아이디가 있습니다.')

        if not password == re_password:
            return render_template('join.html', error_msg='비밀번호가 일치하지 않습니다.')


        users[id] = hashlib.sha1((password+'salting value').encode('utf-8')).hexdigest()

        #저장하기
        file = open('users.json', 'w')
        file.write(json.dumps(users))
        return redirect(url_for('main'))

    elif request.method == 'GET':
        return render_template('join.html')

@app.route('/memo_write', methods=['GET','POST'])
def memo_write():
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']

        memo[subject] = content
        file = open('memo.json', 'w')
        file.write(json.dumps(memo))

        if memo.get(subject):
            session['is_written'] = True
            session['subject'] = subject
            session['content'] = content
        return redirect(url_for('main'))


    elif request.method == 'GET':
        return render_template('memo_write.html')

@app.route('/board', methods=['GET', 'POST'])
def board():
    return render_template('board.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/hello/<name>')
def get_hello(name):
    return render_template('main.html', name=name)

if __name__ == '__main__':
    file = open('users.json')
    users = json.loads(file.read())

    file = open('memo.json')
    memo = json.loads(file.read())

    app.debug = True
    app.run()

