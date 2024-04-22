from flask import Flask , render_template , redirect , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///List.db"
db = SQLAlchemy(app)
app.app_context().push()

class Quiz(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(200) , nullable = False)
    time = db.Column(db.String(500) , nullable = False)
    last_date = db.Column(db.DateTime , default = datetime.now)
    

    def __repr__(self) -> str:
        return f"{self.name} - {self.time} - {self.last_date}"

@app.route("/home")
@app.route("/")
def HomePage():
    # quiz = Quiz(name="Science" , time="3hr")
    # db.session.add(quiz)
    # db.session.commit()
    allquizes = Quiz.query.all()
    return render_template('index.html' , allquizes=allquizes)

@app.route("/Quizpanel")
def Quizpanel():
    allquizes = Quiz.query.all()
    return render_template('quizpanel.html' , allquizes=allquizes)

@app.route("/Managequiz")
def Managequiz():
    allquizes = Quiz.query.all()
    return render_template('managequizes.html' , allquizes=allquizes)

@app.route("/Addquiz" , methods=['GET' , 'POST'])
def Addquiz():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        lastdate = datetime.strptime(request.form['lastdate'], '%Y-%m-%d')
        quiz = Quiz(name=name,time=time,last_date=lastdate)
        db.session.add(quiz)
        db.session.commit()
    allquizes = Quiz.query.all()
    return render_template('addquiz.html' , allquizes=allquizes)

@app.route('/Delete/<int:sno>')
def delete(sno):
    quiz = Quiz.query.filter_by(sno = sno).first()
    db.session.delete(quiz)
    db.session.commit()
    allquizes = Quiz.query.all()
    return render_template('managequizes.html' , allquizes=allquizes)

@app.route("/Test")
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True , port=8000)