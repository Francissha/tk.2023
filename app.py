from flask import Flask ,render_template, url_for, redirect
from flask_sqlalchemy import SQLALchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqllite:///test.db'
db=SQLALchemy(app)

class Todo(db.model):
    id=db.column(db.integer, primary_key=True)
    content=db.column(db.string(200), nullable=False)
    completed=db.column(db.integer, default=0)
    date_created=db.column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=="POST":
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task"
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)  
    
@app.route('/delete/<int:id>')
def delete(id):
        task_to_delete=Todo.query.get_or_404(id)
        
try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
except:
    return 'There was problem deleting the task'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    Todo.query.get_or_404(id)
    if request.method=="POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem updating your task"
    else:
        return render_template(update.html)
    
if __name__ == ("__main__"):
    app.run(debug=True)













