from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ai import generate_cover_letter
from db import get_all_jobs, get_job_by_id, insert_job, update_job, delete_job, search_jobs, insert_user, get_user, get_user_by_id

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'your_secret_key_here'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return User(id=user[0], username=user[1], password=user[2])
    return None


@app.route('/')
def home():
    return render_template("home.html")

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

        if user and check_password_hash(user[2], passwordlogin):
            user = User(id=user[0], username=user[1], password=user[2])
            login_user(user)
            return redirect(url_for('index'))
        else:
            print("Wrong user")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/jobs')
@login_required
def jobs():
    query = request.args.get('q')
    if query:
        jobs = search_jobs(query, current_user.id)
    else:
        jobs = get_all_jobs(current_user.id)

    return render_template("jobs.html", jobs=jobs)

@app.route('/add-job')
@login_required
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    title = request.form['title']
    company = request.form['company']
    link = request.form['link']
    date = request.form['date']

    insert_job(title, company, link, date, current_user.id)
    return redirect(url_for('jobs'))

@app.route('/delete/<int:job_id>')
@login_required
def delete(job_id):
    delete_job(job_id)
    return redirect(url_for('index'))

@app.route('/edit/<int:job_id>', methods=['POST', 'GET'])
@login_required
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
@login_required
def cover_letter(job_id):
    job = get_job_by_id(job_id)

    letter = None

    if request.method == 'POST':
        
        letter = generate_cover_letter(job[1], job[2])

    return render_template('cover_letter.html', job=job, letter=letter)

@app.route('/instant-letter', methods=['POST', 'GET'])
@login_required
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