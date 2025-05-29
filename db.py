import sqlite3

def insert_user(username, password):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user


def get_all_jobs(user_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE user_id = ?", (user_id,))
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

def insert_job(title, company, link, date, user_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("INSERT INTO jobs (title, company, link, date, user_id) VALUES (?, ?, ?, ?, ?)", (title, company, link, date, user_id))
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

def search_jobs(query, user_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    wildcard = f"%{query}%"
    c.execute("SELECT * FROM jobs WHERE (title LIKE ? OR company LIKE ?) AND (user_id = ?)", (wildcard, wildcard, user_id))
    jobs = c.fetchall()
    conn.close()
    return jobs