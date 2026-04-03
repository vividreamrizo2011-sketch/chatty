from flask import Flask, render_template_string, request, redirect
import json, os

app = Flask(__name__)

# Fayl nomlari
STUDENTS_FILE = 'students.json'
COMMENTS_FILE = 'comments.json'

# Yuklash funksiyasi
def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

# Saqlash funksiyasi
def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)

# Ma'lumotlar
students = load_data(STUDENTS_FILE)
comments = load_data(COMMENTS_FILE)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>O'quvchilar tizimi</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 8px; margin: 5px; }
        .box { border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>O'quvchilar ro'yxati</h1>

    <div class="box">
        <h2>O'quvchi qo'shish</h2>
        <form method="POST" action="/add">
            <input name="ism" placeholder="Ism" required>
            <input name="familiya" placeholder="Familiya" required>
            <input name="yosh" type="number" required>
            <input name="sinf" type="number" required>
            <button type="submit">Qo'shish</button>
        </form>
    </div>

    <div class="box">
        <h2>Ro'yxat:</h2>
        <ul>
        {% for s in students %}
            <li>
                {{loop.index}}. {{s['ism']}} {{s['familiya']}} - {{s['yosh']}, {{s['sinf']}}-sinf
                <a href="/delete/{{loop.index0}}">[O'chirish]</a>
            </li>
        {% endfor %}
        </ul>
    </div>

    <div class="box">
        <h2>Kommentariya</h2>
        <form method="POST" action="/comment">
            <input name="name" placeholder="Ismingiz" required>
            <input name="text" placeholder="Fikringiz" required>
            <button type="submit">Yuborish</button>
        </form>

        <h3>Kommentariyalar:</h3>
        <ul>
        {% for c in comments %}
            <li>
                <b>{{c['name']}}:</b> {{c['text']}}
                👍 {{c['like']}} 👎 {{c['dislike']}}
                <a href="/like/{{loop.index0}}">[Like]</a>
                <a href="/dislike/{{loop.index0}}">[Dislike]</a>
                <a href="/delete_comment/{{loop.index0}}">[O'chirish]</a>
            </li>
        {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML, students=students, comments=comments)

@app.route('/add', methods=['POST'])
def add():
    students.append({
        'ism': request.form['ism'],
        'familiya': request.form['familiya'],
        'yosh': int(request.form['yosh']),
        'sinf': int(request.form['sinf'])
    })
    save_data(STUDENTS_FILE, students)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(students):
        students.pop(index)
        save_data(STUDENTS_FILE, students)
    return redirect('/')

@app.route('/comment', methods=['POST'])
def comment():
    comments.append({
        'name': request.form['name'],
        'text': request.form['text'],
        'like': 0,
        'dislike': 0
    })
    save_data(COMMENTS_FILE, comments)
    return redirect('/')

@app.route('/delete_comment/<int:index>')
def delete_comment(index):
    if 0 <= index < len(comments):
        comments.pop(index)
        save_data(COMMENTS_FILE, comments)
    return redirect('/')

@app.route('/like/<int:index>')
def like(index):
    if 0 <= index < len(comments):
        comments[index]['like'] += 1
        save_data(COMMENTS_FILE, comments)
    return redirect('/')

@app.route('/dislike/<int:index>')
def dislike(index):
    if 0 <= index < len(comments):
        comments[index]['dislike'] += 1
        save_data(COMMENTS_FILE, comments)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
