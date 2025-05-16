from flask import Flask, render_template, request, redirect, url_for

from ai import generate_cover_letter
from db import get_all_jobs, get_job_by_id, insert_job, update_job, delete_job

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/jobs')
def jobs():
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

if __name__ == '__main__':
    app.run(debug=True)