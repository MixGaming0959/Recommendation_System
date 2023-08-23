from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import jwt
import datetime
from functools import wraps

from Modules.userRequests import userRequests

import sqlite3
def get_user_by_email(email):
    path = r'D:\Coding\Machine_Learning\Recommendation_System\test\instances\users.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE Email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_movie_by_id(id):
    path = r'D:\Coding\Machine_Learning\Recommendation_System\test\instances\movies.db'
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Movies WHERE MovieID = ?', (id,))
    movie = cursor.fetchone()
    conn.close()
    return movie


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')  # ดึง Token จาก Session

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])

        user = get_user_by_email(email)
        if user and user[4] == password:  # ตรวจสอบรหัสผ่าน
            token = jwt.encode({'username': user[3], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
            session['token'] = token
            # return jsonify({'token': token, 'user_id':username})
            return redirect(url_for('dashboard'))

        return jsonify({'message': 'Invalid credentials'}), 401
    return render_template('login.html')
    
# return jsonify({'token': token, 'user_id':username})
# return redirect(url_for('dashboard'))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('token', None)  # ลบ Token จาก Session
    return redirect(url_for('home'))

#---------token_required------------------------------------------------------------------ 

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Hello, {current_user}! This is a protected route.'})

@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    return render_template('dashboard.html', username=current_user)

@app.route('/recommend', methods=['GET'])
@token_required
def recommend(current_user):
    req = userRequests()
    tmp = req.recommendTop10Movie(current_user)
    status, data = tmp['status'], tmp['data']
    if status == False:
        return data # is error
    movies = []
    for i in range(0, len(data)):
        id = int(data[i][0])
        prep = float(data[i][1])
        lis = list(get_movie_by_id(id))
        # print(lis)
        lis.append(prep)
        movies.append(lis)
    return render_template('recommend.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
