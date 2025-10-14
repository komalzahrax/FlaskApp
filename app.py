from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    city = db.Column(db.String(100))

    # ✅ Fixed method name (was _repr_, must be __repr__)
    def __repr__(self):
        return f"{self.sno} - {self.fname}"

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    phone = request.form['phone']
    city = request.form['city']

    new_student = Student(fname=fname, lname=lname, email=email, phone=phone, city=city)
    db.session.add(new_student)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:sno>')
def delete(sno):
    student = Student.query.filter_by(sno=sno).first()
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    student = Student.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        student.fname = request.form['fname']
        student.lname = request.form['lname']
        student.email = request.form['email']
        student.phone = request.form['phone']
        student.city = request.form['city']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', student=student)

# ✅ Fixed the main guard (was '_main_', should be '__main__')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
