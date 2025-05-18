from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from ai import generate_cover_letter
from db import get_all_jobs, get_job_by_id, insert_job, update_job, delete_job, search_jobs, insert_user, get_user

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        insert_user(username, hashed_password)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        usernamelogin = request.form['usernamelogin']
        passwordlogin = request.form['passwordlogin']

        user = get_user(usernamelogin)

        if user and check_password_hash(user[1], passwordlogin):
            session['user_id'] = user[0]
            session['username'] = usernamelogin
            return redirect(url_for('index'))
        else:
            print("Wrong user")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/jobs')
def jobs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    query = request.args.get('q')
    if query:
        jobs = search_jobs(query)
    else:
        jobs = get_all_jobs()

    return render_template("jobs.html", jobs=jobs)

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    company = request.form['company']
    link = request.form['link']
    date = request.form['date']

    insert_job(title, company, link, date)
    return redirect(url_for('jobs'))

@app.route('/delete/<int:job_id>')
def delete(job_id):
    delete_job(job_id)
    return redirect(url_for('index'))

@app.route('/edit/<int:job_id>', methods=['POST', 'GET'])
def edit(job_id):

    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        link = request.form['link']
        date = request.form['date']

        update_job(job_id, title, company, link, date)

        return redirect(url_for('jobs'))
    
    else:
        job = get_job_by_id(job_id)
        return render_template('edit.html', job=job)
    
@app.route('/cover-letter/<int:job_id>', methods=['POST', 'GET'])
def cover_letter(job_id):
    job = get_job_by_id(job_id)

    letter = None

    if request.method == 'POST':
        
        letter = generate_cover_letter(job[1], job[2])

    return render_template('cover_letter.html', job=job, letter=letter)

@app.route('/instant-letter', methods=['POST', 'GET'])
def instant_letter():
    letter = None

    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        requirements = request.form['requirements']

        from ai import generate_custom_letter
        letter = generate_custom_letter(title, company, requirements)

    return render_template('instant_letter.html', letter=letter)

if __name__ == '__main__':
    app.run(debug=True)