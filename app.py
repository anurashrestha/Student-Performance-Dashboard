from flask import Flask, render_template, request, redirect
import json
import os
import uuid

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    student_name = request.form.get('name')
    subject = request.form.get('subject')
    try:
        grade = float(request.form.get('grade'))
    except ValueError:
        grade = None

    if student_name and subject and grade is not None:
        data = load_students()
        data.append({
            'id': str(uuid.uuid4()),  # unique identifier
            'name': student_name,
            'subject': subject,
            'grade': grade
        })
        save_students(data)

    return redirect('/dashboard')

@app.route('/dashboard')
def show_dashboard():
    students = load_students()
    return render_template('dashboard.html', students=students)

@app.route('/delete/<student_id>', methods=['POST'])
def delete_student(student_id):
    students = load_students()
    students = [s for s in students if s.get('id') != student_id]
    save_students(students)
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
