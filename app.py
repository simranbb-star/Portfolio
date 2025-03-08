from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS skills (id INTEGER PRIMARY KEY, name TEXT, level TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS experience (id INTEGER PRIMARY KEY, job_title TEXT, company TEXT, duration TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("SELECT * FROM skills")
    skills = c.fetchall()
    c.execute("SELECT * FROM experience")
    experience = c.fetchall()
    conn.close()
    
    # Debugging the data (remove in production)
    print("Skills:", skills)
    print("Experience:", experience)
    
    return render_template('resume.html', skills=skills, experience=experience)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add_skill', methods=['POST'])
def add_skill():
    name = request.form['name']
    level = request.form['level']
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("INSERT INTO skills (name, level) VALUES (?, ?)", (name, level))
    conn.commit()
    conn.close()
    return redirect(url_for('resume'))

@app.route('/add_experience', methods=['POST'])
def add_experience():
    job_title = request.form['job_title']
    company = request.form['company']
    duration = request.form['duration']
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("INSERT INTO experience (job_title, company, duration) VALUES (?, ?, ?)", (job_title, company, duration))
    conn.commit()
    conn.close()
    return redirect(url_for('resume'))
    
@app.route('/edit_skill/<int:skill_id>', methods=['GET', 'POST'])
def edit_skill(skill_id):
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()

    # Get the skill data
    c.execute("SELECT * FROM skills WHERE id=?", (skill_id,))
    skill = c.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        level = request.form['level']

        # Update the skill
        c.execute("UPDATE skills SET name=?, level=? WHERE id=?", (name, level, skill_id))
        conn.commit()
        conn.close()
        return redirect(url_for('resume'))

    conn.close()
    return render_template('edit_skill.html', skill=skill)

@app.route('/edit_experience/<int:exp_id>', methods=['GET', 'POST'])
def edit_experience(exp_id):
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()

    # Get the experience data
    c.execute("SELECT * FROM experience WHERE id=?", (exp_id,))
    experience = c.fetchone()

    if request.method == 'POST':
        job_title = request.form['job_title']
        company = request.form['company']
        duration = request.form['duration']

        # Update the experience
        c.execute("UPDATE experience SET job_title=?, company=?, duration=? WHERE id=?", 
                  (job_title, company, duration, exp_id))
        conn.commit()
        conn.close()
        return redirect(url_for('resume'))

    conn.close()
    return render_template('edit_experience.html', experience=experience)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
    #app.run(debug=True)