
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

USERNAME = 'admin'
PASSWORD = 'recruit123'

def get_db_connection():
    conn = sqlite3.connect('jobs.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('job_listings'))

@app.route('/jobs')
def job_listings():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs ORDER BY date_posted DESC').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        category = request.form['category']
        salary = request.form['salary']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO jobs (title, location, category, salary, description) VALUES (?, ?, ?, ?, ?)',
                     (title, location, category, salary, description))
        conn.commit()
        conn.close()
        flash('Job added successfully!')
        return redirect(url_for('admin'))

    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
import os
port = int(os.environ.get('port', 5000))
app.run(host='0.0.0.0', port=port)
