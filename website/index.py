from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234527@localhost/mydb'
db = SQLAlchemy(app)

class USER(db.Model):
    __tablename__ = 'USER'
    uid = db.Column(db.Integer, primary_key=True)
    nickName = db.Column(db.String(64))
    lastUpdate = db.Column(db.Integer)
    posts = db.relationship('POST', backref='user')

class POST(db.Model):
    __tablename__ = 'POST'
    pid = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Integer)
    link = db.Column(db.String(64))
    title = db.Column(db.String(64))
    userid = db.Column(db.Integer, db.ForeignKey('USER.uid'))

# db.create_all()

topPosts = POST.query.order_by(POST.note.desc()).limit(20).all()
for post in topPosts:
    user = post.userid
    print(user)

users = USER.query.all()
for u in users:
    for post in u.posts:
        print(post.pid)

@app.route('/')
def index():
    return render_template('index.html', topPosts=topPosts)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name='JOJO')

if __name__ == '__main__':
    app.run(debug=True)
