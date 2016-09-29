from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234527@localhost/mydb'
db = SQLAlchemy(app)

class POST(db.Model):
    __tablename__ = 'POST'
    pid = db.Column('pid', db.Integer, primary_key=True)
    note = db.Column('note', db.Integer, primary_key=True)
    link = db.Column('link', db.String(64), primary_key=True)
    title = db.Column('title', db.String(64), primary_key=True)
    userName = db.Column('userName', db.String(64), primary_key=True)

topPosts = POST.query.order_by(POST.note.desc()).limit(20).all()

@app.route('/')
def index():
    return render_template('index.html', topPosts=topPosts)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name='JOJO')

if __name__ == '__main__':
    app.run(debug=True)
