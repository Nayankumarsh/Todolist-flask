from flask import Flask,render_template,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Item_Title = db.Column(db.String(200), nullable=False) 
    Desc = db.Column(db.String(500), nullable=False) 
    Date_Created = db.Column(db.DateTime, default = datetime.utcnow) 

    def __repr__(self) ->str:
        return f'{self.SNo}-{self.Item_Title}'

with app.app_context():
    db.create_all()

@app.route('/', methods = ["GET", "POST"])
def hello_world():
    if request.method=="POST":
        Item_Title = request.form["Item_Title"]
        Desc = request.form["Desc"]
        todo = Todo(Item_Title=Item_Title,Desc=Desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route('/delete/<int:SNo>')
def delete(SNo):
    
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:SNo>', methods = ["GET", "POST"])
def update(SNo):
    if request.method=="POST":
        Item_Title = request.form["Item_Title"]
        Desc = request.form["Desc"]
        todo = Todo.query.filter_by(SNo=SNo).first() 
        todo.Item_Title = Item_Title
        todo.Desc = Desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(SNo=SNo).first() 
    return render_template("update.html", todo=todo)
@app.route('/Home')
def Home():
    return 'Hello, World!'


if __name__=="__main__":
    app.run(debug=True,  port=8000)