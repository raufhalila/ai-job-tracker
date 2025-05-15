from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/jobs')
def jobs():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()

    conn.close()

    return render_template("jobs.html", jobs=jobs)

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    company = request.form['company']
    link = request.form['link']
    date = request.form['date']

    print("you submitted a new job")
    print("Title: ", title)
    print("Company: ", company)
    print("Link: ", link)
    print("Date: ", date)

    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    c.execute("INSERT INTO jobs (title, company, link, date) VALUES (?, ?, ?, ?)", (title, company, link, date))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:job_id>')
def delete(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/edit/<int:job_id>', methods=['POST', 'GET'])
def edit(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        link = request.form['link']
        date = request.form['date']

        c.execute("""
            UPDATE jobs SET title = ?, company = ?, link = ?, date = ?
            WHERE id = ?
        """, (title, company, link, date, job_id))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    else:
        c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job = c.fetchone()
        conn.close()
        return render_template('edit.html', job=job)
    
@app.route('/cover-letter/<int:job_id>', methods=['POST', 'GET'])
def cover_letter(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = c.fetchone()
    conn.close()

    letter = None

    if request.method == 'POST':
        
        prompt = f"""
        Write a short, enthusiastic and professional cover letter for a job application.
        The position is '{job[1]}' at the company '{job[2]}'. Mention interest, value, and a strong closing line.
        """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        letter = response.json()["response"]

    return render_template('cover_letter.html', job=job, letter=letter)

if __name__ == '__main__':
    app.run(debug=True)