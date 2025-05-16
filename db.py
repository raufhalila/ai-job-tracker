import sqlite3

def get_all_jobs():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()
    conn.close()
    return jobs

def get_job_by_id(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = c.fetchone()
    conn.close()
    return job

def insert_job(title, company, link, date):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("INSERT INTO jobs (title, company, link, date) VALUES (?, ?, ?, ?)", (title, company, link, date))
    conn.commit()
    conn.close()

def update_job(job_id, title, company, link, date):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("""
        UPDATE jobs SET title = ?, company = ?, link = ?, date = ?
        WHERE id = ?
    """, (title, company, link, date, job_id))
    conn.commit()
    conn.close()

def delete_job(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()